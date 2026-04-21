# Graphene Trace - Pressure Monitoring System

## Demo credentials
- Admin: `admin` / `admin@123`
- Clinician: `clinician` / `clinician@123`
- Patients: `kartheek`, `neyana`, `priyanka`, `mahesh`, `shankar` with password `username@123`

## Run
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo --zip-path sample_data/GTLB-Data.zip
python manage.py runserver
```
