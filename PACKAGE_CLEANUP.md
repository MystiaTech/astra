# Cleaning Up Old Docker Packages

## GitHub Container Registry (GHCR)

### Delete Old Package via GitHub UI

1. Go to: `https://github.com/MystiaTech?tab=packages`
2. Find the old package (probably named `astra`)
3. Click on it
4. Go to **Package settings** (gear icon on right side)
5. Scroll to **Danger Zone**
6. Click **Delete this package**
7. Type the package name to confirm
8. Click **I understand the consequences, delete this package**

### Delete via GitHub API (if UI doesn't work)

```bash
# Get GitHub token with 'delete:packages' scope
# Then run:

# List packages
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://api.github.com/users/MystiaTech/packages?package_type=container

# Delete specific package
curl -X DELETE \
  -H "Authorization: Bearer YOUR_TOKEN" \
  https://api.github.com/users/MystiaTech/packages/container/astra
```

### Fix Package Description

1. Go to package page: `https://github.com/MystiaTech/astra/pkgs/container/astra`
2. Click **Package settings**
3. Edit **Description** field
4. Add something like: "Astra Tarot Discord Bot - Discord bot for tarot readings"
5. Save

## Docker Hub

### Delete Old Repository

1. Go to: `https://hub.docker.com/repositories/mystiatech`
2. Find old repository (probably `astra` without `-bot`)
3. Click on it
4. Click **Settings** tab
5. Click **Delete repository**
6. Type repository name to confirm

### Update Description

1. Go to repository: `https://hub.docker.com/r/mystiatech/astra-bot`
2. Click **Settings** tab
3. Edit:
   - **Description**: "Astra Tarot Discord Bot - Beautiful tarot readings for Discord"
   - **README**: Link to GitHub repo
4. Click **Save**

## Fixing GitHub Actions

The old package name might be cached. Update your workflow:

```yaml
# In .github/workflows/docker-build.yml
# Make sure IMAGE_NAME matches what you want
env:
  IMAGE_NAME: astra-bot  # NOT just "astra"
```

## If You Can't Delete

Sometimes packages get stuck. Try these:

1. **Logout and back in** to GitHub/Docker Hub
2. **Clear browser cache** 
3. **Use incognito/private mode**
4. **Try different browser**
5. **Contact GitHub Support** if it's stuck

## Prevent This in Future

Add to your workflow to automatically clean old images:

```yaml
- name: Delete old images
  uses: actions/delete-package-versions@v4
  with:
    package-name: 'astra-bot'
    package-type: 'container'
    min-versions-to-keep: 10
    delete-only-untagged-versions: 'true'
```
