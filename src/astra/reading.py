"""
Reading Session and Result Models
=================================
IMPLEMENTATION BY: Emma (Backend Lead)

Data models for tarot reading sessions and results.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional

from .data import Card


@dataclass
class ReadingResult:
    """
    Represents a single card result in a reading.

    Attributes:
        card: The tarot card drawn
        position: Position in the spread (1-indexed)
        reversed: Whether the card is reversed
    """

    card: Card
    position: int
    reversed: bool = False

    def get_interpretation(self) -> str:
        """Get the interpretation for this card based on orientation."""
        if self.reversed:
            return self.card.meaning_reversed
        return self.card.meaning

    def get_keywords(self) -> list[str]:
        """Get keywords for this card based on orientation."""
        if self.reversed:
            return self.card.keywords_reversed
        return self.card.keywords


@dataclass
class Reading:
    """
    Represents a complete tarot reading.

    Attributes:
        spread_type: Type of spread used
        question: Optional question asked
        results: List of card results
        timestamp: When the reading was performed
    """

    spread_type: str
    question: Optional[str]
    results: list[ReadingResult]
    timestamp: datetime = field(default_factory=datetime.now)

    def get_card_at_position(self, position: int) -> Optional[ReadingResult]:
        """Get the card result at a specific position."""
        for result in self.results:
            if result.position == position:
                return result
        return None

    def has_major_arcana(self) -> bool:
        """Check if any Major Arcana cards were drawn."""
        return any(r.card.is_major for r in self.results)

    def count_reversed(self) -> int:
        """Count number of reversed cards."""
        return sum(1 for r in self.results if r.reversed)

    def get_dominant_suit(self) -> Optional[str]:
        """Get the most common suit in the reading."""
        from collections import Counter

        suits = [r.card.suit.name for r in self.results]
        if not suits:
            return None
        return Counter(suits).most_common(1)[0][0]


@dataclass
class ReadingSession:
    """
    Represents an active reading session.

    Used for managing the "one user at a time" constraint.

    Attributes:
        user_id: Discord user ID
        username: Discord username
        spread_type: Type of spread being used
        started_at: When the session began
    """

    user_id: int
    username: str
    spread_type: str
    started_at: datetime

    def is_expired(self, timeout_seconds: int = 300) -> bool:
        """Check if the session has exceeded the timeout."""
        elapsed = datetime.now() - self.started_at
        return elapsed > timedelta(seconds=timeout_seconds)

    def elapsed_seconds(self) -> int:
        """Get elapsed time in seconds."""
        return int((datetime.now() - self.started_at).total_seconds())

    def time_remaining(self, timeout_seconds: int = 300) -> int:
        """Get remaining time in seconds."""
        elapsed = self.elapsed_seconds()
        return max(0, timeout_seconds - elapsed)
