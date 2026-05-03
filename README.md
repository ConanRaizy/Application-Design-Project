# Mapps Cars

A Django-based car dealership management system for **Mapps Cars**.

## Features
- Customer showroom to browse available vehicles
- Customer review submission
- Admin panel: manage vehicles, reviews, and respond to customers
- Jenkins CI/CD pipeline integration

## Setup

```bash
bash setup.sh
```

Or manually:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

## Django Settings Module
`mapps_cars.settings`

## Access
- Showroom: `http://<your-ip>:8000/showroom/`
- Admin panel: `http://<your-ip>:8000/admin-panel/`
- Login: `http://<your-ip>:8000/login/`
