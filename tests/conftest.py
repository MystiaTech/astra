"""
Pytest Configuration
====================
QA: Chloe

Fixtures and configuration for testing.
"""

from unittest.mock import AsyncMock, MagicMock

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


@pytest_asyncio.fixture
async def bot():
    """Provide a mocked AstraBot instance for async bot tests."""
    from astra.bot import AstraBot

    bot = AstraBot()
    bot.active_session = None

    # Replace the asyncio.Lock with a mock that behaves as an async context manager
    # so tests can run without a running loop dependency.
    bot.session_lock = MagicMock()
    bot.session_lock.__aenter__ = AsyncMock(return_value=None)
    bot.session_lock.__aexit__ = AsyncMock(return_value=None)
    return bot
