# Astra Tarot Bot - Pterodactyl Compatible Image
# ==============================================

FROM python:3.10-slim

LABEL maintainer="Astra Team"
LABEL description="Astra Tarot Discord Bot for Pterodactyl"

# Install git and other dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Create container user and directory
RUN useradd -m -d /home/container -s /bin/bash container

# Set working directory
WORKDIR /home/container

# Pre-install dependencies (for faster startup)
RUN pip install --no-cache-dir \
    discord-py>=2.3.0 \
    python-dotenv>=1.0.0 \
    aiohttp>=3.9.0 \
    pydantic>=2.5.0 \
    watchdog>=3.0.0 \
    Pillow>=10.0.0 \
    pytest>=7.4.0 \
    pytest-asyncio>=0.21.0

# Copy application code
COPY --chown=container:container src/ ./src/
COPY --chown=container:container themes/ ./themes/
COPY --chown=container:container assets/ ./assets/
COPY --chown=container:container tests/ ./tests/
COPY --chown=container:container pyproject.toml ./
COPY --chown=container:container README.md ./

# Create necessary directories
RUN mkdir -p /home/container/data /home/container/logs && \
    chown -R container:container /home/container

# Switch to container user
USER container

# Set environment
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV USER=container
ENV HOME=/home/container

# Default command (can be overridden by Pterodactyl)
CMD ["python", "-m", "astra"]
