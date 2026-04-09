# Team Assignments - Astra Tarot Bot

## Overview

This document outlines the work assignments for the Astra Discord bot project. Each team lead has specific responsibilities and deliverables.

---

## 👩‍💼 Kimi (Project Lead / You)

**Role:** Project Lead, System Architect, Integration

**Responsibilities:**
- Overall project coordination
- System architecture design
- Code review and standards
- Final integration and deployment
- Documentation oversight

**Deliverables:**
- [x] Project structure and scaffolding
- [x] Team coordination and assignments
- [x] Architecture documentation
- [x] Final integration testing

---

## 📚 Sarah (Research Lead)

**Role:** Tarot Research Specialist, Data Validation

**Expertise:** Esoteric studies, tarot history, symbolism

**Responsibilities:**
- Research all 78 tarot card meanings
- Verify accuracy of upright and reversed interpretations
- Define spread layouts and position meanings
- Document astrological and elemental associations
- Cross-reference multiple authoritative sources

**Deliverables:**
- [x] Complete 78-card database with accurate meanings (`data/cards.py`)
  - Major Arcana (22 cards)
  - Minor Arcana - Wands (14 cards)
  - Minor Arcana - Cups (14 cards)
  - Minor Arcana - Swords (14 cards)
  - Minor Arcana - Pentacles (14 cards)
- [x] Spread definitions (`data/spreads.py`)
  - Single Card
  - Three Card (Past-Present-Future)
  - Mind-Body-Spirit
  - Situation-Action-Outcome
  - Celtic Cross (10 cards)
  - Relationship Spread (7 cards)
  - Career Path Spread (5 cards)
- [x] Theme system documentation (`themes/THEME_GUIDE.md`)
  - Complete card naming reference
  - 78-card filename mapping
  - theme.json specification
  - Reversed card guidelines

**Sources Used:**
- Rider-Waite-Smith deck tradition
- "Seventy-Eight Degrees of Wisdom" - Rachel Pollack
- "The Ultimate Guide to Tarot" - Liz Dean
- "Learning the Tarot" - Joan Bunning

---

## 💻 Emma (Backend Lead)

**Role:** Backend Engineer, Discord Integration

**Expertise:** Python, discord.py, async programming

**Responsibilities:**
- Implement Discord bot framework
- Create slash command handlers
- Implement session management (one user at a time)
- Card drawing and randomization logic
- Reading session lifecycle management

**Deliverables:**
- [x] Bot core (`bot.py`)
  - AstraBot class with session management
  - Slash command registration
  - Session acquisition/release logic
  - Error handling
- [x] TarotCommands cog with all slash commands:
  - `/tarot-single`
  - `/tarot-three`
  - `/tarot-mind-body-spirit`
  - `/tarot-situation-action`
  - `/tarot-relationship`
  - `/tarot-career`
  - `/tarot-celtic`
  - `/tarot-spreads`
  - `/tarot-help`
  - `/tarot-cancel`
- [x] Reading models (`reading.py`)
  - Reading dataclass
  - ReadingResult dataclass
  - ReadingSession dataclass

**Key Implementation Details:**
- Single session lock using asyncio.Lock
- 5-minute session timeout
- Proper session cleanup on completion/error

**Theme System (NEW):**
- [x] Theme manager (`themes.py`)
  - Hot-reload with file watching
  - User preference storage
  - Auto-discovery of new themes
  - Fallback to default theme
- [x] Theme commands (`theme_commands.py`)
  - `/tarot-theme` - Interactive selection
  - `/tarot-themes` - Browse themes
  - `/tarot-my-theme` - Check current theme
  - `/tarot-theme-preview` - Preview themes
  - First-time theme prompt integration

---

## 🎨 Olivia (UX/Frontend Lead)

**Role:** User Experience Designer, Embed Specialist

**Expertise:** Discord embeds, visual design, user flows

**Responsibilities:**
- Design Discord embed layouts
- Create card display formatting
- Implement reading summary generation
- Design color schemes and visual hierarchy
- Ensure readable and beautiful output

**Deliverables:**
- [x] Embed creation module (`embeds.py`)
  - `create_reading_embed()` - Main reading display
  - `create_spread_info_embed()` - Spread catalog
  - `create_help_embed()` - Help documentation
  - `create_card_detail_embed()` - Individual card view
- [x] Visual design elements:
  - Color palette for suits (Purple, Gold, Orange, Blue, Silver, Green)
  - Emoji associations for suits
  - Position number emojis (1️⃣-🔟)
  - Reading summary generation
  - Elemental balance interpretation

**Design Decisions:**
- Major Arcana: Gold (#F1C40F)
- Wands (Fire): Orange (#E67E22)
- Cups (Water): Blue (#3498DB)
- Swords (Air): Silver (#95A5A6)
- Pentacles (Earth): Green (#27AE60)
- Primary accent: Mystic Purple (#9B59B6)
- Reversed indicator: Red (#E74C3C)

**Theme System UI (NEW):**
- [x] Theme embeds (`theme_embeds.py`)
  - `create_theme_selection_embed()` - First-time selection
  - `create_theme_selected_embed()` - Confirmation
  - `create_theme_list_embed()` - Theme catalog
  - `create_theme_preview_embed()` - Theme details
  - `create_theme_help_embed()` - Theme help
- [x] Interactive theme selection with dropdown menus
- [x] Visual theme preview cards
- Reversed indicator: Red (#E74C3C)

---

## 🖼️ Maya (Assets Lead)

**Role:** Graphic Designer, Asset Manager

**Expertise:** Digital art, image processing, branding

**Responsibilities:**
- Create placeholder card images
- Design bot avatar/cover art variants
- Establish image naming conventions
- Create asset documentation
- Generate placeholder generation script

**Deliverables:**
- [x] Card placeholder documentation (`assets/cards/PLACEHOLDER_INFO.md`)
  - Naming convention specification
  - Image size requirements (300x500px)
  - Replacement instructions
- [x] Placeholder generator script (`assets/cards/generate_placeholders.py`)
  - Generates 78 placeholder images
  - Suit-colored borders
  - Card names and numbers
- [x] Cover art variants documentation (`assets/cover_art/COVER_ART_VARIANTS.md`)
  - Primary mystical theme
  - Celestial (starry cosmos)
  - Mystic Moon (lunar phases)
  - Woodland (forest witch)
  - Art Deco (1920s elegance)
  - Minimal (clean modern)
  - Neon (cyberpunk)
  - Autumn (fall harvest)
  - Winter (snow/ice)

**Technical Specifications:**
- Card images: 300x500px PNG
- Bot avatar: 512x512px PNG
- Server banner: 960x540px PNG/JPG
- Promotional: 1920x1080px PNG/JPG

**Theme System Assets (NEW):**
- [x] Theme folder structure documentation (`themes/THEME_GUIDE.md`)
  - Naming conventions for all 78 cards
  - theme.json specification
  - Reversed card support
  - Folder structure examples
  - Image format specifications
- [x] Default theme metadata (`themes/default/theme.json`)
  - Classic Rider-Waite description
  - Version and author info
  - Style tags and colors

---

## 🧪 Chloe (QA Lead)

**Role:** Quality Assurance Engineer, Test Specialist

**Expertise:** Test automation, edge case analysis, validation

**Responsibilities:**
- Write comprehensive test suite
- Validate tarot data accuracy
- Test session management logic
- Verify card drawing randomization
- Test Discord integration
- Document test coverage

**Deliverables:**
- [x] Test configuration (`tests/conftest.py`)
  - Fixtures for deck and spreads
  - Card filtering fixtures
- [x] Card data tests (`tests/test_cards.py`)
  - DECK-001 through DECK-004: Deck integrity
  - CARD-001 through CARD-004: Card structure
  - MAJOR-001 through MAJOR-003: Major Arcana validation
  - MINOR-001 through MINOR-003: Minor Arcana validation
  - MEANING-001 through MEANING-004: Meaning accuracy
  - DISPLAY-001 through DISPLAY-003: Display formatting
  - RESEARCH-001 through RESEARCH-002: Source validation
- [x] Spread tests (`tests/test_spreads.py`)
  - SPREAD-REG-001 through SPREAD-REG-002: Registry validation
  - SINGLE-001 through SINGLE-002: Single card spread
  - THREE-001 through THREE-002: Three card spread
  - CELTIC-001 through CELTIC-003: Celtic Cross
  - REL-001 through REL-002: Relationship spread
  - CAREER-001 through CAREER-002: Career spread
  - DOC-001 through DOC-003: Documentation quality
- [x] Bot logic tests (`tests/test_bot.py`)
  - SESSION-001 through SESSION-004: Session management
  - DRAW-001 through DRAW-004: Card drawing
  - MODEL-001 through MODEL-002: Data models
  - ERROR-001: Error handling
  - CMD-001: Command existence
- [x] Integration tests (`tests/test_integration.py`)
  - FLOW-001 through FLOW-002: Complete user flows
  - EMBED-001: Embed generation
  - CONSISTENCY-001 through CONSISTENCY-002: Data consistency
  - PERF-001: Performance testing
  - SEC-001: Security validation

**Theme System Tests (NEW):**
- [x] Theme tests (`tests/test_themes.py`)
  - THEME-001 through THEME-005: Theme structure
  - MGR-001 through MGR-005: Theme manager
  - DISCOVER-001 through DISCOVER-002: Theme discovery
  - LOOKUP-001 through LOOKUP-003: Card image lookup
  - NAMING-001 through NAMING-002: Naming conventions
  - EDGE-001 through EDGE-003: Edge cases
  - STATS-001: Statistics tracking

**Test Coverage Areas:**
- Data integrity: 100% of cards and spreads
- Session management: All states and transitions
- Card drawing: Randomization, no duplicates
- Command handling: All slash commands
- Theme system: Discovery, preferences, hot-reload
- Edge cases: Expired sessions, errors, timeouts

---

## Work Completed Summary

| Component | Assigned To | Status | Files |
|-----------|-------------|--------|-------|
| Project Structure | Kimi | ✅ Complete | All directories |
| Tarot Card Data | Sarah | ✅ Complete | `data/cards.py` (54KB) |
| Spread Definitions | Sarah | ✅ Complete | `data/spreads.py` (15KB) |
| Bot Framework | Emma | ✅ Complete | `bot.py`, `reading.py` |
| Slash Commands | Emma | ✅ Complete | 10 commands implemented |
| Session Management | Emma | ✅ Complete | Single-user constraint |
| **Theme System** | **Emma** | **✅ Complete** | **`themes.py` (14KB)** |
| **Theme Commands** | **Emma** | **✅ Complete** | **`theme_commands.py` (9KB)** |
| Discord Embeds | Olivia | ✅ Complete | `embeds.py` (13KB) |
| **Theme UI** | **Olivia** | **✅ Complete** | **`theme_embeds.py` (6KB)** |
| Visual Design | Olivia | ✅ Complete | Color palette, emojis |
| Placeholder System | Maya | ✅ Complete | Generator script + docs |
| Cover Art Specs | Maya | ✅ Complete | 9 theme variants |
| **Theme Structure** | **Maya** | **✅ Complete** | **`themes/` (top-level)** |
| Test Suite | Chloe | ✅ Complete | 50+ test cases |
| **Theme Tests** | **Chloe** | **✅ Complete** | **`test_themes.py`** |
| Documentation | Team | ✅ Complete | README, this file |

---

## Next Steps (If Continuing)

1. **Deployment:** Set up Discord application, get token, deploy bot
2. **Card Images:** Replace placeholders with actual tarot artwork
3. **Cover Art:** Create actual avatar images from Maya's designs
4. **User Testing:** Beta test with real Discord users
5. **Analytics:** Add reading statistics tracking (opt-in)
6. **Localization:** Translate to other languages
7. **Advanced Features:** Save readings, reading history, favorites
