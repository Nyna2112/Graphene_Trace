<<<<<<< HEAD
# HealthCare

A clean, role-based Django web application for Admin, Clinician, and Patient users.

## Features

- Single login page for all users with **Hospital Application** heading
- Role-based redirection after login
- Patient dashboard with clinician details, latest blood pressure report, Chart.js trend chart, and symptom submission
- Clinician dashboard with today's patient count, recent consultations, pending reviews, high blood pressure alerts, weekly logbook, and prescription history
- Admin dashboard with right-side management menu, clinician access control, file management, user management, patient feedback, activity logs, clinician counts, recent activity, and alerts
- Bootstrap-based templates
- Django custom user model with roles
- SQLite database by default
- Sample seed data command

## Project structure

- `users` - authentication, roles, user model
- `dashboard` - dashboards and admin/clinician/patient workflows
- `templates` - frontend templates
- `static` - static files

## Setup

```bash
python -m venv venv
# Windows
venv\Scriptsctivate
# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py seed_data
python manage.py runserver
```

## Sample logins

After running `seed_data`:

- Admin: `admin` / `admin123`
- Clinician: `clinician1` / `clinician123`
- Patient: `patient1` / `patient123`

## URLs

- Login: `/`
- Admin dashboard: `/dashboard/admin/`
- Clinician dashboard: `/dashboard/clinician/`
- Patient dashboard: `/dashboard/patient/`

## Notes

- The application uses Django's built-in auth plus a custom user model.
- Chart.js is loaded from CDN for the patient blood pressure trend chart.
- Sample data includes users, profiles, pressure reports, prescriptions, activity logs, and feedback.
=======
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
>>>>>>> 97d8f1e099dcb14aee571f3435fdeabc74c65f11
