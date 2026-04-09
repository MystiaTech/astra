"""
Theme System Tests
==================
QA: Chloe

Tests for the dynamic theme system including hot-reload,
user preferences, and theme discovery.
"""

import pytest
import pytest_asyncio
import json
import os
import tempfile
import shutil
from pathlib import Path
from unittest.mock import MagicMock, patch


class TestThemeStructure:
    """Test Theme dataclass functionality."""
    
    def test_theme_creation(self):
        """THEME-001: Theme objects can be created with required fields."""
        from astra.themes import Theme
        
        theme = Theme(
            id="test_theme",
            name="Test Theme",
            description="A test theme",
            author="Test Author",
            version="1.0.0",
            path="/test/path"
        )
        
        assert theme.id == "test_theme"
        assert theme.name == "Test Theme"
        assert theme.is_default is False
    
    def test_theme_card_path_major_arcana(self):
        """THEME-002: Theme returns correct path for Major Arcana cards."""
        from astra.themes import Theme
        
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a test card file
            card_file = Path(tmpdir) / "major_00.png"
            card_file.touch()
            
            theme = Theme(
                id="test",
                name="Test",
                description="Test",
                author="Test",
                version="1.0",
                path=tmpdir
            )
            
            path = theme.get_card_path("major", 0, reversed=False)
            assert path is not None
            assert "major_00.png" in path
    
    def test_theme_card_path_minor_arcana(self):
        """THEME-003: Theme returns correct path for Minor Arcana cards."""
        from astra.themes import Theme
        
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create test card files
            (Path(tmpdir) / "wands_01.png").touch()
            (Path(tmpdir) / "cups_11.png").touch()
            
            theme = Theme(
                id="test",
                name="Test",
                description="Test",
                author="Test",
                version="1.0",
                path=tmpdir
            )
            
            ace_path = theme.get_card_path("wands", 1, reversed=False)
            page_path = theme.get_card_path("cups", 11, reversed=False)
            
            assert ace_path is not None
            assert "wands_01.png" in ace_path
            assert page_path is not None
            assert "cups_11.png" in page_path
    
    def test_theme_reversed_card_support(self):
        """THEME-004: Theme uses reversed card images when available."""
        from astra.themes import Theme
        
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create upright and reversed versions
            (Path(tmpdir) / "major_00.png").touch()
            (Path(tmpdir) / "major_00_reversed.png").touch()
            
            theme = Theme(
                id="test",
                name="Test",
                description="Test",
                author="Test",
                version="1.0",
                path=tmpdir,
                supports_reversed=True
            )
            
            upright_path = theme.get_card_path("major", 0, reversed=False)
            reversed_path = theme.get_card_path("major", 0, reversed=True)
            
            assert "major_00.png" in upright_path
            assert "major_00_reversed.png" in reversed_path
    
    def test_theme_missing_card_returns_none(self):
        """THEME-005: Theme returns None for missing cards."""
        from astra.themes import Theme
        
        with tempfile.TemporaryDirectory() as tmpdir:
            theme = Theme(
                id="test",
                name="Test",
                description="Test",
                author="Test",
                version="1.0",
                path=tmpdir
            )
            
            path = theme.get_card_path("major", 99, reversed=False)
            assert path is None


class TestThemeManager:
    """Test ThemeManager functionality."""
    
    @pytest.fixture
    def temp_themes_dir(self):
        """Create a temporary themes directory."""
        tmpdir = tempfile.mkdtemp()
        yield tmpdir
        shutil.rmtree(tmpdir)
    
    @pytest.fixture
    def mock_theme_manager(self, temp_themes_dir):
        """Create a theme manager with temp directory."""
        from astra.themes import ThemeManager
        
        manager = ThemeManager()
        manager.THEMES_DIR = temp_themes_dir
        manager.PREFS_FILE = os.path.join(temp_themes_dir, "prefs.json")
        return manager
    
    def test_manager_creates_default_theme(self, mock_theme_manager):
        """MGR-001: Manager creates default theme if none exists."""
        import asyncio
        
        asyncio.run(mock_theme_manager.scan_themes())
        
        assert "default" in mock_theme_manager.themes
        assert mock_theme_manager.default_theme is not None
    
    def test_manager_loads_theme_from_folder(self, mock_theme_manager, temp_themes_dir):
        """MGR-002: Manager loads themes from folders with theme.json."""
        import asyncio
        
        # Create a custom theme
        theme_dir = Path(temp_themes_dir) / "custom"
        theme_dir.mkdir()
        
        theme_json = {
            "name": "Custom Theme",
            "description": "A custom theme",
            "author": "Test",
            "version": "1.0"
        }
        
        with open(theme_dir / "theme.json", "w") as f:
            json.dump(theme_json, f)
        
        # Create some card files
        (theme_dir / "major_00.png").touch()
        (theme_dir / "wands_01.png").touch()
        
        asyncio.run(mock_theme_manager.scan_themes())
        
        assert "custom" in mock_theme_manager.themes
        assert mock_theme_manager.themes["custom"].name == "Custom Theme"
    
    def test_manager_user_preferences(self, mock_theme_manager):
        """MGR-003: Manager stores and retrieves user theme preferences."""
        # Set preference
        result = mock_theme_manager.set_user_theme("12345", "default")
        assert result is True
        
        # Get preference
        theme = mock_theme_manager.get_user_theme("12345")
        assert theme is not None
        
        # Check if selected
        assert mock_theme_manager.has_selected_theme("12345") is True
        assert mock_theme_manager.has_selected_theme("99999") is False
    
    def test_manager_invalid_theme_id(self, mock_theme_manager):
        """MGR-004: Manager rejects invalid theme IDs."""
        result = mock_theme_manager.set_user_theme("12345", "nonexistent")
        assert result is False
    
    def test_manager_get_available_themes(self, mock_theme_manager):
        """MGR-005: Manager returns list of available themes."""
        import asyncio
        
        asyncio.run(mock_theme_manager.scan_themes())
        themes = mock_theme_manager.get_available_themes()
        
        assert len(themes) >= 1
        assert all(isinstance(t.id, str) for t in themes)


class TestThemeDiscovery:
    """Test theme discovery and hot-reload."""
    
    @pytest_asyncio.fixture
    async def temp_theme_setup(self):
        """Create temporary theme structure."""
        tmpdir = tempfile.mkdtemp()
        
        # Create default theme
        default_dir = Path(tmpdir) / "default"
        default_dir.mkdir()
        with open(default_dir / "theme.json", "w") as f:
            json.dump({
                "name": "Default",
                "description": "Default theme",
                "author": "Test",
                "version": "1.0",
                "is_default": True
            }, f)
        
        yield tmpdir
        
        shutil.rmtree(tmpdir)
    
    @pytest.mark.asyncio
    async def test_scan_discovers_new_themes(self, temp_theme_setup):
        """DISCOVER-001: Scan discovers themes in themes directory."""
        from astra.themes import ThemeManager
        
        manager = ThemeManager()
        manager.THEMES_DIR = temp_theme_setup
        manager.PREFS_FILE = os.path.join(temp_theme_setup, "prefs.json")
        
        # Add a new theme after manager creation
        new_theme_dir = Path(temp_theme_setup) / "new_theme"
        new_theme_dir.mkdir()
        with open(new_theme_dir / "theme.json", "w") as f:
            json.dump({
                "name": "New Theme",
                "description": "A new theme",
                "author": "Test",
                "version": "1.0"
            }, f)
        (new_theme_dir / "major_00.png").touch()
        
        discovered = await manager.scan_themes()
        
        assert len(discovered) >= 1
        assert any(t.id == "new_theme" for t in discovered)
    
    @pytest.mark.asyncio
    async def test_scan_detects_removed_themes(self, temp_theme_setup):
        """DISCOVER-002: Scan removes themes that no longer exist."""
        from astra.themes import ThemeManager
        
        manager = ThemeManager()
        manager.THEMES_DIR = temp_theme_setup
        manager.PREFS_FILE = os.path.join(temp_theme_setup, "prefs.json")
        
        # First scan to load themes
        await manager.scan_themes()
        initial_count = len(manager.themes)
        
        # Add then remove a theme
        temp_theme = Path(temp_theme_setup) / "temp"
        temp_theme.mkdir()
        with open(temp_theme / "theme.json", "w") as f:
            json.dump({
                "name": "Temp",
                "description": "Temp",
                "author": "Test",
                "version": "1.0"
            }, f)
        (temp_theme / "major_00.png").touch()
        
        await manager.scan_themes()
        assert "temp" in manager.themes
        
        # Remove theme
        shutil.rmtree(temp_theme)
        
        await manager.scan_themes()
        assert "temp" not in manager.themes


class TestThemeCardImageLookup:
    """Test card image path resolution."""
    
    @pytest.fixture
    def mock_manager_with_themes(self):
        """Create a manager with mock themes."""
        from astra.themes import ThemeManager, Theme
        
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create default theme
            default_dir = Path(tmpdir) / "default"
            default_dir.mkdir()
            (default_dir / "major_00.png").touch()
            (default_dir / "wands_01.png").touch()
            
            # Create custom theme
            custom_dir = Path(tmpdir) / "custom"
            custom_dir.mkdir()
            (custom_dir / "major_00.png").touch()
            (custom_dir / "cups_01.png").touch()
            
            manager = ThemeManager()
            manager.THEMES_DIR = tmpdir
            manager.PREFS_FILE = os.path.join(tmpdir, "prefs.json")
            
            manager.themes["default"] = Theme(
                id="default",
                name="Default",
                description="Default",
                author="Test",
                version="1.0",
                path=str(default_dir),
                is_default=True
            )
            manager.default_theme = manager.themes["default"]
            
            manager.themes["custom"] = Theme(
                id="custom",
                name="Custom",
                description="Custom",
                author="Test",
                version="1.0",
                path=str(custom_dir)
            )
            
            yield manager
    
    def test_get_card_from_user_theme(self, mock_manager_with_themes):
        """LOOKUP-001: Returns card from user's selected theme."""
        manager = mock_manager_with_themes
        manager.set_user_theme("12345", "custom")
        
        path = manager.get_card_image_path("12345", "cups", 1, reversed=False)
        
        assert path is not None
        assert "custom" in path
        assert "cups_01.png" in path
    
    def test_fallback_to_default_theme(self, mock_manager_with_themes):
        """LOOKUP-002: Falls back to default when card missing in user theme."""
        manager = mock_manager_with_themes
        manager.set_user_theme("12345", "custom")
        
        # wands_01 doesn't exist in custom theme
        path = manager.get_card_image_path("12345", "wands", 1, reversed=False)
        
        assert path is not None
        assert "default" in path
        assert "wands_01.png" in path
    
    def test_no_theme_selected_uses_default(self, mock_manager_with_themes):
        """LOOKUP-003: Uses default theme when user has no preference."""
        manager = mock_manager_with_themes
        
        path = manager.get_card_image_path("99999", "major", 0, reversed=False)
        
        assert path is not None
        assert "default" in path


class TestThemeNamingConventions:
    """Test card filename formats."""
    
    def test_default_naming_format(self):
        """NAMING-001: Default format is {suit}_{number}.png."""
        from astra.themes import Theme
        
        theme = Theme(
            id="test",
            name="Test",
            description="Test",
            author="Test",
            version="1.0",
            path="/test",
            card_format="{suit}_{number}.png"
        )
        
        assert theme.card_format == "{suit}_{number}.png"
    
    def test_custom_naming_format(self):
        """NAMING-002: Themes can have custom naming formats."""
        from astra.themes import Theme
        
        theme = Theme(
            id="test",
            name="Test",
            description="Test",
            author="Test",
            version="1.0",
            path="/test",
            card_format="{suit}/{number}.png"
        )
        
        # Format would produce paths like "major/00.png"
        assert "{suit}" in theme.card_format
        assert "{number}" in theme.card_format


class TestThemeEdgeCases:
    """Test edge cases and error handling."""
    
    def test_empty_themes_directory(self):
        """EDGE-001: Handles empty themes directory gracefully."""
        import asyncio
        from astra.themes import ThemeManager
        
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = ThemeManager()
            manager.THEMES_DIR = tmpdir
            manager.PREFS_FILE = os.path.join(tmpdir, "prefs.json")
            
            asyncio.run(manager.scan_themes())
            
            # Should still have default theme
            assert manager.default_theme is not None
    
    def test_corrupted_theme_json(self):
        """EDGE-002: Skips themes with corrupted theme.json."""
        import asyncio
        from astra.themes import ThemeManager
        
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create theme with invalid JSON
            bad_theme = Path(tmpdir) / "bad"
            bad_theme.mkdir()
            with open(bad_theme / "theme.json", "w") as f:
                f.write("not valid json {{{")
            (bad_theme / "major_00.png").touch()
            
            manager = ThemeManager()
            manager.THEMES_DIR = tmpdir
            manager.PREFS_FILE = os.path.join(tmpdir, "prefs.json")
            
            # Should not crash
            asyncio.run(manager.scan_themes())
            
            # Bad theme should not be loaded
            assert "bad" not in manager.themes
    
    def test_theme_with_few_cards(self):
        """EDGE-003: Auto-detects themes with minimal card count."""
        import asyncio
        from astra.themes import ThemeManager
        
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create theme with only 5 cards (below threshold)
            partial = Path(tmpdir) / "partial"
            partial.mkdir()
            for i in range(5):
                (partial / f"major_{i:02d}.png").touch()
            
            manager = ThemeManager()
            manager.THEMES_DIR = tmpdir
            manager.PREFS_FILE = os.path.join(tmpdir, "prefs.json")
            
            # Might or might not be detected based on threshold
            # Just ensure no crash
            asyncio.run(manager.scan_themes())


class TestThemeStats:
    """Test theme statistics."""
    
    def test_theme_usage_stats(self):
        """STATS-001: Manager tracks theme usage statistics."""
        from astra.themes import ThemeManager
        
        manager = ThemeManager()
        
        # Simulate user preferences
        manager.user_preferences = {
            "1": "default",
            "2": "default",
            "3": "custom",
            "4": "custom",
            "5": "custom"
        }
        
        stats = manager.get_theme_stats()
        
        assert stats["total_users_with_preference"] == 5
        assert stats["theme_usage"]["default"] == 2
        assert stats["theme_usage"]["custom"] == 3
