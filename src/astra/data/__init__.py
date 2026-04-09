"""Tarot data module - researched and validated by Sarah."""

from .cards import TAROT_DECK, Card, CardSuit
from .spreads import SPREADS, Spread, SpreadPosition

__all__ = [
    "TAROT_DECK",
    "Card",
    "CardSuit",
    "SPREADS",
    "Spread",
    "SpreadPosition",
]
