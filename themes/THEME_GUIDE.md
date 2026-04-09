# Astra Theme System Guide
============================
DOCUMENTATION BY: Sarah & Maya

This guide explains how to create and add custom tarot themes to Astra.

## Quick Start

1. Create a new folder in `themes/` (top-level folder)
2. Add your card images
3. Create a `theme.json` file
4. Done! Astra will detect it automatically

## Folder Structure

```
themes/                       # Top-level themes folder (easy access!)
├── default/                   # Built-in default theme
│   ├── theme.json
│   ├── major_00.png           # The Fool
│   ├── major_01.png           # The Magician
│   ├── ...
│   ├── wands_01.png           # Ace of Wands
│   ├── wands_02.png           # Two of Wands
│   ├── ...
│   ├── cups_01.png            # Ace of Cups
│   ├── ...
│   ├── swords_01.png          # Ace of Swords
│   ├── ...
│   ├── pentacles_01.png       # Ace of Pentacles
│   └── ...
│
├── celestial/                  # Your custom theme
│   ├── theme.json
│   ├── major_00.png
│   ├── major_01.png
│   └── ... (all 78 cards)
│
└── neon_future/               # Another custom theme
    ├── theme.json
    ├── major_00.png
    └── ...
```

## Theme Metadata (theme.json)

```json
{
  "name": "Celestial Dreams",
  "description": "A mystical theme featuring cosmic imagery and starlight",
  "author": "Your Name",
  "version": "1.0.0",
  "card_format": "{suit}_{number}.png",
  "supports_reversed": false,
  "preview_image": "preview.png",
  "is_default": false,
  "extra": {
    "style": "cosmic",
    "colors": ["indigo", "gold", "silver"],
    "inspired_by": "Night sky photography"
  }
}
```

### Field Reference

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Display name for users |
| `description` | Yes | Short description of the theme |
| `author` | Yes | Creator name |
| `version` | Yes | Theme version (semver) |
| `card_format` | No | Filename format (default: `{suit}_{number}.png`) |
| `supports_reversed` | No | Has unique reversed card images (default: false) |
| `preview_image` | No | Preview/thumbnail filename |
| `is_default` | No | Whether this is the default theme (default: false) |
| `extra` | No | Additional metadata (style, colors, etc.) |

## Card Naming Formats

### Standard Format (default)

```
{suite}_{number}.png
```

Examples:
- `major_00.png` - The Fool
- `major_13.png` - Death
- `wands_01.png` - Ace of Wands
- `wands_11.png` - Page of Wands
- `cups_14.png` - King of Cups

## Full Card Reference

### Major Arcana (0-21)

| Number | Card | Filename |
|--------|------|----------|
| 00 | The Fool | `major_00.png` |
| 01 | The Magician | `major_01.png` |
| 02 | The High Priestess | `major_02.png` |
| 03 | The Empress | `major_03.png` |
| 04 | The Emperor | `major_04.png` |
| 05 | The Hierophant | `major_05.png` |
| 06 | The Lovers | `major_06.png` |
| 07 | The Chariot | `major_07.png` |
| 08 | Strength | `major_08.png` |
| 09 | The Hermit | `major_09.png` |
| 10 | Wheel of Fortune | `major_10.png` |
| 11 | Justice | `major_11.png` |
| 12 | The Hanged Man | `major_12.png` |
| 13 | Death | `major_13.png` |
| 14 | Temperance | `major_14.png` |
| 15 | The Devil | `major_15.png` |
| 16 | The Tower | `major_16.png` |
| 17 | The Star | `major_17.png` |
| 18 | The Moon | `major_18.png` |
| 19 | The Sun | `major_19.png` |
| 20 | Judgement | `major_20.png` |
| 21 | The World | `major_21.png` |

### Minor Arcana - Wands (14 cards)

| # | Card | Filename |
|---|------|----------|
| 1 | Ace of Wands | `wands_01.png` |
| 2 | Two of Wands | `wands_02.png` |
| 3 | Three of Wands | `wands_03.png` |
| 4 | Four of Wands | `wands_04.png` |
| 5 | Five of Wands | `wands_05.png` |
| 6 | Six of Wands | `wands_06.png` |
| 7 | Seven of Wands | `wands_07.png` |
| 8 | Eight of Wands | `wands_08.png` |
| 9 | Nine of Wands | `wands_09.png` |
| 10 | Ten of Wands | `wands_10.png` |
| 11 | Page of Wands | `wands_11.png` |
| 12 | Knight of Wands | `wands_12.png` |
| 13 | Queen of Wands | `wands_13.png` |
| 14 | King of Wands | `wands_14.png` |

### Minor Arcana - Cups (14 cards)

| # | Card | Filename |
|---|------|----------|
| 1 | Ace of Cups | `cups_01.png` |
| 2-10 | Number cards | `cups_02.png` - `cups_10.png` |
| 11 | Page of Cups | `cups_11.png` |
| 12 | Knight of Cups | `cups_12.png` |
| 13 | Queen of Cups | `cups_13.png` |
| 14 | King of Cups | `cups_14.png` |

### Minor Arcana - Swords (14 cards)

| # | Card | Filename |
|---|------|----------|
| 1 | Ace of Swords | `swords_01.png` |
| 2-10 | Number cards | `swords_02.png` - `swords_10.png` |
| 11 | Page of Swords | `swords_11.png` |
| 12 | Knight of Swords | `swords_12.png` |
| 13 | Queen of Swords | `swords_13.png` |
| 14 | King of Swords | `swords_14.png` |

### Minor Arcana - Pentacles (14 cards)

| # | Card | Filename |
|---|------|----------|
| 1 | Ace of Pentacles | `pentacles_01.png` |
| 2-10 | Number cards | `pentacles_02.png` - `pentacles_10.png` |
| 11 | Page of Pentacles | `pentacles_11.png` |
| 12 | Knight of Pentacles | `pentacles_12.png` |
| 13 | Queen of Pentacles | `pentacles_13.png` |
| 14 | King of Pentacles | `pentacles_14.png` |

## Reversed Card Support

If your theme includes unique artwork for reversed cards:

1. Set `"supports_reversed": true` in theme.json
2. Name reversed cards with `_reversed` suffix:
   - `major_00.png` (upright)
   - `major_00_reversed.png` (reversed)

Astra will automatically use reversed images when appropriate.

## Image Specifications

### Recommended
- **Format:** PNG (transparency supported)
- **Size:** 300x500 pixels (3:5 aspect ratio)
- **Resolution:** 72-150 DPI
- **Color Space:** RGB

### Minimum
- **Size:** 150x250 pixels
- **Format:** PNG or JPG

### File Size
- Keep cards under 500KB each
- Total theme under 40MB

## Testing Your Theme

1. Place theme folder in `themes/` (top-level folder)
2. Astra detects it automatically (hot-reload)
3. Use `/tarot-themes` to see it in the list
4. Use `/tarot-theme` to select it
5. Test with `/tarot-three`

Happy theming! 🎨🔮
