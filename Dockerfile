# Astra Tarot Bot - Pterodactyl Compatible Image
# ==============================================

FROM python:3.10-slim

LABEL maintainer="Astra Team"
LABEL description="Astra Tarot Discord Bot for Pterodactyl"

# Install git and build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Create container user
RUN useradd -m -d /home/container -s /bin/bash container

# Set working directory
WORKDIR /home/container

# Copy and install to system Python (as root)
COPY . /opt/astra/
RUN cd /opt/astra && pip install --no-cache-dir . && \
    pip install --no-cache-dir discord-py python-dotenv aiohttp pydantic watchdog Pillow

# Copy static assets to system location
RUN cp -r /opt/astra/themes /opt/astra-assets/ && \
    cp -r /opt/astra/assets /opt/astra-assets/

# Verify installation
RUN python -c "import astra; print('Astra installed:', astra.__file__)"

# Fix permissions
RUN chmod -R 755 /usr/local/lib/python3.10/site-packages/astra*

# Switch to container user
USER container

# Environment
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV USER=container
ENV HOME=/home/container

# Default command
CMD ["python", "-m", "astra"]
