"""
Theme Management System
=======================
IMPLEMENTATION BY: Emma (Backend Lead)

Dynamic theme loading with hot-reload support.
Users can select themes on first use, themes auto-detect without restart.
"""

import asyncio
import json
import logging
import os
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Callable, Optional

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

logger = logging.getLogger(__name__)


@dataclass
class Theme:
    """
    Represents a card theme/deck.

    Attributes:
        id: Unique theme identifier (folder name)
        name: Display name for users
        description: Theme description
        author: Theme creator
        version: Theme version
        path: Filesystem path to theme folder
        card_format: Filename format string
        supports_reversed: Whether theme has reversed card images
        preview_image: Path to preview/thumbnail image
        is_default: Whether this is the fallback theme
        metadata: Additional theme metadata
    """

    id: str
    name: str
    description: str
    author: str
    version: str
    path: str
    card_format: str = "{suit}_{number}.png"
    supports_reversed: bool = False
    preview_image: Optional[str] = None
    is_default: bool = False
    metadata: dict = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

    def get_card_path(
        self, suit: str, number: int, reversed: bool = False, card_name: Optional[str] = None
    ) -> Optional[str]:
        """Get the path to a specific card image."""
        suit_lower = suit.lower()

        # Default project naming convention is numeric and zero-padded, e.g.:
        # - major_00.png .. major_21.png
        # - wands_01.png .. wands_14.png (and similarly for other suits)
        num_str = f"{number:02d}"

        # Prepare format arguments
        format_args = {"suit": suit_lower, "number": num_str, "num": number}

        # Add convenience keys for formats that want rank/court/name.
        court_names = {11: "page", 12: "knight", 13: "queen", 14: "king"}
        if suit_lower != "major":
            if number in court_names:
                court = court_names[number]
                format_args["court"] = court
                format_args["name"] = court
            elif number == 1:
                format_args["rank"] = "ace"
                format_args["name"] = "ace"
            else:
                format_args["rank"] = str(number)
                format_args["name"] = str(number)

            if card_name:
                format_args["full_name"] = card_name.lower().replace(" ", "_").replace("'", "")
        elif card_name:
            # Convert card name to filename format (lowercase, underscores)
            format_args["name"] = card_name.lower().replace(" ", "_").replace("'", "")

        format_args.setdefault("name", "")

        # Format filename
        try:
            filename = self.card_format.format(**format_args)
        except KeyError as e:
            # If format key is missing (e.g., {name} but no card_name provided),
            # fall back to default format
            logger.warning(f"Missing format key {e} for theme {self.id}, falling back")
            filename = f"{suit_lower}_{num_str}.png"

        # Check for reversed variant
        if reversed and self.supports_reversed:
            base, ext = os.path.splitext(filename)
            rev_filename = f"{base}_reversed{ext}"
            rev_path = os.path.join(self.path, rev_filename)
            if os.path.exists(rev_path):
                return rev_path

        full_path = os.path.join(self.path, filename)
        return full_path if os.path.exists(full_path) else None

    def to_dict(self) -> dict:
        """Convert theme to dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Theme":
        """Create theme from dictionary."""
        return cls(**data)


class ThemeChangeHandler(FileSystemEventHandler):
    """Watchdog handler for theme folder changes."""

    def __init__(self, callback: Callable, loop: asyncio.AbstractEventLoop):
        self.callback = callback
        self._loop = loop
        self._scheduled = False

    def on_any_event(self, event):
        """Handle any filesystem event."""
        if event.is_directory:
            return

        # Only schedule one scan at a time (simple debounce)
        if not self._scheduled:
            self._scheduled = True
            # Schedule callback in the main event loop (thread-safe)
            self._loop.call_soon_threadsafe(self._trigger_scan)

    def _trigger_scan(self):
        """Reset flag and trigger scan."""
        self._scheduled = False
        asyncio.create_task(self.callback())


class ThemeManager:
    """
    Manages card themes with hot-reload support.

    Features:
    - Automatic theme discovery
    - Hot-reload without bot restart
    - User preference storage
    - Default theme fallback
    """

    DEFAULT_THEME_ID = "default"
    THEMES_DIR = "themes"
    PREFS_FILE = "data/user_themes.json"

    def __init__(self, bot=None):
        self.bot = bot
        self.themes: dict[str, Theme] = {}
        self.user_preferences: dict[str, str] = {}  # user_id -> theme_id
        self.default_theme: Optional[Theme] = None
        self._observer: Optional[Observer] = None
        self._change_callbacks: list[Callable] = []
        self._prefs_loaded_from: Optional[str] = None

        # Ensure directories exist
        os.makedirs(self.THEMES_DIR, exist_ok=True)
        os.makedirs(os.path.dirname(self.PREFS_FILE), exist_ok=True)

        # Load saved preferences
        self._load_preferences()

        # Initial scan (will be run async when needed)
        # scan_themes() is called explicitly after async loop is ready

    def _ensure_default_theme(self) -> None:
        """Ensure a default theme exists in memory (and on disk)."""
        if self.default_theme is not None and self.DEFAULT_THEME_ID in self.themes:
            return

        if self.DEFAULT_THEME_ID in self.themes:
            self.default_theme = self.themes[self.DEFAULT_THEME_ID]
            return

        self._create_default_theme()

    def start_watching(self):
        """Start watching for theme changes."""
        if self._observer:
            return

        # Get the current event loop (must be called from async context)
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            logger.warning("No running event loop, theme watching disabled")
            return

        handler = ThemeChangeHandler(self.scan_themes, loop)
        self._observer = Observer()
        self._observer.schedule(handler, self.THEMES_DIR, recursive=True)
        self._observer.start()
        logger.info(f"Started watching theme directory: {self.THEMES_DIR}")

    def stop_watching(self):
        """Stop watching for theme changes."""
        if self._observer:
            self._observer.stop()
            self._observer.join()
            self._observer = None
            logger.info("Stopped watching theme directory")

    async def scan_themes(self) -> list[Theme]:
        """
        Scan themes directory and load all valid themes.

        Returns list of newly discovered themes.
        """
        discovered: list[Theme] = []
        previous_themes = set(self.themes.keys())
        found_theme_ids: set[str] = set()

        themes_path = Path(self.THEMES_DIR)
        if not themes_path.exists():
            themes_path.mkdir(parents=True, exist_ok=True)

        for theme_dir in themes_path.iterdir():
            if not theme_dir.is_dir():
                continue

            theme_id = theme_dir.name

            # Skip hidden folders
            if theme_id.startswith("."):
                continue

            try:
                theme = self._load_theme_from_folder(theme_dir)
                if theme:
                    is_new = theme_id not in self.themes
                    self.themes[theme_id] = theme
                    found_theme_ids.add(theme_id)

                    if theme.is_default:
                        self.default_theme = theme

                    if is_new:
                        discovered.append(theme)
                        logger.info(f"Discovered new theme: {theme.name} ({theme_id})")
            except Exception as e:
                logger.error(f"Failed to load theme {theme_id}: {e}")

        # Check for removed themes
        removed = previous_themes - found_theme_ids
        for theme_id in removed:
            if self.default_theme and self.default_theme.id == theme_id:
                self.default_theme = None
            del self.themes[theme_id]
            logger.info(f"Removed theme: {theme_id}")

        # Ensure we have a default
        if not self.default_theme:
            self._create_default_theme()

        # Notify callbacks
        for callback in self._change_callbacks:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback()
                else:
                    callback()
            except Exception as e:
                logger.error(f"Theme change callback error: {e}")

        return discovered

    def _load_theme_from_folder(self, folder: Path) -> Optional[Theme]:
        """Load a theme from a folder."""
        theme_id = folder.name

        # Look for theme.json metadata
        metadata_file = folder / "theme.json"
        if metadata_file.exists():
            with open(metadata_file, "r", encoding="utf-8") as f:
                metadata = json.load(f)

            return Theme(
                id=theme_id,
                name=metadata.get("name", theme_id.replace("_", " ").title()),
                description=metadata.get("description", ""),
                author=metadata.get("author", "Unknown"),
                version=metadata.get("version", "1.0.0"),
                path=str(folder),
                card_format=metadata.get("card_format", "{suit}_{number}.png"),
                supports_reversed=metadata.get("supports_reversed", False),
                preview_image=metadata.get("preview_image"),
                is_default=metadata.get("is_default", False),
                metadata=metadata.get("extra", {}),
            )

        # Auto-detect theme without metadata
        # Check for card images
        card_files = list(folder.glob("*.png")) + list(folder.glob("*.jpg"))
        if len(card_files) >= 10:  # Assume it's a theme if it has images
            return Theme(
                id=theme_id,
                name=theme_id.replace("_", " ").title(),
                description=f"Auto-detected theme with {len(card_files)} cards",
                author="Unknown",
                version="1.0.0",
                path=str(folder),
                is_default=(theme_id == self.DEFAULT_THEME_ID),
            )

        return None

    def _create_default_theme(self) -> None:
        """Create the default/basic theme."""
        default_path = Path(self.THEMES_DIR) / self.DEFAULT_THEME_ID
        default_path.mkdir(exist_ok=True)

        # Create theme.json for default
        metadata = {
            "name": "Classic Rider-Waite",
            "description": (
                "The iconic Rider-Waite-Smith tarot deck featuring Pamela Colman Smith's "
                "visionary artwork from 1909. Rich with Golden Dawn symbolism and the first "
                "deck to feature illustrated pip cards."
            ),
            "author": "Pamela Colman Smith (original)",
            "version": "1.0.0",
            "card_format": "{suit}_{number}.png",
            "supports_reversed": False,
            "is_default": True,
            "extra": {
                "style": "traditional",
                "colors": ["gold", "blue", "red", "green"],
                "artist": "Pamela Colman Smith (original)",
                "year": "1909 (original)",
                "symbolism": "Golden Dawn tradition",
            },
        }

        metadata_file = default_path / "theme.json"
        with open(metadata_file, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2)

        theme = Theme(
            id=self.DEFAULT_THEME_ID,
            name=metadata["name"],
            description=metadata["description"],
            author=metadata["author"],
            version=metadata["version"],
            path=str(default_path),
            card_format=metadata["card_format"],
            supports_reversed=metadata["supports_reversed"],
            is_default=True,
            metadata=metadata["extra"],
        )

        self.themes[self.DEFAULT_THEME_ID] = theme
        self.default_theme = theme
        logger.info("Created default theme")

    def get_theme(self, theme_id: str) -> Optional[Theme]:
        """Get a theme by ID."""
        return self.themes.get(theme_id)

    def get_user_theme(self, user_id: str) -> Theme:
        """Get the theme for a specific user."""
        self._ensure_preferences_loaded()
        self._ensure_default_theme()
        theme_id = self.user_preferences.get(str(user_id))
        if theme_id and theme_id in self.themes:
            return self.themes[theme_id]
        return self.default_theme

    def set_user_theme(self, user_id: str, theme_id: str) -> bool:
        """Set a user's preferred theme."""
        self._ensure_preferences_loaded()
        if theme_id == self.DEFAULT_THEME_ID:
            self._ensure_default_theme()
        if theme_id not in self.themes:
            return False

        self.user_preferences[str(user_id)] = theme_id
        self._save_preferences()
        logger.info(f"User {user_id} selected theme: {theme_id}")
        return True

    def has_selected_theme(self, user_id: str) -> bool:
        """Check if a user has selected a theme."""
        self._ensure_preferences_loaded()
        return str(user_id) in self.user_preferences

    def get_available_themes(self) -> list[Theme]:
        """Get list of all available themes."""
        return list(self.themes.values())

    def get_card_image_path(
        self, user_id: str, suit: str, number: int, reversed: bool = False
    ) -> Optional[str]:
        """
        Get the image path for a specific card for a user.

        Falls back to default theme if user's theme doesn't have the card.
        """
        self._ensure_default_theme()
        theme = self.get_user_theme(user_id)
        card_name = self._resolve_card_name(suit, number)

        # Try user's theme first
        path = theme.get_card_path(suit, number, reversed, card_name=card_name)
        if path:
            return path

        # Fall back to default if different theme
        if theme.id != self.default_theme.id:
            path = self.default_theme.get_card_path(suit, number, reversed, card_name=card_name)
            if path:
                return path

        return None

    def _load_preferences(self):
        """Load user theme preferences from file."""
        if self._prefs_loaded_from == self.PREFS_FILE:
            return
        if os.path.exists(self.PREFS_FILE):
            try:
                with open(self.PREFS_FILE, "r", encoding="utf-8") as f:
                    self.user_preferences = json.load(f)
                logger.info(f"Loaded preferences for {len(self.user_preferences)} users")
            except Exception as e:
                logger.error(f"Failed to load preferences: {e}")
                self.user_preferences = {}
        self._prefs_loaded_from = self.PREFS_FILE

    def _save_preferences(self):
        """Save user theme preferences to file."""
        try:
            with open(self.PREFS_FILE, "w", encoding="utf-8") as f:
                json.dump(self.user_preferences, f, indent=2)
            self._prefs_loaded_from = self.PREFS_FILE
        except Exception as e:
            logger.error(f"Failed to save preferences: {e}")

    def _ensure_preferences_loaded(self) -> None:
        if self._prefs_loaded_from != self.PREFS_FILE:
            self._load_preferences()

    def _resolve_card_name(self, suit: str, number: int) -> Optional[str]:
        """Best-effort resolve a card name from suit/number."""
        try:
            from .data import TAROT_DECK, CardSuit

            suit_lower = suit.lower()
            suit_map = {
                "major": CardSuit.MAJOR,
                "wands": CardSuit.WANDS,
                "cups": CardSuit.CUPS,
                "swords": CardSuit.SWORDS,
                "pentacles": CardSuit.PENTACLES,
            }
            suit_enum = suit_map.get(suit_lower)
            if suit_enum is None:
                return None

            for card in TAROT_DECK:
                if card.suit == suit_enum and card.number == number:
                    return card.name
        except Exception:
            return None
        return None

    def on_theme_change(self, callback: Callable):
        """Register a callback for theme changes."""
        self._change_callbacks.append(callback)

    def get_theme_stats(self) -> dict:
        """Get statistics about themes and user preferences."""
        theme_usage = {}
        for theme_id in self.user_preferences.values():
            theme_usage[theme_id] = theme_usage.get(theme_id, 0) + 1

        return {
            "total_themes": len(self.themes),
            "total_users_with_preference": len(self.user_preferences),
            "theme_usage": theme_usage,
            "default_theme": self.default_theme.id if self.default_theme else None,
        }


# Global theme manager instance
theme_manager: Optional[ThemeManager] = None


def get_theme_manager(bot=None) -> ThemeManager:
    """Get or create the global theme manager instance."""
    global theme_manager
    if theme_manager is None:
        theme_manager = ThemeManager(bot)
    return theme_manager
