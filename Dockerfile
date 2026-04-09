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

# Copy entire project
COPY --chown=container:container . /home/container/

# Install the package
RUN pip install --no-cache-dir -e /home/container

# Verify installation
RUN python -c "import astra; print('Astra installed successfully')"

# Create data directory
RUN mkdir -p /home/container/data && chown -R container:container /home/container

# Switch to container user
USER container

# Set environment
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV USER=container
ENV HOME=/home/container

# Run
CMD ["python", "-m", "astra"]
