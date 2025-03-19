# Use a stable Python version
ARG PYTHON_VERSION=3.12
FROM python:${PYTHON_VERSION}-slim AS base

# Prevents Python from writing pyc files and buffers stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app/

# Create a non-privileged user
ARG UID=10001
RUN adduser --disabled-password --gecos "" --home "/nonexistent" --shell "/usr/sbin/nologin" --no-create-home --uid "${UID}" appuser

# Install system dependencies and clean up to reduce image size
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc g++ python3-dev cmake make build-essential \
    libopenblas-dev libx11-dev \
    && rm -rf /var/lib/apt/lists/*  # Clean apt cache

# Copy only requirements file first (to leverage Docker caching)
COPY requirements.txt .

# Install dependencies efficiently
RUN pip install --no-cache-dir --no-deps -r requirements.txt

# Create logs directory with correct permissions
RUN mkdir -p /app/logs && chmod 755 /app/logs && chown appuser:appuser /app/logs

# Copy source code
COPY ./silver_watch /app

# Switch to non-root user only for execution
USER appuser

# Expose application port
EXPOSE 8000

# Define Django settings and environment file
ENV DJANGO_SETTINGS_MODULE=silver_watch.settings
ENV ENVFILE=/.env

# Start Celery and Daphne properly
CMD ["sh", "-c", "cd silver_watch && \
    python manage.py collectstatic --noinput && \
    python manage.py makemigrations && \
    python manage.py migrate && \
    celery -A silver_watch worker --loglevel=info --pool=threads --concurrency=4 & \
    celery -A silver_watch beat --loglevel=info --pool=threads --concurrency=4 & \
    cd silver_watch && \
    exec daphne -b 0.0.0.0 -p 8000 silver_watch.asgi:application"]
