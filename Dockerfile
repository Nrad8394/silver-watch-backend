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

# Install development tools
RUN pip install --no-cache-dir \
    watchfiles supervisor

# Copy source code after dependency installation (to optimize Docker caching)
COPY . /app/

# Copy entrypoint and supervisor configuration
COPY entrypoint.sh supervisord.conf /app/
RUN chmod +x /app/entrypoint.sh


# Expose application port
EXPOSE 8000

# Define Django settings and environment file
ARG ENVFILE
ENV DJANGO_SETTINGS_MODULE=silver_watch.settings
# Allow external env file override
ENV ENVFILE=${ENVFILE:-/app/.env}  

# Ensure entrypoint.sh is executable
RUN chmod +x /app/entrypoint.sh

# Set entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]