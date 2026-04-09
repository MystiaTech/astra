# Astra Tarot Bot - Pterodactyl Docker Image
# ==========================================

FROM python:3.10-slim

LABEL maintainer="Astra Team"
LABEL description="Astra Tarot Discord Bot for Pterodactyl"

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /home/container

# Copy requirements first for better caching
COPY pyproject.toml ./

# Install Python dependencies
RUN pip install --no-cache-dir \
    discord-py>=2.3.0 \
    python-dotenv>=1.0.0 \
    aiohttp>=3.9.0 \
    pydantic>=2.5.0 \
    watchdog>=3.0.0 \
    Pillow>=10.0.0

# Copy application code
COPY src/ ./src/
COPY themes/ ./themes/
COPY assets/ ./assets/
COPY data/ ./data/

# Create necessary directories
RUN mkdir -p /home/container/data /home/container/logs

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV LOG_LEVEL=INFO

# Pterodactyl uses this user
USER root

# Entrypoint
ENTRYPOINT ["python", "-m", "astra"]
