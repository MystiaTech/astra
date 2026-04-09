# Gitea Actions Setup Guide
===========================

This guide explains how to build Docker images automatically using Gitea Actions.

## Prerequisites

1. Gitea instance with Actions enabled
2. Gitea Container Registry enabled
3. A runner configured (self-hosted or using act_runner)

## Setup Steps

### 1. Enable Gitea Actions

In your Gitea instance (`giteas.fullmooncyberworks.com:30009`):

1. Go to **Site Administration** → **Actions**
2. Enable Actions
3. Note the **Actions URL** (usually same as Gitea URL)

### 2. Register a Runner

On your WSL2 machine or a server:

```bash
# Download act_runner
wget https://dl.gitea.com/act_runner/main/linux-amd64/act_runner
chmod +x act_runner

# Register the runner
./act_runner register \
  --instance https://giteas.fullmooncyberworks.com:30009 \
  --token <YOUR_REGISTRATION_TOKEN>

# Get token from:
# Gitea Admin → Actions → Runners → Create New Runner

# Start the runner
./act_runner daemon
```

Or use Docker for the runner:
```bash
docker run --rm -it \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v $(pwd)/data:/data \
  gitea/act_runner:latest \
  register \
  --instance https://giteas.fullmooncyberworks.com:30009 \
  --token <YOUR_REGISTRATION_TOKEN>
```

### 3. Create Gitea Token

1. Go to your Gitea profile → **Settings** → **Applications**
2. Generate a new **Access Token**
3. Grant scopes: `package`, `repo`
4. Copy the token

### 4. Add Token to Repository Secrets

1. Go to your Astra repository → **Settings** → **Secrets**
2. Add a new secret:
   - **Name:** `GITEA_TOKEN`
   - **Value:** Your access token from step 3

### 5. Push the Workflow

The workflow file (`.gitea/workflows/docker-build.yml`) is already in the repo.

Push to main:
```bash
git add .gitea/workflows/docker-build.yml
git commit -m "Add Gitea Actions workflow"
git push origin main
```

### 6. Verify Build

1. Go to repository → **Actions** tab
2. You should see the workflow running
3. Once complete, check **Packages** for the built image

## Using the Built Image

### Pull from Gitea Registry

```bash
# Login to Gitea registry
docker login giteas.fullmooncyberworks.com:30009 -u mystiatech

# Pull the image
docker pull giteas.fullmooncyberworks.com:30009/mystiatech/astra-bot:main

# Run it
docker run -e DISCORD_TOKEN=your_token_here \
  giteas.fullmooncyberworks.com:30009/mystiatech/astra-bot:main
```

### Deploy to Pterodactyl

Update the egg to use your Gitea registry:

```json
{
  "docker_images": {
    "giteas.fullmooncyberworks.com:30009/mystiatech/astra-bot:latest": "giteas.fullmooncyberworks.com:30009/mystiatech/astra-bot:latest"
  }
}
```

## Alternative: Manual Build on Server

If you don't want to set up Actions, build on your server:

```bash
# SSH to your server
ssh user@your-server

# Install Docker if not present
curl -fsSL https://get.docker.com | sh

# Clone and build
git clone https://giteas.fullmooncyberworks.com/mystiatech/Astra.git
cd Astra/astra
docker build -t astra-bot .

# Run
docker run -d \
  --name astra \
  -e DISCORD_TOKEN=your_token \
  -v $(pwd)/themes:/home/container/themes \
  -v $(pwd)/data:/home/container/data \
  astra-bot
```

## Troubleshooting

### "No runner available"

- Make sure your runner is registered and online
- Check runner status in Gitea Admin → Actions → Runners

### "Authentication failed"

- Verify GITEA_TOKEN is set correctly in repository secrets
- Ensure token has `package` scope

### "Cannot connect to Docker daemon"

The runner needs access to Docker. If using Docker runner:
```bash
docker run ... -v /var/run/docker.sock:/var/run/docker.sock ...
```

If using binary runner, ensure user is in docker group:
```bash
sudo usermod -aG docker $USER
```

## Resources

- [Gitea Actions Documentation](https://docs.gitea.com/usage/actions/overview)
- [Act Runner Documentation](https://gitea.com/gitea/act_runner)
- [Gitea Container Registry](https://docs.gitea.com/usage/packages/container)
