# Pterodactyl Deployment Guide
==============================

This guide explains how to deploy Astra on a Pterodactyl panel.

## Recommended Image

For Pterodactyl, we recommend using either:

1. **`mystiatech/astra-bot:latest`** (Standard, ~100 CVEs) - Full compatibility
2. **`mystiatech/astra-bot:alpine`** (Recommended, ~20 CVEs) - Good security balance

**Note:** The `distroless` image does NOT work with Pterodactyl because it has no shell for the installation script.

## Quick Setup

### 1. Import the Egg

1. Download `egg-astra.json` from the repository
2. In Pterodactyl Admin: **Nests** → **Import Egg**
3. Upload the JSON file
4. Select a nest (e.g., "Discord Bots")

### 2. Create Server

| Setting | Value |
|---------|-------|
| **Egg** | Astra Tarot Bot |
| **Docker Image** | `mystiatech/astra-bot:alpine` (recommended) |
| **Startup Command** | `python -m astra` |

### 3. Set Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `DISCORD_TOKEN` | ✅ Yes | Your Discord bot token |
| `LOG_LEVEL` | ❌ No | DEBUG/INFO/WARNING/ERROR |

### 4. Start Server

The server will:
1. Pull the Docker image
2. Run the startup command
3. Show "Astra is ready" when online

## Docker Image Comparison

| Image | CVEs | Size | Pterodactyl Compatible |
|-------|------|------|------------------------|
| `latest` | ~100 | 150MB | ✅ Yes |
| `alpine` | ~20 | 80MB | ✅ Yes (Recommended) |
| `distroless` | ~5 | 70MB | ❌ No (no shell) |

## Troubleshooting

### "No module named astra"

The image is outdated. Update to the latest:
```
mystiatech/astra-bot:alpine
```

### Server stuck on "Starting"

Check that the startup detection is set to look for:
```
Astra is ready
```

### Permission denied

Ensure the Docker image runs as a non-root user. Our images are configured with `USER container` or `USER nonroot`.

### Commands don't appear in Discord

1. Wait 1 hour for global commands to sync, OR
2. Kick and re-invite the bot to your server

## Alternative: Git-based Deployment

If you prefer to have the code editable:

1. Use **Generic Python** egg
2. **Docker Image**: `python:3.10-alpine`
3. **Startup**: `python -m astra`
4. **Install Script**:
```bash
apk add --no-cache git
 git clone https://giteas.fullmooncyberworks.com/mystiatech/Astra.git .
cd astra
pip install -e .
```

This clones fresh code on each reinstall.

## Support

For issues:
1. Check Pterodactyl logs
2. Verify Docker image tag
3. Ensure Discord token is valid
4. Check the [GitHub Issues](https://github.com/MystiaTech/astra/issues)
