# Use official Python runtime as base image
FROM python:3.11-slim

# Set working directory in container
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies (if needed)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .
COPY config.py .
COPY database.py .

# Create data directory for SQLite database
RUN mkdir -p /app/data && \
    chmod 755 /app/data

# Expose port (Cloud Run will set PORT env variable)
EXPOSE 8080

# Run the application with gunicorn
# Cloud Run sets PORT environment variable automatically
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app
