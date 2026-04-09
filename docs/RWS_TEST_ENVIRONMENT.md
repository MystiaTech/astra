# Rider-Waite-Smith Test Environment Setup

**Document:** Test Environment Preparation Guide  
**Owner:** Chloe (QA Lead)  
**Date:** 2026-04-09  
**Status:** Ready for Testing

---

## Quick Start Checklist

Use this checklist to prepare the test environment once Maya completes the image assets.

### Pre-Testing Setup

- [ ] **1. Verify Classic Theme Directory Structure**
  ```bash
  ls -la themes/classic/
  ```
  Expected: 78 PNG files + theme.json + optional preview.png

- [ ] **2. Run Automated Verification Script**
  ```bash
  python scripts/verify_rws_images.py --verbose
  ```
  **Expected Result:** Status: PASSED - All images ready!

- [ ] **3. Verify theme.json Configuration**
  ```bash
  cat themes/classic/theme.json
  ```

- [ ] **4. Install/Update Dependencies**
  ```bash
  pip install -e .
  ```

- [ ] **5. Run Unit Tests**
  ```bash
  pytest tests/test_rws_integration.py -v
  ```

- [ ] **6. Set Up Discord Test Environment**
  - Create test Discord server
  - Invite test bot instance
  - Create #test-readings channel
  - Prepare test user accounts

---

## Detailed Component Verification

### A. Image Assets Verification

#### A.1 File Count Verification
```bash
echo "PNG files in themes/classic/:"
ls themes/classic/*.png 2>/dev/null | wc -l
# Expected: 78 (or 79 with preview.png)
```

#### A.2 File Naming Convention
Run the verification script to check all naming:
```bash
python scripts/verify_rws_images.py
```

#### A.3 Image Integrity Check
All files should be valid PNG images (non-zero size, correct magic bytes).

---

### B. Theme System Verification

#### B.1 Theme Discovery
The classic theme should appear in theme listings:
```bash
python -c "from astra.themes import ThemeManager; mgr = ThemeManager(); mgr.scan_themes(); print(list(mgr.themes.keys()))"
```

#### B.2 Card Path Resolution
Card images should be resolvable via the theme system.

---

### C. Database/Storage Verification

Ensure data directories exist:
- `data/` - User preferences
- `data/journals/` - Journal storage

---

### D. Discord Bot Verification

Verify commands are available:
- `/tarot-themes` - List available themes
- `/tarot-theme` - Select a theme
- `/tarot-my-theme` - Check current theme

---

## Manual Testing Procedures

### Phase 1: Individual Card Testing (2-3 hours)

For each of the 78 cards:
1. Trigger a reading that shows the card
2. Verify image displays correctly
3. Check no distortion/stretching
4. Verify card name matches image
5. Mark off in test plan checklist

### Phase 2: Spread Testing (1 hour)

Test each spread type:
1. `/tarot-single` - Verify 1 card displays
2. `/tarot-three` - Verify 3 cards, correct positions
3. `/tarot-celtic` - Verify 10 cards, correct positions
4. `/tarot-relationship` - Verify 7 cards
5. `/tarot-career` - Verify 5 cards

### Phase 3: Theme System Testing (30 min)

1. `/tarot-themes` - Verify classic appears in list
2. `/tarot-theme` - Select classic theme
3. `/tarot-my-theme` - Verify selection saved
4. Run reading - Verify classic images used
5. Switch to default theme
6. Run reading - Verify default images used

### Phase 4: Journal Testing (30 min)

1. Run a reading with classic theme
2. Save to journal
3. `/tarot-journal` - Verify entry appears
4. `/tarot-journal-view 1` - Verify details correct
5. Restart bot
6. Verify journal entry persists

### Phase 5: Edge Cases (30 min)

1. Delete a card image, verify fallback works
2. Corrupt a card image, verify error handling
3. Two users with different themes simultaneously
4. Rapid theme switching

---

## Automated Test Execution

### Run All RWS Tests
```bash
pytest tests/test_rws_integration.py -v
```

### Run Image Verification
```bash
python scripts/verify_rws_images.py
```

---

## Sign-off Checklist

Before declaring testing complete:

- [ ] All 78 images verified by script
- [ ] All automated tests pass (or appropriately skipped)
- [ ] Manual testing completed per procedures
- [ ] Theme switching tested
- [ ] Journal integration tested
- [ ] Edge cases tested
- [ ] Performance acceptable (images load < 2 seconds)
- [ ] No critical bugs open
- [ ] Test report generated
- [ ] Stakeholders signed off

---

*Document Version 1.0 - Last Updated: 2026-04-09*
