# syntax=docker/dockerfile:1

# Use a minimal Python 3.11 slim image
FROM python:3.11-slim

# Set environment variables
# PYTHONDONTWRITEBYTECODE: Prevents Python from writing pyc files to disc
# PYTHONUNBUFFERED: Prevents Python from buffering stdout and stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    # Set a non-root user for security
    UID=10001 \
    GID=10001

# Set working directory
WORKDIR /app

# Install system dependencies required for building Python packages
# --no-install-recommends to keep image size small
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user to run the application
RUN groupadd -g "${GID}" appuser \
    && useradd --create-home --no-log-init -u "${UID}" -g "${GID}" appuser

# Copy requirements file first to leverage Docker layer caching
COPY requirements.txt .

# Install Python dependencies
# Use cache mount to speed up subsequent builds
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Change ownership of the application code to the non-root user
RUN chown -R appuser:appuser /app

# Switch to the non-root user
USER appuser

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
# Using uvicorn as the ASGI server for FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
