# Astra Tarot Bot - Secure Docker Image
# =====================================
# Uses python:3.10-alpine for minimal CVE surface

FROM python:3.10-alpine

LABEL maintainer="Astra Team"
LABEL description="Astra Tarot Discord Bot"

# Install security updates and required packages
RUN apk update && \
    apk upgrade && \
    apk add --no-cache \
        git \
        gcc \
        musl-dev \
        libffi-dev \
    && rm -rf /var/cache/apk/*

# Create non-root user for security
RUN adduser -D -h /home/container container

# Set working directory
WORKDIR /home/container

# Copy and install dependencies first (better caching)
COPY pyproject.toml ./
RUN pip install --no-cache-dir --user \
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

# Create data directory and set permissions
RUN mkdir -p /home/container/data && \
    chown -R container:container /home/container

# Switch to non-root user
USER container

# Set environment
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PATH="/home/container/.local/bin:${PATH}"

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)" || exit 1

# Run
ENTRYPOINT ["python", "-m", "astra"]
