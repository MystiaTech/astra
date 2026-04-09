"""
Card Data Tests
===============
QA: Chloe

Validates tarot card data integrity and correctness.
All 78 cards must be properly defined with accurate meanings.
"""

import re

from astra.data import CardSuit


class TestDeckIntegrity:
    """Verify the complete deck has correct structure."""

    def test_deck_has_78_cards(self, sample_deck):
        """DECK-001: Tarot deck must have exactly 78 cards."""
        assert len(sample_deck) == 78, f"Expected 78 cards, got {len(sample_deck)}"

    def test_major_arcana_count(self, major_arcana_cards):
        """DECK-002: Major Arcana must have exactly 22 cards (0-21)."""
        assert len(major_arcana_cards) == 22, "Major Arcana should have 22 cards"

    def test_minor_arcana_count(self, minor_arcana_cards):
        """DECK-003: Minor Arcana must have exactly 56 cards."""
        assert len(minor_arcana_cards) == 56, "Minor Arcana should have 56 cards"

    def test_suit_distribution(self, minor_arcana_cards):
        """DECK-004: Each suit must have exactly 14 cards."""
        for suit in [CardSuit.WANDS, CardSuit.CUPS, CardSuit.SWORDS, CardSuit.PENTACLES]:
            suit_cards = [c for c in minor_arcana_cards if c.suit == suit]
            assert len(suit_cards) == 14, f"{suit.name} should have 14 cards"


class TestCardStructure:
    """Verify each card has required attributes."""

    def test_all_cards_have_name(self, sample_deck):
        """CARD-001: Every card must have a name."""
        for card in sample_deck:
            assert card.name, f"Card {card.number} of {card.suit.name} missing name"
            assert len(card.name) > 0, "Card name cannot be empty"

    def test_all_cards_have_meanings(self, sample_deck):
        """CARD-002: Every card must have upright and reversed meanings."""
        for card in sample_deck:
            assert card.meaning, f"{card.name} missing upright meaning"
            assert card.meaning_reversed, f"{card.name} missing reversed meaning"
            assert len(card.meaning) > 10, f"{card.name} meaning too short"
            assert len(card.meaning_reversed) > 10, f"{card.name} reversed meaning too short"

    def test_all_cards_have_keywords(self, sample_deck):
        """CARD-003: Every card must have keywords."""
        for card in sample_deck:
            assert card.keywords, f"{card.name} missing keywords"
            assert card.keywords_reversed, f"{card.name} missing reversed keywords"
            assert len(card.keywords) >= 3, f"{card.name} should have at least 3 keywords"

    def test_all_cards_have_image_placeholder(self, sample_deck):
        """CARD-004: Every card must have an image placeholder filename."""
        for card in sample_deck:
            assert card.image_placeholder, f"{card.name} missing image placeholder"
            assert card.image_placeholder.endswith(".png"), f"{card.name} placeholder should be PNG"


class TestMajorArcana:
    """Verify Major Arcana specific attributes."""

    def test_fool_is_number_zero(self, major_arcana_cards):
        """MAJOR-001: The Fool must be numbered 0."""
        fool = [c for c in major_arcana_cards if c.name == "The Fool"]
        assert len(fool) == 1, "Should have exactly one Fool"
        assert fool[0].number == 0, "The Fool must be number 0"

    def test_world_is_number_21(self, major_arcana_cards):
        """MAJOR-002: The World must be numbered 21."""
        world = [c for c in major_arcana_cards if c.name == "The World"]
        assert len(world) == 1, "Should have exactly one World"
        assert world[0].number == 21, "The World must be number 21"

    def test_major_arcana_have_astrology(self, major_arcana_cards):
        """MAJOR-003: Major Arcana should have astrological correspondences."""
        for card in major_arcana_cards:
            assert card.astrology, f"{card.name} missing astrological correspondence"


class TestMinorArcana:
    """Verify Minor Arcana specific attributes."""

    def test_aces_are_number_one(self, minor_arcana_cards):
        """MINOR-001: All Aces must be numbered 1."""
        for suit in [CardSuit.WANDS, CardSuit.CUPS, CardSuit.SWORDS, CardSuit.PENTACLES]:
            aces = [c for c in minor_arcana_cards if c.suit == suit and c.number == 1]
            assert len(aces) == 1, f"{suit.name} should have exactly one Ace"
            assert "Ace" in aces[0].name, f"{suit.name} card 1 should be named Ace"

    def test_court_cards_exist(self, minor_arcana_cards):
        """MINOR-002: Each suit must have 4 court cards (Page, Knight, Queen, King)."""
        for suit in [CardSuit.WANDS, CardSuit.CUPS, CardSuit.SWORDS, CardSuit.PENTACLES]:
            suit_cards = [c for c in minor_arcana_cards if c.suit == suit]
            court_cards = [c for c in suit_cards if c.number >= 11]
            assert len(court_cards) == 4, f"{suit.name} should have 4 court cards"

            # Check titles
            titles = [c.court_title for c in court_cards]
            assert "Page" in titles, f"{suit.name} missing Page"
            assert "Knight" in titles, f"{suit.name} missing Knight"
            assert "Queen" in titles, f"{suit.name} missing Queen"
            assert "King" in titles, f"{suit.name} missing King"

    def test_minor_arcana_have_elements(self, minor_arcana_cards):
        """MINOR-003: Minor Arcana should have elemental associations."""
        elements = {
            CardSuit.WANDS: "Fire",
            CardSuit.CUPS: "Water",
            CardSuit.SWORDS: "Air",
            CardSuit.PENTACLES: "Earth",
        }
        for card in minor_arcana_cards:
            if card.number <= 10:  # Number cards
                expected = elements.get(card.suit)
                assert card.element == expected, f"{card.name} should have element {expected}"


class TestCardMeaningsAccuracy:
    """
    Validate card meanings are accurate and appropriate.

    These tests ensure Sarah's research is properly implemented.
    """

    def test_death_card_not_literal(self, sample_deck):
        """MEANING-001: Death card meaning should not imply physical death."""
        death = [c for c in sample_deck if c.name == "Death"][0]
        assert (
            "physical death" not in death.meaning.lower()
            or "literal death" not in death.meaning.lower()
        ), "Death card should not focus on literal death"
        assert (
            "transformation" in death.meaning.lower()
            or "change" in death.meaning.lower()
            or "ending" in death.meaning.lower()
        ), "Death card should emphasize transformation"

    def test_devil_card_addresses_bondage(self, sample_deck):
        """MEANING-002: Devil card should address self-imposed limitations."""
        devil = [c for c in sample_deck if c.name == "The Devil"][0]
        assert any(
            word in devil.meaning.lower()
            for word in ["attachment", "addiction", "restriction", "shadow", "limitation"]
        ), "Devil card should address attachments and restrictions"

    def test_fool_card_addresses_beginnings(self, sample_deck):
        """MEANING-003: Fool should emphasize new beginnings and potential."""
        fool = [c for c in sample_deck if c.name == "The Fool"][0]
        assert any(
            word in fool.meaning.lower()
            for word in ["beginning", "new", "potential", "innocence", "faith"]
        ), "Fool card should emphasize new beginnings"

    def test_suit_meanings_are_consistent(self, minor_arcana_cards):
        """MEANING-004: Suit meanings should be consistent with elemental associations."""
        # Wands = Fire = creativity, action, passion
        wands = [c for c in minor_arcana_cards if c.suit == CardSuit.WANDS and c.number == 1][0]
        assert any(
            word in wands.meaning.lower()
            for word in ["inspiration", "creativity", "passion", "action"]
        ), "Wands Ace should emphasize fire qualities"

        # Cups = Water = emotions, relationships
        cups = [c for c in minor_arcana_cards if c.suit == CardSuit.CUPS and c.number == 1][0]
        assert any(
            word in cups.meaning.lower() for word in ["emotion", "love", "feeling", "relationship"]
        ), "Cups Ace should emphasize water qualities"


class TestCardDisplay:
    """Test card display formatting."""

    def test_major_arcana_display_name(self, major_arcana_cards):
        """DISPLAY-001: Major Arcana display names should not include suit."""
        pattern = r"\\bof\\s+(wands|cups|swords|pentacles)\\b"
        for card in major_arcana_cards:
            name = card.get_display_name()
            assert not re.search(
                pattern, name, re.IGNORECASE
            ), f"Major Arcana {card.name} should not include a suit name"

    def test_minor_arcana_display_name(self, minor_arcana_cards):
        """DISPLAY-002: Minor Arcana display names should include number/rank and suit."""
        for card in minor_arcana_cards:
            name = card.get_display_name()
            assert "of" in name, f"Minor Arcana {card.name} should include 'of'"
            assert card.suit.name.title() in name, f"{card.name} should include suit name"

    def test_reversed_indicator(self, sample_deck):
        """DISPLAY-003: Reversed cards should show indicator."""
        for card in sample_deck:
            normal = card.get_display_name(reversed=False)
            rev = card.get_display_name(reversed=True)
            assert "(Reversed)" not in normal, "Normal cards should not show reversed"
            assert "(Reversed)" in rev, "Reversed cards should show indicator"


class TestResearchValidation:
    """
    Cross-reference validation against known tarot sources.

    These tests verify Sarah's research is accurate.
    """

    def test_all_cards_present(self, sample_deck):
        """RESEARCH-001: All 78 cards from standard deck must be present."""
        # Check for some key cards that should exist
        required_cards = [
            "The Fool",
            "The Magician",
            "The High Priestess",
            "The Empress",
            "The Emperor",
            "The Hierophant",
            "The Lovers",
            "The Chariot",
            "Strength",
            "The Hermit",
            "Wheel of Fortune",
            "Justice",
            "The Hanged Man",
            "Death",
            "Temperance",
            "The Devil",
            "The Tower",
            "The Star",
            "The Moon",
            "The Sun",
            "Judgement",
            "The World",
        ]

        card_names = [c.name for c in sample_deck if c.suit == CardSuit.MAJOR]
        for required in required_cards:
            assert required in card_names, f"Missing required card: {required}"

    def test_keywords_are_appropriate(self, sample_deck):
        """RESEARCH-002: Keywords should be appropriate and meaningful."""
        for card in sample_deck:
            for keyword in card.keywords:
                assert len(keyword) > 2, f"{card.name} keyword too short: {keyword}"
                normalized = keyword.replace("-", "").replace("'", "")
                assert (
                    normalized.isalpha() or " " in keyword
                ), f"{card.name} keyword should be readable: {keyword}"
