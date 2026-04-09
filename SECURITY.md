# Security Information
======================

## CVE Status

### Current Status
The `mystiatech/astra-bot` image on Docker Hub has some CVEs detected. This is normal for Python-based images.

### What are these CVEs?

Most CVEs found are in:
- **System libraries** (glibc, openssl, etc.) - used by Python interpreter
- **Python standard library** - rarely exploitable in bot context
- **Build tools** - not present in final image

### Severity Assessment

For a Discord bot that:
- ✅ Only makes outbound HTTPS connections
- ✅ Has no open ports
- ✅ Runs as non-root user
- ✅ Processes only Discord slash commands

**Risk Level: LOW**

Most CVEs require:
- Local system access
- Specific network conditions
- Malicious input processing
- Privileged execution

None of which apply to Astra's use case.

## Mitigation Strategies

### Option 1: Use Alpine-Based Image (Recommended)

The updated `Dockerfile` now uses `python:3.10-alpine` which has:
- Smaller attack surface
- Fewer packages = fewer CVEs
- Regular Alpine security updates

```bash
docker build -t mystiatech/astra-bot:alpine .
docker push mystiatech/astra-bot:alpine
```

### Option 2: Use Distroless Image (Maximum Security)

```bash
docker build -f Dockerfile.distroless -t mystiatech/astra-bot:distroless .
docker push mystiatech/astra-bot:distroless
```

Distroless images contain only your application and its runtime dependencies:
- No shell
- No package manager
- No unnecessary libraries
- Minimal CVE surface

### Option 3: Regular Rebuilds

CVEs are constantly being fixed. Schedule regular rebuilds:

```yaml
# .github/workflows/rebuild.yml
name: Rebuild for Security Updates
on:
  schedule:
    - cron: '0 0 * * 0'  # Weekly
```

## Best Practices

### 1. Always Use Latest Tag

```bash
docker pull mystiatech/astra-bot:latest
```

### 2. Scan Before Deploying

```bash
# Using Trivy
trivy image mystiatech/astra-bot:latest

# Using Docker Scout
docker scout cves mystiatech/astra-bot:latest
```

### 3. Run as Non-Root

Already configured in Dockerfile:
```dockerfile
USER container
```

### 4. Minimal Environment

Only required env vars:
- `DISCORD_TOKEN` (required)
- `LOG_LEVEL` (optional)

No secrets in image!

### 5. Read-Root Filesystem

Run container with read-only root:
```bash
docker run --read-only \
  -v /tmp:/tmp \
  -e DISCORD_TOKEN=xxx \
  mystiatech/astra-bot:latest
```

## Reporting Security Issues

If you find a security vulnerability specific to Astra's code (not base image CVEs):

1. **DO NOT** open a public issue
2. Email: security@fullmooncyberworks.com
3. Include: Description, reproduction steps, impact assessment

## Security Features in Astra

- ✅ No privileged Discord intents required
- ✅ Only responds to slash commands (structured input)
- ✅ No file uploads processed (only images displayed)
- ✅ No database connections
- ✅ No external API calls (except Discord)
- ✅ Session timeouts prevent resource exhaustion
- ✅ Single-session reading prevents abuse

## Base Image Comparison

| Image | Size | CVE Count | Use Case |
|-------|------|-----------|----------|
| `python:3.10` | ~900MB | High | Development |
| `python:3.10-slim` | ~120MB | Medium | General use |
| `python:3.10-alpine` | ~60MB | Low | Production ✅ |
| `distroless` | ~50MB | Minimal | High security ✅ |

## Recommended Deployment

For production with security focus:

```bash
# Build alpine version
docker build -t mystiatech/astra-bot:alpine .

# Scan it
trivy image mystiatech/astra-bot:alpine

# Push
docker push mystiatech/astra-bot:alpine

# Run with security options
docker run -d \
  --name astra \
  --read-only \
  --security-opt=no-new-privileges:true \
  --cap-drop=ALL \
  -e DISCORD_TOKEN=your_token \
  mystiatech/astra-bot:alpine
```

## TL;DR

- Current CVEs are in base Python image, not Astra code
- Risk is low due to bot's limited functionality
- Use `alpine` or `distroless` tags for fewer CVEs
- Rebuild regularly to get security patches
- Run as non-root with minimal permissions
