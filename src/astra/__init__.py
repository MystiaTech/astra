"""
🔮 Astra - Tarot Reading Discord Bot
A focused, single-session tarot reading experience for Discord.
"""

__version__ = "1.0.0"
__author__ = "Team Astra"

from .bot import AstraBot
from .data import SPREADS, TAROT_DECK, Card, Spread
from .reading import Reading, ReadingResult, ReadingSession

__all__ = [
    "AstraBot",
    "TAROT_DECK",
    "SPREADS",
    "Card",
    "Spread",
    "Reading",
    "ReadingResult",
    "ReadingSession",
]
