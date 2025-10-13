# =============================================================================
# Multi-stage Dockerfile for Django App Store
# =============================================================================

# Stage 1: Base image with Python
FROM python:3.11-slim as base

# Note: This project supports Python 3.8+, but 3.11 is recommended for best performance

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    postgresql-client \
    libpq-dev \
    gettext \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# =============================================================================
# Stage 2: Development image
# =============================================================================
FROM base as development

# Copy requirements
COPY requirements/ requirements/

# Install development dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements/development.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p logs staticfiles uploads

# Expose port
EXPOSE 8000

# Development command
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# =============================================================================
# Stage 3: Production image
# =============================================================================
FROM base as production

# Copy requirements
COPY requirements/ requirements/

# Install production dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements/production.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && \
    mkdir -p logs staticfiles uploads && \
    chown -R appuser:appuser /app

# Collect static files
RUN python manage.py collectstatic --noinput || true

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Production command using gunicorn
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "120"]

