"""
Theme Management System
=======================
IMPLEMENTATION BY: Emma (Backend Lead)

Dynamic theme loading with hot-reload support.
Users can select themes on first use, themes auto-detect without restart.
"""

import json
import os
import re
import asyncio
import logging
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional, Callable
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

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
    
    def get_card_path(self, suit: str, number: int, reversed: bool = False) -> Optional[str]:
        """Get the path to a specific card image."""
        suit_lower = suit.lower()
        
        # Handle special naming
        if number == 1 and suit != "major":
            num_str = "ace"
        elif number == 11:
            num_str = "page"
        elif number == 12:
            num_str = "knight"
        elif number == 13:
            num_str = "queen"
        elif number == 14:
            num_str = "king"
        else:
            num_str = f"{number:02d}"
        
        # Format filename
        filename = self.card_format.format(
            suit=suit_lower,
            number=num_str,
            num=number
        )
        
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
    
    def __init__(self, callback: Callable):
        self.callback = callback
        self._debounce_timer = None
    
    def on_any_event(self, event):
        """Handle any filesystem event."""
        if event.is_directory:
            return
        
        # Debounce rapid changes
        if self._debounce_timer:
            self._debounce_timer.cancel()
        
        loop = asyncio.get_event_loop()
        self._debounce_timer = loop.call_later(1.0, lambda: asyncio.create_task(self.callback()))


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
        
        # Ensure directories exist
        os.makedirs(self.THEMES_DIR, exist_ok=True)
        os.makedirs(os.path.dirname(self.PREFS_FILE), exist_ok=True)
        
        # Load saved preferences
        self._load_preferences()
        
        # Initial scan (will be run async when needed)
        # scan_themes() is called explicitly after async loop is ready
    
    def start_watching(self):
        """Start watching for theme changes."""
        if self._observer:
            return
        
        handler = ThemeChangeHandler(self.scan_themes)
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
        discovered = []
        previous_themes = set(self.themes.keys())
        
        themes_path = Path(self.THEMES_DIR)
        if not themes_path.exists():
            logger.warning(f"Themes directory not found: {self.THEMES_DIR}")
            return discovered
        
        for theme_dir in themes_path.iterdir():
            if not theme_dir.is_dir():
                continue
            
            theme_id = theme_dir.name
            
            # Skip hidden folders
            if theme_id.startswith('.'):
                continue
            
            try:
                theme = self._load_theme_from_folder(theme_dir)
                if theme:
                    is_new = theme_id not in self.themes
                    self.themes[theme_id] = theme
                    
                    if theme.is_default:
                        self.default_theme = theme
                    
                    if is_new:
                        discovered.append(theme)
                        logger.info(f"Discovered new theme: {theme.name} ({theme_id})")
            except Exception as e:
                logger.error(f"Failed to load theme {theme_id}: {e}")
        
        # Check for removed themes
        current_themes = set(self.themes.keys())
        removed = previous_themes - current_themes
        for theme_id in removed:
            del self.themes[theme_id]
            logger.info(f"Removed theme: {theme_id}")
        
        # Ensure we have a default
        if not self.default_theme:
            await self._create_default_theme()
        
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
            with open(metadata_file, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            
            return Theme(
                id=theme_id,
                name=metadata.get('name', theme_id.replace('_', ' ').title()),
                description=metadata.get('description', ''),
                author=metadata.get('author', 'Unknown'),
                version=metadata.get('version', '1.0.0'),
                path=str(folder),
                card_format=metadata.get('card_format', '{suit}_{number}.png'),
                supports_reversed=metadata.get('supports_reversed', False),
                preview_image=metadata.get('preview_image'),
                is_default=metadata.get('is_default', False),
                metadata=metadata.get('extra', {})
            )
        
        # Auto-detect theme without metadata
        # Check for card images
        card_files = list(folder.glob('*.png')) + list(folder.glob('*.jpg'))
        if len(card_files) >= 10:  # Assume it's a theme if it has images
            return Theme(
                id=theme_id,
                name=theme_id.replace('_', ' ').title(),
                description=f"Auto-detected theme with {len(card_files)} cards",
                author="Unknown",
                version="1.0.0",
                path=str(folder),
                is_default=(theme_id == self.DEFAULT_THEME_ID)
            )
        
        return None
    
    async def _create_default_theme(self):
        """Create the default/basic theme."""
        default_path = Path(self.THEMES_DIR) / self.DEFAULT_THEME_ID
        default_path.mkdir(exist_ok=True)
        
        # Create theme.json for default
        metadata = {
            "name": "Classic Rider-Waite",
            "description": "Traditional tarot imagery based on the Rider-Waite-Smith deck",
            "author": "Team Astra",
            "version": "1.0.0",
            "card_format": "{suit}_{number}.png",
            "supports_reversed": False,
            "is_default": True,
            "extra": {
                "style": "traditional",
                "colors": ["gold", "blue", "red"]
            }
        }
        
        metadata_file = default_path / "theme.json"
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)
        
        theme = Theme(
            id=self.DEFAULT_THEME_ID,
            name=metadata['name'],
            description=metadata['description'],
            author=metadata['author'],
            version=metadata['version'],
            path=str(default_path),
            card_format=metadata['card_format'],
            supports_reversed=metadata['supports_reversed'],
            is_default=True,
            metadata=metadata['extra']
        )
        
        self.themes[self.DEFAULT_THEME_ID] = theme
        self.default_theme = theme
        logger.info("Created default theme")
    
    def get_theme(self, theme_id: str) -> Optional[Theme]:
        """Get a theme by ID."""
        return self.themes.get(theme_id)
    
    def get_user_theme(self, user_id: str) -> Theme:
        """Get the theme for a specific user."""
        theme_id = self.user_preferences.get(str(user_id))
        if theme_id and theme_id in self.themes:
            return self.themes[theme_id]
        return self.default_theme
    
    def set_user_theme(self, user_id: str, theme_id: str) -> bool:
        """Set a user's preferred theme."""
        if theme_id not in self.themes:
            return False
        
        self.user_preferences[str(user_id)] = theme_id
        self._save_preferences()
        logger.info(f"User {user_id} selected theme: {theme_id}")
        return True
    
    def has_selected_theme(self, user_id: str) -> bool:
        """Check if a user has selected a theme."""
        return str(user_id) in self.user_preferences
    
    def get_available_themes(self) -> list[Theme]:
        """Get list of all available themes."""
        return list(self.themes.values())
    
    def get_card_image_path(
        self, 
        user_id: str, 
        suit: str, 
        number: int, 
        reversed: bool = False
    ) -> Optional[str]:
        """
        Get the image path for a specific card for a user.
        
        Falls back to default theme if user's theme doesn't have the card.
        """
        theme = self.get_user_theme(user_id)
        
        # Try user's theme first
        path = theme.get_card_path(suit, number, reversed)
        if path:
            return path
        
        # Fall back to default if different theme
        if theme.id != self.default_theme.id:
            path = self.default_theme.get_card_path(suit, number, reversed)
            if path:
                return path
        
        return None
    
    def _load_preferences(self):
        """Load user theme preferences from file."""
        if os.path.exists(self.PREFS_FILE):
            try:
                with open(self.PREFS_FILE, 'r', encoding='utf-8') as f:
                    self.user_preferences = json.load(f)
                logger.info(f"Loaded preferences for {len(self.user_preferences)} users")
            except Exception as e:
                logger.error(f"Failed to load preferences: {e}")
                self.user_preferences = {}
    
    def _save_preferences(self):
        """Save user theme preferences to file."""
        try:
            with open(self.PREFS_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.user_preferences, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save preferences: {e}")
    
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
