# Astra Cover Art Variants
==========================
DESIGN BY: Maya (Assets Lead)

This directory contains alternate cover/banner art for Astra.
These can be used for:
- Bot profile pictures
- Server banners
- Promotional materials
- Seasonal themes

## Primary Cover Art

### `astra_primary.png`
The main bot avatar - mystical feminine figure with celestial elements.

**Design Elements:**
- Deep purple/midnight blue background
- Silver crescent moon
- Star constellation patterns
- Crystal ball or tarot cards in hands
- Flowing robes with subtle shimmer

## Alternate Variants

### `astra_celestial.png`
**Theme:** Starry cosmos and astronomy
- Deep space background with nebula
- Golden astrological symbols
- Zodiac wheel elements
- Cosmic energy streams

### `astra_mystic_moon.png`
**Theme:** Lunar phases and moon magic
- Phases of the moon as border
- Indigo and silver color scheme
- Moonflower or night-blooming elements
- Reflections in water

### `astra_woodland.png`
**Theme:** Forest witch aesthetic
- Deep forest greens
- Moss and mushroom elements
- Owl or raven companion
- Natural crystals
- Wooden tarot box

### `astra_art_deco.png`
**Theme:** 1920s art deco elegance
- Gold and black color scheme
- Geometric patterns
- Sunburst motifs
- Stylized figure
- Gilded frame elements

### `astra_minimal.png`
**Theme:** Clean modern design
- Single line art style
- White or light background
- Simple crystal ball or eye symbol
- Modern typography
- Subtle gradient

### `astra_neon.png`
**Theme:** Cyberpunk/futuristic
- Neon purple and cyan
- Digital glitch effects
- Holographic cards
- Circuit patterns
- Futuristic setting

### `astra_autumn.png`
**Theme:** Fall harvest and change
- Orange, red, gold palette
- Falling leaves
- Pumpkin or apple elements
- Cozy sweater aesthetic
- Warm lighting

### `astra_winter.png`
**Theme:** Snow and introspection
- Ice blue and white
- Snowflakes
- Bare branches
- Candle light
- Fuzzy textures

## Technical Specifications

### Bot Avatar
- **Size:** 512x512 pixels (Discord requirement)
- **Format:** PNG
- **Style:** Recognizable at small sizes
- **Background:** Transparent or solid

### Server Banner
- **Size:** 960x540 pixels
- **Format:** PNG or JPG
- **Safe zone:** Keep important elements center 800x420

### Promotional
- **Size:** 1920x1080 pixels (16:9)
- **Format:** PNG or JPG
- **Include:** Bot name, tagline, key features

## Usage Guide

To change the bot's avatar:
```python
# In bot setup or via command
with open('assets/cover_art/astra_variant.png', 'rb') as f:
    await bot.user.edit(avatar=f.read())
```

To set seasonal themes:
```python
# Check date and set appropriate theme
import datetime
month = datetime.now().month
if month in [9, 10, 11]:  # Autumn
    theme = "autumn"
elif month in [12, 1, 2]:  # Winter
    theme = "winter"
# etc.
```
