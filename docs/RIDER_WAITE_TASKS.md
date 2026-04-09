# Classic Rider-Waite Card Integration
## Team Assignments

---

## 📚 Sarah (Research Lead) - Task 1

### Find Authentic Rider-Waite Sources

**Objective:** Research and document legitimate sources for classic Rider-Waite tarot card images.

#### Sources to Investigate:

1. **Public Domain Options:**
   - Original 1909 RWS deck (Pamela Colman Smith) - may be public domain in some jurisdictions
   - Wikimedia Commons tarot collection
   - Internet Archive scanned decks

2. **Creative Commons / Free Licenses:**
   - Check for CC-BY or CC0 licensed decks
   - Open source tarot projects
   - Academic/ educational collections

3. **Purchasable Licensed Decks:**
   - US Games Systems official licensing
   - Other publishers with digital rights
   - Cost estimates for licensing

#### Deliverables:
- [ ] List of 3-5 viable image sources
- [ ] Copyright status for each source
- [ ] Recommended source with justification
- [ ] Licensing requirements documentation

**Time Estimate:** 2-3 days

---

## 🖼️ Maya (Assets Lead) - Task 2

### Acquire and Format Card Images

**Objective:** Obtain all 78 Rider-Waite cards in consistent format.

#### Requirements:

**Image Specifications:**
- Format: PNG (transparent background preferred)
- Size: 300x500 pixels minimum
- Aspect ratio: 2:3 (tarot standard)
- Color space: RGB
- Naming: Match existing convention (e.g., `major_00_the_fool.png`)

**Card Set:**
- Major Arcana: 22 cards (0-21)
- Minor Arcana: 56 cards
  - Wands: 14 cards (Ace through King)
  - Cups: 14 cards
  - Swords: 14 cards  
  - Pentacles: 14 cards

#### Deliverables:
- [ ] All 78 cards in `themes/classic/` directory
- [ ] Consistent sizing and formatting
- [ ] README with source attribution
- [ ] Sample cards for team review (first 5 cards)

**Time Estimate:** 3-5 days

---

## 💻 Emma (Backend Lead) - Task 3

### Update Theme System

**Objective:** Ensure theme system properly supports the classic deck.

#### Tasks:

1. **Create Classic Theme Config:**
```json
{
  "name": "Classic Rider-Waite",
  "description": "Authentic Pamela Colman Smith illustrations (1909)",
  "author": "Pamela Colman Smith",
  "version": "1.0.0",
  "card_format": "{suit}_{number}_{name}.png",
  "supports_reversed": false,
  "is_default": false
}
```

2. **Update Image Path Resolution:**
   - Ensure `themes/classic/` is checked
   - Support both upright and reversed (if available)
   - Fallback handling

3. **Add Theme Selection:**
   - Classic theme appears in `/tarot-themes`
   - Proper metadata display

#### Deliverables:
- [ ] `themes/classic/theme.json` created
- [ ] Image path resolution tested
- [ ] Theme appears in theme list

**Time Estimate:** 1 day

---

## 🎨 Olivia (UX Lead) - Task 4

### Update Card Display

**Objective:** Optimize embed display for classic Rider-Waite cards.

#### Tasks:

1. **Image Display Optimization:**
   - Ensure classic cards display at proper size
   - Test aspect ratio preservation
   - Verify image quality in Discord

2. **Card Information Enhancement:**
   - Add Pamela Colman Smith attribution
   - Include traditional RWS keywords
   - Link to card meanings

3. **Reversed Card Handling:**
   - If no reversed images: rotate 180°
   - Add "Reversed" indicator

#### Deliverables:
- [ ] Classic cards display correctly in embeds
- [ ] Attribution shown properly
- [ ] Reversed cards handled

**Time Estimate:** 1-2 days

---

## 🧪 Chloe (QA Lead) - Task 5

### Test Complete Card Set

**Objective:** Verify all 78 classic cards display correctly.

#### Test Plan:

1. **Individual Card Tests:**
   ```bash
   # Test each card type
   Major Arcana: 0-21 (22 cards)
   Minor Arcana Numbers: 1-10 each suit (40 cards)
   Minor Arcana Courts: 11-14 each suit (16 cards)
   ```

2. **Spread Tests:**
   - Single card (random)
   - Three card spread
   - Celtic Cross (10 cards)

3. **Theme Switching:**
   - Switch between default and classic
   - Verify correct images load

4. **Edge Cases:**
   - Missing images (fallback)
   - Reversed cards
   - Slow loading

#### Deliverables:
- [ ] All 78 cards tested individually
- [ ] Test report with screenshots
- [ ] Bug list (if any)
- [ ] Sign-off for deployment

**Time Estimate:** 2 days

---

## 📋 Project Timeline

| Day | Task | Owner |
|-----|------|-------|
| 1-2 | Research sources | Sarah |
| 2 | Review and approve source | Kimi |
| 3-6 | Acquire and format images | Maya |
| 6 | Update theme system | Emma |
| 6-7 | Update display | Olivia |
| 7-8 | Testing | Chloe |
| 8 | Deployment | Kimi |

**Total: 8 days**

---

## ⚠️ Important Notes

### Copyright Considerations:
- Original 1909 RWS deck may be public domain in some countries
- US Games Systems holds copyright in USA
- Must verify legal use in target jurisdictions
- Consider using early public domain scans

### Alternative: Create Placeholder Enhancement
If authentic RWS cannot be obtained legally, enhance existing placeholders:
- Higher quality placeholder images
- Traditional RWS color schemes
- Symbolic representations

---

## 🔗 Helpful Resources

- Wikimedia Commons: https://commons.wikimedia.org/wiki/Category:Rider-Waite_tarot
- Internet Archive: https://archive.org/search?query=rider+waite+tarot
- Sacred Texts: https://sacred-texts.com/tarot/
- Aeclectic Tarot: https://www.aeclectic.net/tarot/

---

**Next Step:** Sarah to begin research and report findings within 2 days.
