# Counterparty-Exposure-Limit-Monitor

# Contact Info

Want to hire me? Check out my LinkedIn here: https://www.linkedin.com/in/jesse-o-03476a102/

Want to comission me for a project? Check out my Upwork profile here: https://www.upwork.com/freelancers/~0193f57dd84700cb81

# Counterparty Exposure Limit Monitoring Dashboard
Overview

This project is a lightweight web application for monitoring counterparty exposure limits.

Built using Python, and Flask - the application allows users to upload exposure files and automatically identifies:

Breaches (Exposure > Limit)

Near Breaches (Exposure above user-defined threshold %)

Safe positions

The system is designed to demonstrate how institutional risk monitoring workflows can be translated into deterministic, auditable code.

Problem Statement

In financial institutions, counterparty exposure monitoring is often handled via manually maintained spreadsheets.

This introduces risks:

Delayed breach detection

Inconsistent threshold logic

Lack of audit trail

Manual sorting/filtering

This application formalizes limit monitoring logic programmatically.

How It Works
Input

A CSV file containing:

Counterparty,Exposure,Limit


Example:

Alpha Capital Partners,12000000,10000000
Beta Financial LLC,8500000,10000000

Core Logic

The application performs the following steps:

Normalizes and validates required columns

Coerces exposure and limit fields to numeric

Computes:

utilization = exposure / limit
utilization_pct = utilization * 100


Classifies counterparties:

BREACH → utilization > 1.0

NEAR_BREACH → utilization >= threshold (user configurable)

OK → below threshold

Sorts counterparties by utilization (descending)

Web Application Features

CSV Upload via browser

Adjustable “Near Breach” threshold (percentage)

Segregated breach view

Downloadable processed CSV

Timestamped run tracking

In-memory storage for last processed file (demo mode)

Tech Stack

Python 3

Pandas

Flask

Jinja templating

File Structure
project/
│
├── app.py
├── sample_exposures.csv
├── templates/
│   └── index.html
├── requirements.txt
└── README.md

Running the Application

Install dependencies:

pip install flask pandas


Run the server:

python app.py


Navigate to:

http://127.0.0.1:5000


Upload your exposure CSV and define your near-breach threshold.

# Why This Project Matters

This project demonstrates:

Risk classification logic

Financial data validation

Exposure monitoring workflows

Deterministic classification systems

Web delivery of risk analytics

It mirrors real-world limit monitoring systems used in:

Counterparty Credit Risk

Prime Brokerage

Commodities Trading

Hedge Fund Risk Oversight

Structured Products

Future Improvements

Potential production-ready enhancements:

PostgreSQL persistence layer

Historical breach archiving

Email / Slack alerts

Exposure aggregation by sector or rating

Time-series tracking of utilization trends

VaR overlays

Role-based authentication

Author:

Jesse Olivarez
Finance Professional | Credit Risk | Data Analytics
