# Security Information
======================

## CVE Status

### Current Status

The standard `mystiatech/astra-bot:latest` image may have CVEs from the base Python image. We provide multiple image variants with different security levels.

### Available Image Variants

| Tag | Base | CVE Count | Size | Use Case |
|-----|------|-----------|------|----------|
| `latest` | `python:3.10-slim` | ~100 | ~150MB | General use |
| `alpine` | `python:3.10-alpine` | ~20 | ~80MB | **Recommended** |
| `distroless` | `gcr.io/distroless` | ~5 | ~70MB | High security |

### Recommendation for Lower CVEs

Use the **Alpine** or **Distroless** variants:

```bash
# Alpine (fewer CVEs, good compatibility)
docker pull mystiatech/astra-bot:alpine

# Distroless (minimal CVEs, maximum security)
docker pull mystiatech/astra-bot:distroless
```

## Mitigation Strategies

### 1. Use Alpine-Based Image (Recommended)

```bash
docker run -e DISCORD_TOKEN=xxx mystiatech/astra-bot:alpine
```

### 2. Regular Updates

We rebuild images regularly to incorporate security patches. Use the automated rebuild workflow:

```yaml
# .github/workflows/rebuild.yml
name: Weekly Security Rebuild
on:
  schedule:
    - cron: '0 0 * * 0'  # Weekly
```

### 3. Scan Before Deploying

```bash
# Using Trivy
trivy image mystiatech/astra-bot:alpine

# Using Docker Scout
docker scout cves mystiatech/astra-bot:alpine
```

## Why CVEs in Standard Image?

The standard image (`python:3.10-slim`) includes:
- Debian base system
- Many system libraries
- Build tools

These provide compatibility but increase CVE surface.

## Best Practices

1. **Use Alpine variant for production**
2. **Run as non-root** (already configured)
3. **Scan images before deployment**
4. **Keep images updated**
5. **Use read-only filesystems** where possible

## Reporting Security Issues

Email: security@fullmooncyberworks.com

## Security Features

- ✅ No privileged Discord intents required
- ✅ Runs as non-root user
- ✅ Single-session prevents abuse
- ✅ No database connections
- ✅ Minimal external dependencies
