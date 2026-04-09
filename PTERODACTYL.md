# Pterodactyl Deployment Guide
==============================

This guide explains how to deploy Astra on a Pterodactyl panel.

## Quick Start

### Method 1: Using Docker Image (Recommended)

1. Build and push the Docker image:
```bash
docker build -t your-registry/astra-bot:latest .
docker push your-registry/astra-bot:latest
```

2. In Pterodactyl, create a server using the Astra Egg

3. Set the environment variable:
   - `DISCORD_TOKEN` - Your bot token

4. Start the server

### Method 2: Using Git Clone (Egg with Git)

1. Create a server with the "Astra" egg
2. Set startup parameters:
   - `REPO_URL`: `https://giteas.fullmooncyberworks.com/mystiatech/Astra.git`
   - `BRANCH`: `main`
3. Set environment variable:
   - `DISCORD_TOKEN`: Your bot token
4. Start the server - it will auto-pull and run

---

## Pterodactyl Egg Configuration

### Egg JSON

Create a new egg with these settings:

**Name:** Astra Tarot Bot
**Description:** Discord tarot reading bot with dynamic themes
**Docker Image:** `python:3.10-slim` (or your custom image)
**Startup Command:** `python -m astra`

### Configuration Parser

```json
{
  "config": {
    "files": "{\
    \".env\": {\n        \"parser\": \"properties\",\n        \"find\": {\n            \"DISCORD_TOKEN\": \"{{server.build.env.DISCORD_TOKEN}}\"\n        }\n    }\n}",
    "startup": "{\n    \"done\": \"Synced.*slash commands\"\n}",
    "logs": "{}",
    "stop": "^C"
  }
}
```

### Startup Script

```bash
#!/bin/bash
# Pterodactyl Startup Script for Astra

cd /home/container

# Export environment variables
export DISCORD_TOKEN={{DISCORD_TOKEN}}
export LOG_LEVEL={{LOG_LEVEL}}|INFO

# Create .env file from environment
cat > .env << EOF
DISCORD_TOKEN=${DISCORD_TOKEN}
LOG_LEVEL=${LOG_LEVEL}
EOF

# Run the bot
python -m astra
```

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DISCORD_TOKEN` | ✅ Yes | - | Your Discord bot token |
| `LOG_LEVEL` | ❌ No | INFO | Logging level (DEBUG, INFO, WARNING, ERROR) |
| `DEFAULT_READING_TIMEOUT` | ❌ No | 300 | Session timeout in seconds |

### Image Configuration

**Base Image:** `python:3.10-slim`

**Installation Script:**
```bash
#!/bin/bash
# Pterodactyl Installation Script

cd /home/container

# Clone the repository
git clone {{REPO_URL}} . || git pull

# Install dependencies
pip install --user -e .

echo "Astra installation complete!"
```

---

## Building Custom Docker Image

### 1. Build Image

```bash
cd astra
docker build -t your-dockerhub-username/astra-bot:v1.0.0 .
```

### 2. Test Locally

```bash
docker run -e DISCORD_TOKEN=your_token_here your-dockerhub-username/astra-bot:v1.0.0
```

### 3. Push to Registry

```bash
docker push your-dockerhub-username/astra-bot:v1.0.0
```

### 4. Use in Pterodactyl

Update the egg to use your custom image:
```
your-dockerhub-username/astra-bot:v1.0.0
```

---

## Adding Themes in Pterodactyl

Since Pterodactyl uses containers, themes work slightly differently:

### Method 1: Mount Volume (Recommended)

In Pterodactyl, mount a volume for themes:

```
/mnt/pterodactyl/themes/astra:/home/container/themes
```

Upload themes to `/mnt/pterodactyl/themes/astra/` on the host.

### Method 2: Include in Image

Build a custom image with themes baked in:

```dockerfile
FROM your-registry/astra-bot:latest

# Add custom themes
COPY my-theme/ /home/container/themes/my-theme/
```

### Method 3: Git Submodules

If using the Git clone method, themes can be added as submodules.

---

## Updating the Bot

### Manual Update

1. Stop the server
2. Reinstall (pulls latest code)
3. Start the server

### Auto-Update (with Git egg)

Set `AUTO_UPDATE` environment variable:
```bash
AUTO_UPDATE=1
```

The startup script will pull latest changes before starting.

---

## Troubleshooting

### "No module named 'astra'"

The installation script didn't run properly. Try:
1. Reinstall the server
2. Check installation logs

### "Permission denied"

Pterodactyl runs as non-root in some configurations. Ensure:
```dockerfile
USER root
```
in the Dockerfile.

### Themes not appearing

Check that the themes directory is properly mounted:
```bash
# In the container
ls -la /home/container/themes/
```

### High memory usage

Astra is lightweight, but if needed:
1. Limit concurrent readings
2. Reduce theme image sizes
3. Set memory limits in Pterodactyl

---

## Resource Requirements

| Resource | Minimum | Recommended |
|----------|---------|-------------|
| RAM | 256 MB | 512 MB |
| CPU | 0.25 cores | 0.5 cores |
| Storage | 100 MB | 500 MB (with themes) |
| Network | Outbound only | Outbound only |

---

## Docker Compose (for testing)

```yaml
version: '3.8'

services:
  astra:
    build: .
    container_name: astra-bot
    environment:
      - DISCORD_TOKEN=${DISCORD_TOKEN}
      - LOG_LEVEL=INFO
    volumes:
      - ./themes:/home/container/themes:ro
      - ./data:/home/container/data
    restart: unless-stopped
```

---

## Support

For issues specific to Pterodactyl deployment:
1. Check Pterodactyl logs
2. Verify environment variables are set
3. Ensure Discord token is valid
4. Check file permissions

For bot issues, see the main README.md.
