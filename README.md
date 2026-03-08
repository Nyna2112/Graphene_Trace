# Graphene Trace Django Project

A Django web application for the Graphene Trace case study.

## Features
- Custom authentication with 3 roles: Admin, Clinician, Patient
- Patient/clinician/admin dashboards
- CSV upload for time-ordered 32x32 pressure-map frames
- Session, frame, metrics, alerts, comments, replies, explanations, reports
- Trend analysis and comparison with previous session
- Rule-based risk detection
- Optional ML model training/prediction from stored metrics
- PDF report generation

## Quick start
1. Create and activate a virtual environment.
2. Install requirements: `pip install -r requirements.txt`
3. Run migrations: `python manage.py migrate`
4. Create a superuser: `python manage.py createsuperuser`
5. Seed demo data if needed: `python manage.py seed_demo`
6. Start server: `python manage.py runserver`
7. Open `http://127.0.0.1:8000/`

## Login routing
- Admin users go to admin dashboard
- Clinicians go to clinician dashboard
- Patients go to patient dashboard

## CSV format expected
- 32 rows and 32 columns per frame
- Blank line separates frames
- Optional timestamp line before a frame: `timestamp,2025-03-07T10:15:00`
- Sensor values should be from 1 to 4095
