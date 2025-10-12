FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies (use Heroku-specific requirements)
COPY requirements-heroku.txt /app/
RUN pip install --upgrade pip --root-user-action=ignore
RUN pip install -r requirements-heroku.txt --root-user-action=ignore

# Copy project
COPY . /app/

# Expose port
EXPOSE $PORT

# Use Heroku's PORT environment variable
CMD gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
