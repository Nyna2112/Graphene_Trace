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
