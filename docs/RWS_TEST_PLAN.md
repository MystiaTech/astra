# Rider-Waite-Smith (RWS) Classic Deck Test Plan

**QA Lead:** Chloe  
**Test Plan Version:** 1.0  
**Created:** 2026-04-09  
**Target:** Classic Rider-Waite deck integration validation

---

## Overview

This test plan covers comprehensive testing of the classic Rider-Waite-Smith (RWS) tarot deck integration for Astra Tarot Bot. The classic theme will provide 78 authentic Pamela Colman Smith illustrations from the original 1909 deck.

**Test Scope:**
- All 78 card images (22 Major Arcana + 56 Minor Arcana)
- Theme system integration
- Spread display functionality
- Journal integration
- Performance and edge cases

---

## Test Environment Setup

### Prerequisites

```bash
# 1. Ensure classic theme directory exists
ls -la themes/classic/

# 2. Verify theme.json is configured
cat themes/classic/theme.json

# 3. Run image verification script
python scripts/verify_rws_images.py

# 4. Ensure bot is running for Discord integration tests
# (For manual testing)
```

### Required Test Files

| File | Purpose | Location |
|------|---------|----------|
| `themes/classic/theme.json` | Theme configuration | `themes/classic/` |
| 78 card images | Card artwork | `themes/classic/` |
| `scripts/verify_rws_images.py` | Image validation | `scripts/` |
| `data/user_themes.json` | User preferences | `data/` |

### Test Accounts

- **Test User 1:** For theme selection tests
- **Test User 2:** For journal integration tests
- **Admin User:** For system verification

---

## Test Checklists

### 1. Image Tests

#### 1.1 Major Arcana Display (22 Cards)

| # | Card Name | Filename | Status | Notes |
|---|-----------|----------|--------|-------|
| 0 | The Fool | `major_00_the_fool.png` | [ ] | |
| 1 | The Magician | `major_01_the_magician.png` | [ ] | |
| 2 | The High Priestess | `major_02_the_high_priestess.png` | [ ] | |
| 3 | The Empress | `major_03_the_empress.png` | [ ] | |
| 4 | The Emperor | `major_04_the_emperor.png` | [ ] | |
| 5 | The Hierophant | `major_05_the_hierophant.png` | [ ] | |
| 6 | The Lovers | `major_06_the_lovers.png` | [ ] | |
| 7 | The Chariot | `major_07_the_chariot.png` | [ ] | |
| 8 | Strength | `major_08_strength.png` | [ ] | |
| 9 | The Hermit | `major_09_the_hermit.png` | [ ] | |
| 10 | Wheel of Fortune | `major_10_wheel_of_fortune.png` | [ ] | |
| 11 | Justice | `major_11_justice.png` | [ ] | |
| 12 | The Hanged Man | `major_12_the_hanged_man.png` | [ ] | |
| 13 | Death | `major_13_death.png` | [ ] | |
| 14 | Temperance | `major_14_temperance.png` | [ ] | |
| 15 | The Devil | `major_15_the_devil.png` | [ ] | |
| 16 | The Tower | `major_16_the_tower.png` | [ ] | |
| 17 | The Star | `major_17_the_star.png` | [ ] | |
| 18 | The Moon | `major_18_the_moon.png` | [ ] | |
| 19 | The Sun | `major_19_the_sun.png` | [ ] | |
| 20 | Judgement | `major_20_judgement.png` | [ ] | |
| 21 | The World | `major_21_the_world.png` | [ ] | |

**Test Steps:**
1. [ ] Run `/tarot-single` until each Major Arcana card appears
2. [ ] Verify image displays correctly in Discord embed
3. [ ] Check image is not stretched or distorted
4. [ ] Verify image loads in under 2 seconds
5. [ ] Confirm card name matches image

#### 1.2 Minor Arcana - Wands (14 Cards)

| # | Card Name | Filename | Status | Notes |
|---|-----------|----------|--------|-------|
| 1 | Ace of Wands | `wands_01_ace.png` | [ ] | |
| 2 | Two of Wands | `wands_02.png` | [ ] | |
| 3 | Three of Wands | `wands_03.png` | [ ] | |
| 4 | Four of Wands | `wands_04.png` | [ ] | |
| 5 | Five of Wands | `wands_05.png` | [ ] | |
| 6 | Six of Wands | `wands_06.png` | [ ] | |
| 7 | Seven of Wands | `wands_07.png` | [ ] | |
| 8 | Eight of Wands | `wands_08.png` | [ ] | |
| 9 | Nine of Wands | `wands_09.png` | [ ] | |
| 10 | Ten of Wands | `wands_10.png` | [ ] | |
| 11 | Page of Wands | `wands_11_page.png` | [ ] | |
| 12 | Knight of Wands | `wands_12_knight.png` | [ ] | |
| 13 | Queen of Wands | `wands_13_queen.png` | [ ] | |
| 14 | King of Wands | `wands_14_king.png` | [ ] | |

#### 1.3 Minor Arcana - Cups (14 Cards)

| # | Card Name | Filename | Status | Notes |
|---|-----------|----------|--------|-------|
| 1 | Ace of Cups | `cups_01_ace.png` | [ ] | |
| 2 | Two of Cups | `cups_02.png` | [ ] | |
| 3 | Three of Cups | `cups_03.png` | [ ] | |
| 4 | Four of Cups | `cups_04.png` | [ ] | |
| 5 | Five of Cups | `cups_05.png` | [ ] | |
| 6 | Six of Cups | `cups_06.png` | [ ] | |
| 7 | Seven of Cups | `cups_07.png` | [ ] | |
| 8 | Eight of Cups | `cups_08.png` | [ ] | |
| 9 | Nine of Cups | `cups_09.png` | [ ] | |
| 10 | Ten of Cups | `cups_10.png` | [ ] | |
| 11 | Page of Cups | `cups_11_page.png` | [ ] | |
| 12 | Knight of Cups | `cups_12_knight.png` | [ ] | |
| 13 | Queen of Cups | `cups_13_queen.png` | [ ] | |
| 14 | King of Cups | `cups_14_king.png` | [ ] | |

#### 1.4 Minor Arcana - Swords (14 Cards)

| # | Card Name | Filename | Status | Notes |
|---|-----------|----------|--------|-------|
| 1 | Ace of Swords | `swords_01_ace.png` | [ ] | |
| 2 | Two of Swords | `swords_02.png` | [ ] | |
| 3 | Three of Swords | `swords_03.png` | [ ] | |
| 4 | Four of Swords | `swords_04.png` | [ ] | |
| 5 | Five of Swords | `swords_05.png` | [ ] | |
| 6 | Six of Swords | `swords_06.png` | [ ] | |
| 7 | Seven of Swords | `swords_07.png` | [ ] | |
| 8 | Eight of Swords | `swords_08.png` | [ ] | |
| 9 | Nine of Swords | `swords_09.png` | [ ] | |
| 10 | Ten of Swords | `swords_10.png` | [ ] | |
| 11 | Page of Swords | `swords_11_page.png` | [ ] | |
| 12 | Knight of Swords | `swords_12_knight.png` | [ ] | |
| 13 | Queen of Swords | `swords_13_queen.png` | [ ] | |
| 14 | King of Swords | `swords_14_king.png` | [ ] | |

#### 1.5 Minor Arcana - Pentacles (14 Cards)

| # | Card Name | Filename | Status | Notes |
|---|-----------|----------|--------|-------|
| 1 | Ace of Pentacles | `pentacles_01_ace.png` | [ ] | |
| 2 | Two of Pentacles | `pentacles_02.png` | [ ] | |
| 3 | Three of Pentacles | `pentacles_03.png` | [ ] | |
| 4 | Four of Pentacles | `pentacles_04.png` | [ ] | |
| 5 | Five of Pentacles | `pentacles_05.png` | [ ] | |
| 6 | Six of Pentacles | `pentacles_06.png` | [ ] | |
| 7 | Seven of Pentacles | `pentacles_07.png` | [ ] | |
| 8 | Eight of Pentacles | `pentacles_08.png` | [ ] | |
| 9 | Nine of Pentacles | `pentacles_09.png` | [ ] | |
| 10 | Ten of Pentacles | `pentacles_10.png` | [ ] | |
| 11 | Page of Pentacles | `pentacles_11_page.png` | [ ] | |
| 12 | Knight of Pentacles | `pentacles_12_knight.png` | [ ] | |
| 13 | Queen of Pentacles | `pentacles_13_queen.png` | [ ] | |
| 14 | King of Pentacles | `pentacles_14_king.png` | [ ] | |

**Image Quality Tests:**

- [ ] All 78 card images exist in `themes/classic/`
- [ ] No images are 0 bytes
- [ ] All images are PNG format
- [ ] Image dimensions are consistent (300x500 pixels minimum)
- [ ] Aspect ratio is 2:3 (tarot standard)
- [ ] Images load in under 2 seconds on average connection
- [ ] Images are not stretched or distorted in Discord embeds
- [ ] Colors render correctly (not washed out or oversaturated)

---

### 2. Theme Tests

#### 2.1 Theme Discovery

- [ ] Classic theme appears in `/tarot-themes` command
- [ ] Theme shows correct name: "Classic Rider-Waite"
- [ ] Theme shows correct description mentioning Pamela Colman Smith
- [ ] Theme displays author attribution
- [ ] Theme displays version number
- [ ] Theme shows "Standard" for reversed card support (not supported)

#### 2.2 Theme Selection

- [ ] User can select classic theme via `/tarot-theme`
- [ ] Selection confirmation shows correct theme name
- [ ] Selection confirmation shows theme description
- [ ] Theme preview image displays (if available)

#### 2.3 Theme Persistence

- [ ] Selected theme persists after bot restart
- [ ] Theme preference saved to `data/user_themes.json`
- [ ] User sees their selected theme with `/tarot-my-theme`

#### 2.4 Theme Switching

- [ ] Can switch from default to classic theme
- [ ] Can switch from classic to default theme
- [ ] Can switch between themes multiple times
- [ ] Theme change takes effect immediately for next reading

#### 2.5 Theme Configuration

Verify `themes/classic/theme.json`:

```json
{
  "name": "Classic Rider-Waite",
  "description": "Authentic Pamela Colman Smith illustrations from the original 1909 Rider-Waite-Smith deck",
  "author": "Pamela Colman Smith",
  "version": "1.0.0",
  "card_format": "{suit}_{number}.png",
  "supports_reversed": false,
  "is_default": false,
  "preview_image": "preview.png",
  "extra": {
    "artist": "Pamela Colman Smith",
    "year": "1909",
    "symbolism": "Golden Dawn tradition",
    "colors": ["gold", "blue", "red", "green"]
  }
}
```

---

### 3. Spread Tests

#### 3.1 Single Card Spread

- [ ] `/tarot-single` shows 1 RWS card
- [ ] Card displays in correct position
- [ ] Card image is from classic theme
- [ ] Card name displays correctly
- [ ] Keywords display correctly
- [ ] Meaning displays correctly

#### 3.2 Three Card Spread

- [ ] `/tarot-three` shows 3 RWS cards
- [ ] Position 1: Past - correct card displayed
- [ ] Position 2: Present - correct card displayed
- [ ] Position 3: Future - correct card displayed
- [ ] All card images are from classic theme
- [ ] Position labels display correctly

#### 3.3 Celtic Cross Spread (10 Cards)

- [ ] `/tarot-celtic` shows 10 RWS cards
- [ ] Position 1: Present Situation
- [ ] Position 2: Challenge/Cross
- [ ] Position 3: Foundation
- [ ] Position 4: Recent Past
- [ ] Position 5: Crown/Goal
- [ ] Position 6: Near Future
- [ ] Position 7: Self
- [ ] Position 8: Environment
- [ ] Position 9: Hopes & Fears
- [ ] Position 10: Outcome
- [ ] All card images are from classic theme
- [ ] All position meanings display correctly

#### 3.4 Other Spreads

- [ ] `/tarot-relationship` (7 cards) - all RWS images
- [ ] `/tarot-career` (5 cards) - all RWS images
- [ ] Mind-Body-Spirit spread (3 cards) - all RWS images
- [ ] Situation-Action-Outcome spread (3 cards) - all RWS images

---

### 4. Integration Tests

#### 4.1 Journal Integration

- [ ] Save to journal works with classic theme
- [ ] Saved reading shows correct card names
- [ ] Journal entry includes theme information
- [ ] Journal displays classic theme indicator
- [ ] Viewing saved reading shows correct card details
- [ ] Journal entry survives bot restart

#### 4.2 Attribution Display

- [ ] Reading embeds show Pamela Colman Smith attribution
- [ ] Theme selection shows artist credit
- [ ] `/tarot-theme-help` mentions RWS origins

#### 4.3 Reversed Cards

- [ ] Reversed cards display with "(Reversed)" label
- [ ] Reversed meaning displays correctly
- [ ] Image orientation is rotated 180° (since no reversed images exist)
- [ ] Reversed keywords display correctly

---

### 5. Performance Tests

#### 5.1 Image Loading Performance

- [ ] Single card image loads in < 2 seconds
- [ ] Three card spread loads in < 3 seconds
- [ ] Celtic Cross (10 cards) loads in < 5 seconds
- [ ] No timeout errors on image loading

#### 5.2 Memory Usage

- [ ] Bot memory usage remains stable
- [ ] No memory leaks during repeated readings
- [ ] Images are properly garbage collected

---

### 6. Edge Cases & Fallback Tests

#### 6.1 Missing Image Fallback

- [ ] If classic card image missing, falls back to default theme
- [ ] If no image available, shows text-only reading
- [ ] Error message is user-friendly
- [ ] Reading continues even if one image fails

#### 6.2 Corrupted Image Handling

- [ ] Corrupted/invalid image files don't crash the bot
- [ ] Error is logged for corrupted images
- [ ] User sees appropriate fallback

#### 6.3 Concurrent Users

- [ ] Multiple users can use classic theme simultaneously
- [ ] User A (classic) and User B (default) get correct themes
- [ ] Theme switching doesn't affect other users

#### 6.4 Theme Directory Changes

- [ ] Adding new card to classic theme is detected (hot reload)
- [ ] Removing card triggers fallback behavior
- [ ] Modifying theme.json updates display

---

## Automated Test Script

### Image Verification Script

Run the automated verification:

```bash
cd /home/mystiatech/projects/Astra/astra
python scripts/verify_rws_images.py
```

**Expected Output:**
```
=== Rider-Waite-Smith Image Verification ===
Checking themes/classic/ directory...

✓ themes/classic/theme.json exists
✓ Theme name: Classic Rider-Waite
✓ Theme author: Pamela Colman Smith

Major Arcana: 22/22 found ✓
Minor Arcana: 56/56 found ✓
  - Wands: 14/14 ✓
  - Cups: 14/14 ✓
  - Swords: 14/14 ✓
  - Pentacles: 14/14 ✓

Total: 78/78 images found ✓

File Size Check: All images > 0 bytes ✓
Naming Convention: All files follow pattern ✓

=== Summary ===
Status: PASSED ✓
All images ready for testing!
```

---

## Test Execution Schedule

### Phase 1: Pre-Testing (Day 1)
- [ ] Run automated image verification script
- [ ] Verify all 78 images present and valid
- [ ] Check theme.json configuration
- [ ] Set up test Discord server

### Phase 2: Automated Testing (Day 2)
- [ ] Run unit tests for theme system
- [ ] Run integration tests for card display
- [ ] Verify journal integration
- [ ] Generate test report

### Phase 3: Manual Testing (Day 3)
- [ ] Manual verification of all 22 Major Arcana
- [ ] Spot check Minor Arcana (10% sample)
- [ ] Test all spread types
- [ ] Test theme switching
- [ ] Test journal save/view

### Phase 4: Edge Case Testing (Day 4)
- [ ] Missing image scenarios
- [ ] Concurrent user testing
- [ ] Performance testing
- [ ] Long-running stability test

### Phase 5: Sign-off (Day 5)
- [ ] Review all test results
- [ ] Document any issues
- [ ] Obtain sign-off from stakeholders
- [ ] Prepare deployment checklist

---

## Test Results Template

### Summary

| Category | Tests | Passed | Failed | Status |
|----------|-------|--------|--------|--------|
| Image Tests | 78 | | | |
| Theme Tests | 15 | | | |
| Spread Tests | 25 | | | |
| Integration Tests | 12 | | | |
| Performance Tests | 5 | | | |
| Edge Cases | 10 | | | |
| **Total** | **145** | | | |

### Issues Found

| ID | Severity | Description | Steps to Reproduce | Expected | Actual | Status |
|----|----------|-------------|-------------------|----------|--------|--------|
| | | | | | | |

### Sign-off

- [ ] QA Lead (Chloe): _________________ Date: _______
- [ ] Backend Lead (Emma): _________________ Date: _______
- [ ] UX Lead (Olivia): _________________ Date: _______
- [ ] Project Lead (Kimi): _________________ Date: _______

---

## Appendix A: Card Reference

### Major Arcana Names
0. The Fool
1. The Magician
2. The High Priestess
3. The Empress
4. The Emperor
5. The Hierophant
6. The Lovers
7. The Chariot
8. Strength
9. The Hermit
10. Wheel of Fortune
11. Justice
12. The Hanged Man
13. Death
14. Temperance
15. The Devil
16. The Tower
17. The Star
18. The Moon
19. The Sun
20. Judgement
21. The World

### Minor Arcana Structure
- **Wands:** Fire suit (Ace through King)
- **Cups:** Water suit (Ace through King)
- **Swords:** Air suit (Ace through King)
- **Pentacles:** Earth suit (Ace through King)

---

## Appendix B: Naming Convention

### Expected Filename Patterns

**Major Arcana:**
- `major_00_the_fool.png`
- `major_01_the_magician.png`
- ...
- `major_21_the_world.png`

**Minor Arcana:**
- Aces: `{suit}_01_ace.png` (e.g., `wands_01_ace.png`)
- Numbers 2-10: `{suit}_{number}.png` (e.g., `cups_05.png`)
- Courts:
  - Page: `{suit}_11_page.png`
  - Knight: `{suit}_12_knight.png`
  - Queen: `{suit}_13_queen.png`
  - King: `{suit}_14_king.png`

---

## Appendix C: Commands Reference

### Theme Commands
- `/tarot-themes` - List all available themes
- `/tarot-theme` - Select your theme
- `/tarot-my-theme` - Check current theme
- `/tarot-theme-preview <name>` - Preview a theme
- `/tarot-theme-help` - Theme system help

### Reading Commands
- `/tarot-single` - Single card reading
- `/tarot-three` - Past/Present/Future spread
- `/tarot-celtic` - Celtic Cross (10 cards)
- `/tarot-relationship` - Relationship spread (7 cards)
- `/tarot-career` - Career spread (5 cards)

### Journal Commands
- `/tarot-journal` - View saved readings
- `/tarot-journal-view <id>` - View specific entry
- `/tarot-journal-stats` - Reading statistics

---

*Test Plan Version 1.0 - Last Updated: 2026-04-09*
