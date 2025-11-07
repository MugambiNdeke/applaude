# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables for the runtime
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Install system dependencies needed for psycopg2 (PostgreSQL adapter)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file and install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire Django project code
COPY . /app/

# Expose the default Gunicorn port (8000 is common)
EXPOSE 8000

# Set the entrypoint script
ENTRYPOINT ["/app/start.sh"]
