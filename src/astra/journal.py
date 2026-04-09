"""
Personal Reading Journal System
===============================
IMPLEMENTATION BY: Emma (Backend Lead)

Allows users to save and retrieve their tarot readings.
Each user has their own private journal.
"""

import json
import os
from datetime import datetime
from typing import Optional, List, Dict
from dataclasses import dataclass, asdict
import logging

logger = logging.getLogger(__name__)


@dataclass
class JournalEntry:
    """Represents a saved journal entry."""
    entry_id: int
    user_id: str
    timestamp: str
    spread_type: str
    question: Optional[str]
    cards: List[Dict]
    interpretation: Optional[str] = None
    notes: Optional[str] = None
    
    def to_dict(self) -> Dict:
        """Convert entry to dictionary."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> "JournalEntry":
        """Create entry from dictionary."""
        return cls(**data)


class JournalManager:
    """
    Manages personal reading journals for users.
    
    Each user has their own isolated journal stored in a JSON file.
    """
    
    JOURNAL_DIR = "data/journals"
    MAX_ENTRIES_PER_USER = 100  # Prevent abuse
    
    def __init__(self):
        """Initialize the journal manager."""
        os.makedirs(self.JOURNAL_DIR, exist_ok=True)
        logger.info(f"Journal manager initialized. Directory: {self.JOURNAL_DIR}")
    
    def _get_journal_path(self, user_id: str) -> str:
        """Get the file path for a user's journal."""
        # Sanitize user_id to prevent path traversal
        safe_user_id = str(user_id).replace("/", "_").replace("\\", "_")
        return os.path.join(self.JOURNAL_DIR, f"{safe_user_id}.json")
    
    def _load_journal(self, user_id: str) -> List[Dict]:
        """Load a user's journal from disk."""
        path = self._get_journal_path(user_id)
        
        if not os.path.exists(path):
            return []
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            logger.error(f"Failed to load journal for user {user_id}: {e}")
            return []
    
    def _save_journal(self, user_id: str, entries: List[Dict]) -> bool:
        """Save a user's journal to disk."""
        path = self._get_journal_path(user_id)
        
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(entries, f, indent=2, default=str)
            return True
        except IOError as e:
            logger.error(f"Failed to save journal for user {user_id}: {e}")
            return False
    
    def save_reading(
        self,
        user_id: str,
        spread_type: str,
        question: Optional[str],
        cards: List[Dict],
        interpretation: Optional[str] = None,
        notes: Optional[str] = None
    ) -> Optional[JournalEntry]:
        """
        Save a reading to the user's journal.
        
        Returns the created entry, or None if save failed.
        """
        user_id = str(user_id)
        
        # Load existing entries
        entries = self._load_journal(user_id)
        
        # Check limit
        if len(entries) >= self.MAX_ENTRIES_PER_USER:
            logger.warning(f"User {user_id} reached journal limit ({self.MAX_ENTRIES_PER_USER})")
            return None
        
        # Create new entry
        entry_id = len(entries) + 1
        entry = JournalEntry(
            entry_id=entry_id,
            user_id=user_id,
            timestamp=datetime.now().isoformat(),
            spread_type=spread_type,
            question=question,
            cards=cards,
            interpretation=interpretation,
            notes=notes
        )
        
        # Add to entries
        entries.append(entry.to_dict())
        
        # Save
        if self._save_journal(user_id, entries):
            logger.info(f"Saved entry {entry_id} for user {user_id}")
            return entry
        
        return None
    
    def get_user_readings(self, user_id: str) -> List[JournalEntry]:
        """Get all readings for a user, newest first."""
        user_id = str(user_id)
        entries = self._load_journal(user_id)
        
        # Convert to JournalEntry objects, newest first
        journal_entries = [JournalEntry.from_dict(e) for e in entries]
        journal_entries.reverse()  # Newest first
        
        return journal_entries
    
    def get_entry(self, user_id: str, entry_id: int) -> Optional[JournalEntry]:
        """Get a specific entry by ID."""
        user_id = str(user_id)
        entries = self._load_journal(user_id)
        
        for entry_data in entries:
            if entry_data.get('entry_id') == entry_id:
                return JournalEntry.from_dict(entry_data)
        
        return None
    
    def delete_entry(self, user_id: str, entry_id: int) -> bool:
        """Delete a specific entry."""
        user_id = str(user_id)
        entries = self._load_journal(user_id)
        
        # Find and remove entry
        new_entries = [e for e in entries if e.get('entry_id') != entry_id]
        
        if len(new_entries) == len(entries):
            return False  # Entry not found
        
        # Re-number remaining entries
        for i, entry in enumerate(new_entries, 1):
            entry['entry_id'] = i
        
        return self._save_journal(user_id, new_entries)
    
    def clear_journal(self, user_id: str) -> bool:
        """Clear all entries for a user. Use with caution!"""
        user_id = str(user_id)
        path = self._get_journal_path(user_id)
        
        try:
            if os.path.exists(path):
                os.remove(path)
            logger.info(f"Cleared journal for user {user_id}")
            return True
        except IOError as e:
            logger.error(f"Failed to clear journal for user {user_id}: {e}")
            return False
    
    def get_stats(self, user_id: str) -> Dict:
        """Get statistics for a user's journal."""
        user_id = str(user_id)
        entries = self._load_journal(user_id)
        
        if not entries:
            return {
                "total_readings": 0,
                "most_common_spread": None,
                "first_reading": None,
                "latest_reading": None
            }
        
        # Count spreads
        spread_counts = {}
        for entry in entries:
            spread = entry.get('spread_type', 'unknown')
            spread_counts[spread] = spread_counts.get(spread, 0) + 1
        
        most_common = max(spread_counts, key=spread_counts.get)
        
        return {
            "total_readings": len(entries),
            "most_common_spread": most_common,
            "first_reading": entries[0].get('timestamp'),
            "latest_reading": entries[-1].get('timestamp')
        }
    
    def search_readings(
        self,
        user_id: str,
        query: str,
        spread_type: Optional[str] = None
    ) -> List[JournalEntry]:
        """Search user's readings by keyword."""
        user_id = str(user_id)
        entries = self._load_journal(user_id)
        query_lower = query.lower()
        
        results = []
        for entry_data in entries:
            # Check spread type filter
            if spread_type and entry_data.get('spread_type') != spread_type:
                continue
            
            # Search in question, notes, and card names
            searchable_text = ""
            
            if entry_data.get('question'):
                searchable_text += entry_data['question'].lower() + " "
            
            if entry_data.get('notes'):
                searchable_text += entry_data['notes'].lower() + " "
            
            for card in entry_data.get('cards', []):
                searchable_text += card.get('name', '').lower() + " "
            
            if query_lower in searchable_text:
                results.append(JournalEntry.from_dict(entry_data))
        
        # Return newest first
        results.reverse()
        return results


# Global journal manager instance
_journal_manager: Optional[JournalManager] = None


def get_journal_manager() -> JournalManager:
    """Get or create the global journal manager instance."""
    global _journal_manager
    if _journal_manager is None:
        _journal_manager = JournalManager()
    return _journal_manager
