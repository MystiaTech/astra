# Astra Tarot Bot - Production Image
# ==================================
# Based on python:3.10-slim with security hardening

FROM python:3.10-slim AS builder

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
WORKDIR /install
COPY pyproject.toml ./
COPY src/ ./src/
RUN pip install --user --no-cache-dir .

# Production stage
FROM python:3.10-slim

LABEL maintainer="MystiaTech"
LABEL description="Astra Tarot Discord Bot"

# Security: Create non-root user
RUN groupadd -r container && useradd -r -g container -d /home/container container

# Install runtime dependency (git for Pterodactyl)
RUN apt-get update && \
    apt-get install -y --no-install-recommends git && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean

WORKDIR /home/container

# Copy installed packages from builder
COPY --from=builder /root/.local /home/container/.local

# Copy application
COPY --chown=container:container src/ ./src/
COPY --chown=container:container themes/ ./themes/
COPY --chown=container:container assets/ ./assets/
COPY --chown=container:container pyproject.toml ./

# Install runtime dependencies
RUN pip install --user --no-cache-dir \
    discord-py>=2.3.0 \
    python-dotenv>=1.0.0 \
    aiohttp>=3.9.0 \
    pydantic>=2.5.0 \
    watchdog>=3.0.0 \
    Pillow>=10.0.0 && \
    rm -rf /home/container/.cache

# Create data directory
RUN mkdir -p /home/container/data && \
    chown -R container:container /home/container

# Switch to non-root user
USER container

# Environment
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PATH="/home/container/.local/bin:$PATH"
ENV USER=container
ENV HOME=/home/container

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import astra" || exit 1

CMD ["python", "-m", "astra"]
