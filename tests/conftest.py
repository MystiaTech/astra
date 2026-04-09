"""
Pytest Configuration
====================
QA: Chloe

Fixtures and configuration for testing.
"""

import pytest
import pytest_asyncio


@pytest.fixture
def sample_deck():
    """Provide the full tarot deck for tests."""
    from astra.data import TAROT_DECK
    return TAROT_DECK


@pytest.fixture
def sample_spreads():
    """Provide all spreads for tests."""
    from astra.data import SPREADS
    return SPREADS


@pytest.fixture
def major_arcana_cards():
    """Provide only Major Arcana cards."""
    from astra.data import TAROT_DECK, CardSuit
    return [c for c in TAROT_DECK if c.suit == CardSuit.MAJOR]


@pytest.fixture
def minor_arcana_cards():
    """Provide only Minor Arcana cards."""
    from astra.data import TAROT_DECK, CardSuit
    return [c for c in TAROT_DECK if c.suit != CardSuit.MAJOR]
