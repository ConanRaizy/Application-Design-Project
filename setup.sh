#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# Mapps Cars — one-shot setup script
# Run this once after cloning to get the project ready.
# ─────────────────────────────────────────────────────────────────────────────
set -e

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Running migrations..."
python manage.py migrate

echo "Creating superuser (admin) and demo customer..."
python manage.py shell << 'EOF'
from django.contrib.auth.models import User

# Admin account
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin',
        password='admin123',
        email='admin@mappscars.com',
        first_name='Admin',
        last_name='Mapps'
    )
    print("  ✓ Admin user created  (username: admin / password: admin123)")
else:
    print("  ✓ Admin user already exists")

# Regular customer account
if not User.objects.filter(username='customer').exists():
    u = User.objects.create_user(
        username='customer',
        password='customer123',
        email='customer@example.com',
        first_name='Jane',
        last_name='Doe'
    )
    print("  ✓ Customer user created  (username: customer / password: customer123)")
else:
    print("  ✓ Customer user already exists")
EOF

echo "Loading sample vehicle data..."
python manage.py shell << 'EOF'
from cars.models import Car
if Car.objects.count() == 0:
    cars = [
        dict(make='BMW',        model='3 Series',  year=2022, price=32500, mileage=18000, fuel_type='petrol',   color='Alpine White',   status='available', description='Immaculate condition, full service history, heated seats.'),
        dict(make='Mercedes',   model='C-Class',   year=2021, price=29900, mileage=24000, fuel_type='diesel',   color='Obsidian Black', status='available', description='AMG Line exterior, panoramic sunroof, wireless charging.'),
        dict(make='Audi',       model='A4',        year=2020, price=24500, mileage=35000, fuel_type='diesel',   color='Daytona Grey',   status='sold',      description='S Line, Quattro AWD, Bang & Olufsen sound system.'),
        dict(make='Tesla',      model='Model 3',   year=2023, price=38000, mileage=8000,  fuel_type='electric', color='Pearl White',    status='available', description='Long Range, Autopilot, 350 mile range. Like new.'),
        dict(make='Porsche',    model='Cayenne',   year=2021, price=65000, mileage=21000, fuel_type='hybrid',   color='Jet Black',      status='reserved',  description='E-Hybrid, BOSE surround, 21" wheels, sport chrono package.'),
    ]
    for c in cars:
        Car.objects.create(**c)
    print(f"  ✓ {len(cars)} sample vehicles added")
else:
    print(f"  ✓ {Car.objects.count()} vehicles already in database")
EOF

echo ""
echo "─────────────────────────────────────────────────"
echo " Mapps Cars is ready!"
echo " Run: python manage.py runserver"
echo " Then open: http://localhost:8000"
echo ""
echo " Admin login:    admin / admin123"
echo " Customer login: customer / customer123"
echo "─────────────────────────────────────────────────"
