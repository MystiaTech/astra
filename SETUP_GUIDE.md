# Discord Bot Setup Guide
=========================

This guide explains how to set up Astra in the Discord Developer Portal.

## Required Permissions

### OAuth2 Scopes

When inviting the bot, you need these **scopes**:

| Scope | Required | Why |
|-------|----------|-----|
| `bot` | ✅ Yes | The bot needs to connect as a bot user |
| `applications.commands` | ✅ Yes | Required for slash commands |

### Bot Permissions

Astra needs these **permissions**:

| Permission | Required | Purpose |
|------------|----------|---------|
| `Send Messages` | ✅ Yes | Send reading results |
| `Embed Links` | ✅ Yes | Send rich embeds for cards |
| `Attach Files` | ✅ Yes | Display card images |
| `Use External Emojis` | ❌ No | Uses built-in Discord emojis only |
| `Add Reactions` | ❌ No | Not used |
| `Read Message History` | ❌ No | Only responds to slash commands |

### Intents

In the Discord Developer Portal under "Privileged Gateway Intents", you need:

| Intent | Required | Purpose |
|--------|----------|---------|
| `MESSAGE CONTENT` | ❌ No | Not needed - uses slash commands |
| `SERVER MEMBERS` | ❌ No | Not needed |
| `PRESENCE` | ❌ No | Not needed |

**Note:** Astra only uses basic intents, no privileged intents required!

---

## Step-by-Step Setup

### 1. Create Application

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application"
3. Name it "Astra" (or your preferred name)
4. Click "Create"

### 2. Get Bot Token

1. In your application, go to "Bot" tab
2. Click "Add Bot" or "Reset Token"
3. Click "Copy" to get your token
4. **SAVE THIS SECRETLY** - put it in your `.env` file:
   ```
   DISCORD_TOKEN=your_token_here
   ```

### 3. Enable Privileged Intents (if needed)

Astra doesn't need any, but if you enable message content intent:

1. In "Bot" tab, scroll to "Privileged Gateway Intents"
2. Toggle `MESSAGE CONTENT INTENT` **OFF** (not needed)
3. Save changes

### 4. Invite Bot to Server

**Method A: Using URL Generator (Recommended)**

1. Go to "OAuth2" → "URL Generator"
2. Select scopes:
   - ✅ `bot`
   - ✅ `applications.commands`
3. Select bot permissions:
   - ✅ `Send Messages`
   - ✅ `Embed Links`
   - ✅ `Attach Files`
   - ✅ `Read Messages/View Channels`
4. Copy the generated URL
5. Open in browser and invite to your server

**Method B: Direct URL**

Replace `YOUR_CLIENT_ID` with your application's Client ID:

```
https://discord.com/api/oauth2/authorize?client_id=YOUR_CLIENT_ID&permissions=18432&scope=bot%20applications.commands
```

This URL grants:
- `Send Messages` (2048)
- `Embed Links` (16384)
- Total: 18432

### 5. Verify It's Working

1. Run the bot: `python -m astra`
2. In Discord, type `/` and you should see Astra's commands
3. Try `/tarot-help` to verify

---

## Permission Calculator

If you want custom permissions, use this calculator:

| Permission | Bit Value |
|------------|-----------|
| Create Instant Invite | 1 |
| Kick Members | 2 |
| Ban Members | 4 |
| Administrator | 8 |
| Manage Channels | 16 |
| Manage Guild | 32 |
| Add Reactions | 64 |
| View Audit Log | 128 |
| Priority Speaker | 256 |
| Stream | 512 |
| View Channel | 1024 |
| Send Messages | 2048 |
| Send TTS Messages | 4096 |
| Manage Messages | 8192 |
| **Embed Links** | **16384** |
| Attach Files | 32768 |
| Read Message History | 65536 |
| Mention Everyone | 131072 |
| Use External Emojis | 262144 |
| View Guild Insights | 524288 |
| Connect | 1048576 |
| Speak | 2097152 |
| Mute Members | 4194304 |
| Deafen Members | 8388608 |
| Move Members | 16777216 |
| Use Voice Activity | 33554432 |
| Change Nickname | 67108864 |
| Manage Nicknames | 134217728 |
| Manage Roles | 268435456 |
| Manage Webhooks | 536870912 |
| Manage Emojis | 1073741824 |
| Use Application Commands | 2147483648 |

**Astra's minimum:** 2048 + 16384 + 32768 + 1024 = **52224**

---

## Troubleshooting

### Commands don't appear

1. Make sure you included `applications.commands` scope when inviting
2. Wait up to 1 hour for global commands to sync (they sync on bot start)
3. Try kicking and re-inviting the bot

### Bot shows as offline

1. Check your `DISCORD_TOKEN` is correct
2. Check bot logs for errors
3. Verify the bot process is running

### Can't invite bot

1. You need "Manage Server" permission on the target server
2. Check that the OAuth2 URL has the correct Client ID
3. Ensure scopes include both `bot` and `applications.commands`

---

## Security Notes

- **Never share your bot token** - anyone with it can control your bot
- **Don't commit .env files** - add to `.gitignore`
- **Use separate bots for dev/prod** - create a test application for development

---

## Quick Reference

```bash
# .env file
discord.com/developers/applications
```

**Minimal Invite URL:**
```
https://discord.com/api/oauth2/authorize?client_id=YOUR_CLIENT_ID&permissions=52224&scope=bot%20applications.commands
```

That's it! Astra should now work in your server. 🔮
