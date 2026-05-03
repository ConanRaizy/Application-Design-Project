FROM python:3.13.3-slim as base

ENV PYTHONUNBUFFERED 1

# Install system dependencies including nginx
RUN apt-get update && apt-get install -y \
    libpq-dev \
    build-essential \
    nginx \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt /app/
RUN python3 -m pip install --no-cache-dir -r requirements.txt
RUN python3 -m pip install gunicorn

# Copy entire project from GitHub (Jenkins clones it first)
COPY . /app/

# Run Django setup
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput

# Set Django settings module
ENV DJANGO_SETTINGS_MODULE=mapps_cars.settings

# Copy nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

# Start Gunicorn and Nginx together
CMD sh -c "gunicorn --chdir /app mapps_cars.wsgi:application --bind 127.0.0.1:8000 & nginx -g 'daemon off;'"
