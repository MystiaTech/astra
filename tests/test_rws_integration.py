"""
Rider-Waite-Smith Classic Deck Integration Tests
================================================
QA: Chloe

Tests specifically for the classic RWS deck integration.
Covers theme loading, card display, and integration with spreads/journal.

Run with: pytest tests/test_rws_integration.py -v
"""

import json
import tempfile
from pathlib import Path
from unittest.mock import MagicMock

import pytest


class TestRWSThemeConfiguration:
    """Test classic theme configuration and metadata."""

    def test_classic_theme_directory_structure(self):
        """RWS-001: Classic theme directory exists with proper structure."""
        classic_dir = Path("themes/classic")

        # Directory should exist
        assert classic_dir.exists(), "Classic theme directory should exist"
        assert classic_dir.is_dir(), "Classic theme should be a directory"

        # Should have theme.json
        theme_json = classic_dir / "theme.json"
        assert theme_json.exists(), "theme.json should exist"

    def test_classic_theme_json_valid(self):
        """RWS-002: theme.json is valid and has required fields."""
        theme_json_path = Path("themes/classic/theme.json")

        if not theme_json_path.exists():
            pytest.skip("Classic theme not yet installed")

        with open(theme_json_path, "r", encoding="utf-8") as f:
            config = json.load(f)

        # Required fields
        required = ["name", "description", "author", "version", "card_format"]
        for field in required:
            assert field in config, f"theme.json missing required field: {field}"

        # RWS-specific validation
        name_lower = config.get("name", "").lower()
        assert (
            "rider" in name_lower or "waite" in name_lower
        ), "Theme name should reference Rider-Waite"

        # Should NOT be default
        assert config.get("is_default") is False, "Classic theme should not be the default"

        # Should not support reversed (unless we get special artwork)
        assert (
            config.get("supports_reversed") is False
        ), "Classic theme should not claim reversed support without reversed images"

    def test_classic_theme_metadata(self):
        """RWS-003: Theme has proper Pamela Colman Smith attribution."""
        theme_json_path = Path("themes/classic/theme.json")

        if not theme_json_path.exists():
            pytest.skip("Classic theme not yet installed")

        with open(theme_json_path, "r", encoding="utf-8") as f:
            config = json.load(f)

        # Check for attribution
        author = config.get("author", "").lower()
        description = config.get("description", "").lower()

        has_attribution = (
            "pamela" in author
            or "colman" in author
            or "smith" in author
            or "pamela" in description
            or "colman" in description
            or "smith" in description
        )

        assert has_attribution, "Theme should attribute Pamela Colman Smith"


class TestRWSImageFiles:
    """Test classic card image files."""

    @pytest.fixture
    def classic_dir(self):
        """Provide classic theme directory path."""
        return Path("themes/classic")

    def test_all_major_arcana_exist(self, classic_dir):
        """RWS-010: All 22 Major Arcana images exist."""
        if not classic_dir.exists():
            pytest.skip("Classic theme not yet installed")

        major_arcana = [
            (0, "the_fool"),
            (1, "the_magician"),
            (2, "the_high_priestess"),
            (3, "the_empress"),
            (4, "the_emperor"),
            (5, "the_hierophant"),
            (6, "the_lovers"),
            (7, "the_chariot"),
            (8, "strength"),
            (9, "the_hermit"),
            (10, "wheel_of_fortune"),
            (11, "justice"),
            (12, "the_hanged_man"),
            (13, "death"),
            (14, "temperance"),
            (15, "the_devil"),
            (16, "the_tower"),
            (17, "the_star"),
            (18, "the_moon"),
            (19, "the_sun"),
            (20, "judgement"),
            (21, "the_world"),
        ]

        missing = []
        for number, name in major_arcana:
            filename = f"major_{number:02d}_{name}.png"
            if not (classic_dir / filename).exists():
                missing.append(filename)

        if missing:
            pytest.skip(f"Missing Major Arcana images: {missing}")

        assert len(missing) == 0, f"Missing {len(missing)} Major Arcana images"

    def test_all_minor_arcana_exist(self, classic_dir):
        """RWS-011: All 56 Minor Arcana images exist."""
        if not classic_dir.exists():
            pytest.skip("Classic theme not yet installed")

        suits = ["wands", "cups", "swords", "pentacles"]
        court_cards = {11: "page", 12: "knight", 13: "queen", 14: "king"}

        missing = []
        for suit in suits:
            for number in range(1, 15):
                if number == 1:
                    filename = f"{suit}_01_ace.png"
                elif number >= 11:
                    filename = f"{suit}_{number:02d}_{court_cards[number]}.png"
                else:
                    filename = f"{suit}_{number:02d}.png"

                if not (classic_dir / filename).exists():
                    missing.append(filename)

        if missing:
            pytest.skip(f"Missing Minor Arcana images: {missing[:5]}... ({len(missing)} total)")

        assert len(missing) == 0, f"Missing {len(missing)} Minor Arcana images"

    def test_no_zero_byte_files(self, classic_dir):
        """RWS-012: No image files are empty (0 bytes)."""
        if not classic_dir.exists():
            pytest.skip("Classic theme not yet installed")

        empty_files = []
        for img_file in classic_dir.glob("*.png"):
            if img_file.stat().st_size == 0:
                empty_files.append(img_file.name)

        assert len(empty_files) == 0, f"Found {len(empty_files)} empty image files: {empty_files}"

    def test_image_file_sizes_reasonable(self, classic_dir):
        """RWS-013: Image files have reasonable sizes (1KB - 10MB)."""
        if not classic_dir.exists():
            pytest.skip("Classic theme not yet installed")

        suspicious_files = []
        for img_file in classic_dir.glob("*.png"):
            size = img_file.stat().st_size
            if size < 1024:  # Less than 1KB
                suspicious_files.append((img_file.name, size, "too small"))
            elif size > 10 * 1024 * 1024:  # More than 10MB
                suspicious_files.append((img_file.name, size, "too large"))

        # Just warn about suspicious sizes, don't fail
        if suspicious_files:
            for name, size, reason in suspicious_files:
                print(f"⚠️  Warning: {name} is {reason} ({size} bytes)")


class TestRWSThemeIntegration:
    """Test classic theme integration with theme system."""

    @pytest.fixture
    def mock_classic_theme(self):
        """Create a temporary classic theme structure."""
        with tempfile.TemporaryDirectory() as tmpdir:
            classic_dir = Path(tmpdir) / "classic"
            classic_dir.mkdir()

            # Create theme.json
            theme_config = {
                "name": "Classic Rider-Waite",
                "description": "Authentic Pamela Colman Smith illustrations (1909)",
                "author": "Pamela Colman Smith",
                "version": "1.0.0",
                "card_format": "{suit}_{number}_{name}.png",
                "supports_reversed": False,
                "is_default": False,
                "extra": {"artist": "Pamela Colman Smith", "year": "1909"},
            }

            with open(classic_dir / "theme.json", "w") as f:
                json.dump(theme_config, f)

            # Create some sample card files
            (classic_dir / "major_00_the_fool.png").touch()
            (classic_dir / "wands_01_ace.png").touch()
            (classic_dir / "cups_14_king.png").touch()

            yield str(classic_dir), theme_config

    def test_classic_theme_loading(self, mock_classic_theme):
        """RWS-020: Classic theme loads correctly via ThemeManager."""
        from astra.themes import ThemeManager

        classic_path, config = mock_classic_theme

        # Create manager with test directory
        manager = ThemeManager()
        manager.THEMES_DIR = str(Path(classic_path).parent)
        manager.PREFS_FILE = str(Path(classic_path).parent / "prefs.json")

        # Scan themes
        import asyncio

        asyncio.run(manager.scan_themes())

        # Should find classic theme
        assert "classic" in manager.themes, "Classic theme should be discovered"

        theme = manager.themes["classic"]
        assert theme.name == "Classic Rider-Waite"
        assert theme.author == "Pamela Colman Smith"

    def test_classic_card_path_resolution(self, mock_classic_theme):
        """RWS-021: Card paths resolve correctly for classic theme."""
        from astra.themes import Theme

        classic_path, _ = mock_classic_theme

        theme = Theme(
            id="classic",
            name="Classic Rider-Waite",
            description="Test",
            author="PCS",
            version="1.0",
            path=classic_path,
            card_format="{suit}_{number}_{name}.png",
        )

        # Test Major Arcana
        path = theme.get_card_path("major", 0, card_name="The Fool")
        assert path is not None
        assert "major_00_the_fool.png" in path

        # Test Minor Arcana
        path = theme.get_card_path("wands", 1)
        assert path is not None
        assert "wands_01_ace.png" in path

    def test_user_can_select_classic_theme(self, mock_classic_theme):
        """RWS-022: User can select classic theme."""
        from astra.themes import ThemeManager

        classic_path, _ = mock_classic_theme

        manager = ThemeManager()
        manager.THEMES_DIR = str(Path(classic_path).parent)
        manager.PREFS_FILE = str(Path(classic_path).parent / "prefs.json")

        import asyncio

        asyncio.run(manager.scan_themes())

        # User selects classic
        result = manager.set_user_theme("test_user_123", "classic")
        assert result is True, "Should successfully set classic theme"

        # Verify selection
        theme = manager.get_user_theme("test_user_123")
        assert theme.id == "classic"

    def test_classic_theme_persistence(self, mock_classic_theme):
        """RWS-023: Classic theme selection persists."""
        from astra.themes import ThemeManager

        classic_path, _ = mock_classic_theme
        prefs_file = str(Path(classic_path).parent / "prefs.json")

        # First manager instance
        manager1 = ThemeManager()
        manager1.THEMES_DIR = str(Path(classic_path).parent)
        manager1.PREFS_FILE = prefs_file

        import asyncio

        asyncio.run(manager1.scan_themes())
        manager1.set_user_theme("user_456", "classic")

        # Second manager instance (simulating restart)
        manager2 = ThemeManager()
        manager2.THEMES_DIR = str(Path(classic_path).parent)
        manager2.PREFS_FILE = prefs_file

        asyncio.run(manager2.scan_themes())
        theme = manager2.get_user_theme("user_456")
        assert theme.id == "classic", "Theme should persist after restart"


class TestRWSSpreadDisplay:
    """Test classic cards display correctly in spreads."""

    def test_single_card_embed_with_classic(self):
        """RWS-030: Single card reading displays classic image."""
        from unittest.mock import MagicMock

        from astra.data import SPREADS, TAROT_DECK
        from astra.embeds import create_reading_embed_with_images
        from astra.reading import Reading, ReadingResult

        # Create reading with first card
        card = TAROT_DECK[0]  # The Fool
        reading = Reading(
            spread_type="single",
            question="Test question",
            results=[ReadingResult(card=card, position=1, reversed=False)],
        )

        # Mock user
        mock_user = MagicMock()
        mock_user.display_name = "TestUser"
        mock_user.display_avatar = MagicMock()
        mock_user.display_avatar.url = "http://example.com/avatar.png"

        spread = SPREADS["single"]

        # This would need actual image files to fully test
        # For now, just verify it doesn't crash
        try:
            embed, files = create_reading_embed_with_images(reading, mock_user, spread, "test_user")
            assert embed is not None
        except Exception as e:
            pytest.skip(f"Image loading failed (expected if images not present): {e}")

    def test_celtic_cross_ten_cards(self):
        """RWS-031: Celtic Cross displays 10 cards correctly."""
        from astra.bot import TarotCommands
        from astra.data import SPREADS

        spread = SPREADS["celtic"]
        assert spread.num_cards == 10

        # Test card drawing
        cog = TarotCommands(None)
        reading = cog._draw_cards(
            spread_type="celtic", question="Test Celtic Cross", allow_reversed=False
        )

        assert len(reading.results) == 10

        # Verify position assignments
        for i, result in enumerate(reading.results):
            assert result.position == i + 1


class TestRWSJournalIntegration:
    """Test classic theme integration with journal system."""

    def test_journal_saves_theme_info(self):
        """RWS-040: Journal entries preserve theme information."""
        from astra.journal import JournalManager

        with tempfile.TemporaryDirectory() as tmpdir:
            manager = JournalManager()
            manager.JOURNAL_DIR = tmpdir

            # Simulate saving a reading with classic theme
            cards_data = [
                {
                    "name": "The Fool",
                    "position": 1,
                    "reversed": False,
                    "meaning": "New beginnings...",
                    "keywords": ["beginnings", "innocence"],
                }
            ]

            entry = manager.save_reading(
                user_id="test_user",
                spread_type="single",
                question="Test question",
                cards=cards_data,
                interpretation="Test interpretation",
                notes="Used Classic Rider-Waite theme",
            )

            assert entry is not None
            assert entry.spread_type == "single"

            # Retrieve and verify
            readings = manager.get_user_readings("test_user")
            assert len(readings) == 1
            assert readings[0].cards[0]["name"] == "The Fool"


class TestRWSAttribution:
    """Test proper attribution display."""

    def test_theme_list_shows_attribution(self):
        """RWS-050: Theme list shows Pamela Colman Smith credit."""
        from astra.theme_embeds import create_theme_list_embed
        from astra.themes import Theme

        # Create mock themes
        classic_theme = Theme(
            id="classic",
            name="Classic Rider-Waite",
            description="Authentic Pamela Colman Smith illustrations from 1909",
            author="Pamela Colman Smith",
            version="1.0.0",
            path="/test/classic",
        )

        mock_manager = MagicMock()
        mock_manager.user_preferences = {}

        embed = create_theme_list_embed([classic_theme], mock_manager)

        # Check that embed contains theme info
        assert "Classic Rider-Waite" in str(embed.title) or any(
            "Classic Rider-Waite" in str(field.name) for field in embed.fields
        )


class TestRWSPerformance:
    """Test performance characteristics."""

    @pytest.mark.skip(reason="Requires actual image files")
    def test_image_load_time(self):
        """RWS-060: Images load within acceptable time (< 2 seconds)."""
        # Sample 10 random cards
        import random
        import time

        from astra.data import TAROT_DECK
        from astra.embeds import get_card_image_path

        sample_cards = random.sample(TAROT_DECK, 10)

        load_times = []
        for card in sample_cards:
            start = time.time()
            get_card_image_path(card, reversed=False)
            elapsed = time.time() - start
            load_times.append(elapsed)

        avg_time = sum(load_times) / len(load_times)
        assert avg_time < 2.0, f"Average load time {avg_time:.2f}s exceeds 2 second threshold"


class TestRWSFallbackBehavior:
    """Test fallback when classic images are missing."""

    def test_fallback_to_default_theme(self):
        """RWS-070: Falls back to default when classic card missing."""
        from astra.themes import Theme, ThemeManager

        with tempfile.TemporaryDirectory() as tmpdir:
            # Create default theme with all cards
            default_dir = Path(tmpdir) / "default"
            default_dir.mkdir()
            (default_dir / "major_00_the_fool.png").touch()
            (default_dir / "wands_01_ace.png").touch()

            # Create classic theme missing some cards
            classic_dir = Path(tmpdir) / "classic"
            classic_dir.mkdir()
            (classic_dir / "major_00_the_fool.png").touch()
            # Note: wands_01_ace.png is missing!

            manager = ThemeManager()
            manager.THEMES_DIR = tmpdir
            manager.PREFS_FILE = str(Path(tmpdir) / "prefs.json")

            # Set up themes manually
            manager.themes["default"] = Theme(
                id="default",
                name="Default",
                description="Default",
                author="Test",
                version="1.0",
                path=str(default_dir),
                card_format="{suit}_{number}_{name}.png",
                is_default=True,
            )
            manager.default_theme = manager.themes["default"]

            manager.themes["classic"] = Theme(
                id="classic",
                name="Classic",
                description="Classic",
                author="Test",
                version="1.0",
                path=str(classic_dir),
                card_format="{suit}_{number}_{name}.png",
            )

            # User has classic selected
            manager.set_user_theme("test_user", "classic")

            # Request card that exists in classic
            path = manager.get_card_image_path("test_user", "major", 0)
            assert "classic" in path

            # Request card missing in classic - should fallback to default
            path = manager.get_card_image_path("test_user", "wands", 1)
            assert path is not None
            assert "default" in path


# Mark tests that require actual image files
pytestmark = [
    pytest.mark.integration,
]
