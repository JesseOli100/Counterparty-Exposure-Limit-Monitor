from flask import Flask, render_template, request, redirect, url_for, send_file, flash
import pandas as pd
import io
from datetime import datetime

app = Flask(__name__)
app.secret_key = "change-this-in-production"

# Simple in-memory store for last processed file (demo purposes)
last_processed_csv = None
last_run_timestamp = None


def analyze_exposures(df, near_breach_threshold=0.8):
    """
    Expects columns: Counterparty, Exposure, Limit
    Returns enriched df and separate dataframes for breaches / near / ok.
    """
    # Normalize column names
    df = df.rename(columns={c: c.strip().lower() for c in df.columns})

    required_cols = {"counterparty", "exposure", "limit"}
    if not required_cols.issubset(set(df.columns)):
        raise ValueError(
            f"Input must contain columns: {', '.join(required_cols)}. "
            f"Got: {', '.join(df.columns)}"
        )

    # Coerce numeric
    for col in ["exposure", "limit"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Drop rows with missing critical data
    df = df.dropna(subset=["counterparty", "exposure", "limit"])

    # Compute utilization
    df["utilization"] = df["exposure"] / df["limit"]
    df["utilization_pct"] = (df["utilization"] * 100).round(1)

    # Initialize status column
    df["status"] = "OK"

    # Classify explicitly
    df.loc[df["utilization"] > 1.0, "status"] = "BREACH"
    df.loc[
        (df["utilization"] >= near_breach_threshold) & (df["utilization"] <= 1.0),
        "status"
    ] = "NEAR_BREACH"

    # Sort by utilization desc
    df = df.sort_values(by="utilization", ascending=False)

    # Split into separate frames
    breaches = df[df["status"] == "BREACH"]
    near = df[df["status"] == "NEAR_BREACH"]
    ok = df[df["status"] == "OK"]

    return df, breaches, near, ok



@app.route("/", methods=["GET", "POST"])
def index():
    global last_processed_csv, last_run_timestamp

    if request.method == "POST":
        file = request.files.get("file")
        threshold_str = request.form.get("threshold", "0.8")

        if not file or file.filename == "":
            flash("Please upload a CSV file.", "danger")
            return redirect(url_for("index"))

        try:
            threshold = threshold = float(threshold_str) / 100.0
        except ValueError:
            flash("Threshold must be a number (e.g. 0.8).", "danger")
            return redirect(url_for("index"))

        try:
            df = pd.read_csv(file)
            full_df, breaches, near, ok = analyze_exposures(df, near_breach_threshold=threshold)

            # Save to memory for optional CSV download
            csv_buffer = io.StringIO()
            full_df.to_csv(csv_buffer, index=False)
            last_processed_csv = csv_buffer.getvalue()
            last_run_timestamp = datetime.utcnow()

            return render_template(
                "index.html",
                results=True,
                breaches=breaches.to_dict(orient="records"),
                near=near.to_dict(orient="records"),
                ok=ok.to_dict(orient="records"),
                threshold=int(threshold * 100),
                total=len(full_df),
                breach_count=len(breaches),
                near_count=len(near),
                ok_count=len(ok),
            )
        except Exception as e:
            flash(f"Error processing file: {e}", "danger")
            return redirect(url_for("index"))

    # GET
    return render_template("index.html", results=False)


@app.route("/download")
def download():
    global last_processed_csv, last_run_timestamp
    if not last_processed_csv:
        flash("No processed file available. Please upload and analyze a file first.", "warning")
        return redirect(url_for("index"))

    buffer = io.BytesIO(last_processed_csv.encode("utf-8"))
    filename = f"counterparty_exposure_analysis_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.csv"
    return send_file(
        buffer,
        mimetype="text/csv",
        as_attachment=True,
        download_name=filename,
    )


if __name__ == "__main__":
    app.run(debug=True)
