# 🔮 Astra - Tarot Reading Discord Bot

Astra is a Discord bot that provides authentic tarot readings including single card, three-card spreads, and more. She handles **one reading at a time** to ensure quality and focus.

## Features

- ✅ **Single Card Reading** - Quick guidance for daily reflection
- ✅ **Three Card Spread** - Past, Present, Future
- ✅ **Mind-Body-Spirit** - Holistic self-examination
- ✅ **Situation-Action-Outcome** - Problem-solving guidance
- ✅ **Celtic Cross** - In-depth 10-card spread
- ✅ **Relationship Spread** - Insights into connections (7 cards)
- ✅ **Career Path Spread** - Professional guidance (5 cards)
- ✅ **Dynamic Themes** - Multiple card decks, auto-detected, hot-reload

## Team Structure

| Role | Lead | Responsibility |
|------|------|----------------|
| Project Lead | **Kimi** | Architecture, coordination, integration |
| Research | **Sarah** | Tarot meanings, spreads, validation, theme docs |
| Backend | **Emma** | Discord bot, session management, theme system |
| UX/Frontend | **Olivia** | Embeds, card display, theme selection UI |
| Assets | **Maya** | Placeholder images, cover art, theme structure |
| QA | **Chloe** | Testing, validation, edge cases |

## Installation

### Quick Deploy Options

| Method | Difficulty | Best For |
|--------|------------|----------|
| [Local](#local-setup) | Easy | Development, testing |
| [Pterodactyl](#pterodactyl-deployment) | Medium | Production hosting |
| [Docker](#docker) | Medium | Containerized deployments |

### 1. Discord Setup

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application
3. Go to "Bot" tab and copy your token
4. Invite bot with URL Generator (see [SETUP_GUIDE.md](SETUP_GUIDE.md))

### 2. Local Setup

```bash
# Clone the repository
git clone <repository-url>
cd astra

# Install dependencies
pip install -e ".[dev]"

# Copy environment template
cp .env.example .env

# Edit .env with your Discord bot token
# DISCORD_TOKEN=your_token_here
```

## Configuration

Create a `.env` file (see [SETUP_GUIDE.md](SETUP_GUIDE.md) for how to get these values):

```env
DISCORD_TOKEN=your_bot_token_here
DISCORD_APPLICATION_ID=your_application_id
LOG_LEVEL=INFO
```

## Running the Bot

```bash
# Run the bot
python -m astra
```

**Need help setting up?** See [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed Discord Developer Portal instructions.

### Pterodactyl Deployment

See [PTERODACTYL.md](PTERODACTYL.md) for complete Pterodactyl panel deployment instructions.

Quick steps:
1. Import `egg-astra.json` into your Pterodactyl panel
2. Create a server with the Astra egg
3. Set your `DISCORD_TOKEN` environment variable
4. Start the server

### Docker Deployment

```bash
# Pull pre-built image
docker pull ghcr.io/mystiatech/astra:latest

# Run with your token
docker run -e DISCORD_TOKEN=your_token_here ghcr.io/mystiatech/astra:latest
```

Or build locally:
```bash
docker build -t astra .
docker run -e DISCORD_TOKEN=your_token_here astra
```

## Required Bot Permissions

When inviting Astra to your server, use these settings:

**OAuth2 Scopes:** `bot`, `applications.commands`

**Bot Permissions:**
- ✅ Send Messages
- ✅ Embed Links  
- ✅ Attach Files
- ✅ Read Messages/View Channels

No admin permissions needed! Astra only responds to slash commands.

## Slash Commands

### Tarot Readings

| Command | Description | Cards | Difficulty |
|---------|-------------|-------|------------|
| `/tarot-single` | Quick single card guidance | 1 | Beginner |
| `/tarot-three` | Past, Present, Future | 3 | Beginner |
| `/tarot-mind-body-spirit` | Holistic self-examination | 3 | Beginner |
| `/tarot-situation-action` | Problem-solving spread | 3 | Beginner |
| `/tarot-relationship` | Relationship dynamics | 7 | Intermediate |
| `/tarot-career` | Career guidance | 5 | Intermediate |
| `/tarot-celtic` | Full Celtic Cross | 10 | Advanced |

### Theme Commands

| Command | Description |
|---------|-------------|
| `/tarot-theme` | Select your card deck theme |
| `/tarot-themes` | Browse all available themes |
| `/tarot-my-theme` | Check your current theme |
| `/tarot-theme-preview` | Preview a specific theme |
| `/tarot-theme-help` | Learn about themes |

### Utility Commands

| Command | Description |
|---------|-------------|
| `/tarot-spreads` | Learn about all spreads |
| `/tarot-help` | Get help and tips |
| `/tarot-cancel` | Cancel your reading |

## Single Session Design

Astra serves **one user at a time** to ensure each reading receives full attention. If someone is mid-reading, others will see:

> "🔮 Astra is Currently With Another Seeker"

Sessions automatically expire after 5 minutes of inactivity.

## Theme System 🎨

Astra features a powerful **dynamic theme system** that allows multiple card decks:

### For Users

- **First-time selection**: On your first reading, choose a theme that resonates
- **Easy switching**: Use `/tarot-theme` anytime to change decks
- **Personal preference**: Each user can have their own theme

### For Server Admins

- **Drop-in themes**: Add new decks by placing folders in `themes/` (top-level folder)
- **Auto-detection**: New themes appear automatically (no restart needed!)
- **Hot-reload**: Changes to themes are detected instantly

### Creating a Theme

1. Create a folder in `themes/` (e.g., `my_theme/`)
2. Add your 78 card images following the naming convention
3. Create a `theme.json` metadata file
4. Done! Astra will detect it within seconds

See [THEME_GUIDE.md](themes/THEME_GUIDE.md) for complete documentation.

### Theme Folder Structure

```
themes/                         # ⭐ Top-level folder - easy access!
├── default/                    # Built-in default theme
│   ├── theme.json
│   ├── major_00.png
│   ├── major_01.png
│   └── ... (all 78 cards)
│
├── celestial/                  # Your custom theme
│   ├── theme.json
│   ├── major_00.png
│   └── ...
│
└── neon_future/               # Another custom theme
    ├── theme.json
    └── ...
```

### Example theme.json

```json
{
  "name": "Celestial Dreams",
  "description": "A mystical theme featuring cosmic imagery",
  "author": "Your Name",
  "version": "1.0.0",
  "card_format": "{suit}_{number}.png",
  "supports_reversed": true,
  "preview_image": "preview.png"
}
```

## Project Structure

```
astra/
├── src/astra/
│   ├── __init__.py
│   ├── __main__.py              # Entry point
│   ├── bot.py                   # Discord bot (Emma)
│   ├── reading.py               # Reading models (Emma)
│   ├── embeds.py                # Discord embeds (Olivia)
│   ├── themes.py                # Theme manager (Emma)
│   ├── theme_embeds.py          # Theme UI (Olivia)
│   ├── theme_commands.py        # Theme commands (Emma)
│   └── data/
│       ├── __init__.py
│       ├── cards.py             # 78 tarot cards (Sarah)
│       └── spreads.py           # Spread definitions (Sarah)
├── tests/                       # Test suite (Chloe)
├── themes/                      # 🎨 Card themes - EASY TO ADD!
│   ├── default/                 # Built-in theme
│   ├── my_custom_theme/         # Drop your themes here
│   └── THEME_GUIDE.md           # How to create themes
├── assets/
│   └── cover_art/               # Bot artwork (Maya)
├── pyproject.toml
├── .env.example
└── README.md
```

## Tarot Data Validation

All 78 cards have been researched and validated by Sarah:

- **Major Arcana**: 22 cards (The Fool 0 - The World 21)
- **Wands**: 14 cards (Fire - creativity, action, passion)
- **Cups**: 14 cards (Water - emotions, relationships, intuition)
- **Swords**: 14 cards (Air - intellect, conflict, decisions)
- **Pentacles**: 14 cards (Earth - material world, finances)

Each card includes:
- Upright and reversed meanings
- Keywords for quick reference
- Elemental and astrological associations
- Image placeholder reference

Sources consulted:
- Rider-Waite-Smith tradition
- *Seventy-Eight Degrees of Wisdom* by Rachel Pollack
- *The Ultimate Guide to Tarot* by Liz Dean
- *Learning the Tarot* by Joan Bunning

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=astra

# Run specific test file
pytest tests/test_cards.py

# Run theme tests
pytest tests/test_themes.py
```

## Cover Art Variants

Maya has designed several cover art themes in `assets/cover_art/`:

- `astra_primary.png` - Main mystical theme
- `astra_celestial.png` - Starry cosmos
- `astra_mystic_moon.png` - Lunar magic
- `astra_woodland.png` - Forest witch
- `astra_art_deco.png` - 1920s elegance
- `astra_minimal.png` - Clean modern
- `astra_neon.png` - Cyberpunk
- `astra_autumn.png` - Fall harvest
- `astra_winter.png` - Snow and ice

## License

This project is for educational purposes. Tarot card meanings are based on traditional interpretations.

---

🔮 *May the stars guide your path* 🌟
