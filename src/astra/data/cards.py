"""
Tarot Card Definitions
======================
RESEARCH BY: Sarah (Research Lead)
VALIDATED: All meanings cross-referenced with Rider-Waite-Smith tradition
and modern tarot interpretation sources.

Sources consulted:
- Rider-Waite-Smith deck (Pamela Colman Smith illustrations)
- "Seventy-Eight Degrees of Wisdom" by Rachel Pollack
- "The Ultimate Guide to Tarot" by Liz Dean
- "Learning the Tarot" by Joan Bunning
"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional


class CardSuit(Enum):
    """The four suits of the Minor Arcana plus Major Arcana."""

    MAJOR = auto()  # Major Arcana - life lessons, karmic influences
    WANDS = auto()  # Fire - passion, creativity, action
    CUPS = auto()  # Water - emotions, relationships, intuition
    SWORDS = auto()  # Air - intellect, conflict, decisions
    PENTACLES = auto()  # Earth - material world, finances, body


@dataclass(frozen=True)
class Card:
    """
    Represents a single Tarot card.

    Attributes:
        number: Card number (0-21 for Major, 1-14 for Minor where 11-14 are courts)
        suit: The card's suit
        name: Full card name
        keywords: Core meanings for upright position
        keywords_reversed: Core meanings for reversed position
        meaning: Detailed upright interpretation
        meaning_reversed: Detailed reversed interpretation
        element: Associated element (for Minor Arcana)
        astrology: Associated astrological correspondence
        image_placeholder: Filename for placeholder image
    """

    number: int
    suit: CardSuit
    name: str
    keywords: list[str]
    keywords_reversed: list[str]
    meaning: str
    meaning_reversed: str
    element: Optional[str] = None
    astrology: Optional[str] = None
    image_placeholder: str = ""

    @property
    def is_major(self) -> bool:
        """Check if this is a Major Arcana card."""
        return self.suit == CardSuit.MAJOR

    @property
    def is_court(self) -> bool:
        """Check if this is a court card (Page, Knight, Queen, King)."""
        return self.number >= 11 and self.suit != CardSuit.MAJOR

    @property
    def court_title(self) -> Optional[str]:
        """Get the court title if applicable."""
        if not self.is_court:
            return None
        titles = {11: "Page", 12: "Knight", 13: "Queen", 14: "King"}
        return titles.get(self.number)

    def get_display_name(self, reversed: bool = False) -> str:
        """Get formatted display name with optional reversed indicator."""
        suffix = " (Reversed)" if reversed else ""
        if self.is_major:
            return f"{self.name}{suffix}"
        elif self.is_court:
            return f"{self.court_title} of {self.suit.name.title()}{suffix}"
        else:
            # Number cards
            num_display = {1: "Ace", 11: "Page", 12: "Knight", 13: "Queen", 14: "King"}
            num_str = num_display.get(self.number, str(self.number))
            return f"{num_str} of {self.suit.name.title()}{suffix}"


# =============================================================================
# MAJOR ARCANA (0-21)
# =============================================================================
# The Fool's Journey - from innocence to integration

MAJOR_ARCANA = [
    Card(
        number=0,
        suit=CardSuit.MAJOR,
        name="The Fool",
        keywords=["beginnings", "innocence", "spontaneity", "free spirit"],
        keywords_reversed=["recklessness", "risk-taking", "foolishness", "naivety"],
        meaning=(
            "The Fool represents new beginnings, having faith in the future, being inexperienced, "
            "not knowing what to expect, having beginner's luck, improvisation, believing in "
            "the universe, having no commitments, being carefree, having an open heart, "
            "trusting the flow, taking a leap of faith, being in the present moment."
        ),
        meaning_reversed=(
            "Reversed, The Fool warns against recklessness, taking unnecessary risks, "
            "being foolish, lacking judgment, being naive, falling prey to deception, "
            "not thinking before acting, ignoring consequences, being irresponsible, "
            "or missing important details through carelessness."
        ),
        astrology="Uranus",
        image_placeholder="major_00_fool.png",
    ),
    Card(
        number=1,
        suit=CardSuit.MAJOR,
        name="The Magician",
        keywords=["manifestation", "resourcefulness", "power", "inspired action"],
        keywords_reversed=["manipulation", "poor planning", "untapped talents", "trickery"],
        meaning=(
            "The Magician represents manifestation, resourcefulness, power, inspired action, "
            "channeling energy, having all tools needed, confidence, creativity, "
            "the ability to transform, willpower, concentration, using skills effectively, "
            "taking initiative, making things happen, being in control."
        ),
        meaning_reversed=(
            "Reversed, The Magician indicates manipulation, poor planning, untapped talents, "
            "deception, trickery, greed, misuse of power, lack of confidence, "
            "wasted potential, manipulation of others for selfish gain, or illusions."
        ),
        astrology="Mercury",
        image_placeholder="major_01_magician.png",
    ),
    Card(
        number=2,
        suit=CardSuit.MAJOR,
        name="The High Priestess",
        keywords=["intuition", "sacred knowledge", "divine feminine", "subconscious"],
        keywords_reversed=["secrets", "disconnected from intuition", "withdrawal", "silence"],
        meaning=(
            "The High Priestess represents intuition, sacred knowledge, divine feminine, "
            "the subconscious mind, mystery, inner wisdom, spiritual insight, "
            "the space between worlds, hidden knowledge, patience, stillness, "
            "listening to inner voice, dreams, psychic abilities, the unknown."
        ),
        meaning_reversed=(
            "Reversed, The High Priestess suggests secrets, being disconnected from intuition, "
            "withdrawal, silence that hides truth, hidden agendas, repressed intuition, "
            "ignoring inner voice, surface-level understanding, or information being withheld."
        ),
        astrology="The Moon",
        image_placeholder="major_02_high_priestess.png",
    ),
    Card(
        number=3,
        suit=CardSuit.MAJOR,
        name="The Empress",
        keywords=["femininity", "beauty", "nature", "nurturing", "abundance"],
        keywords_reversed=["creative block", "dependence", "smothering", "emptiness"],
        meaning=(
            "The Empress represents femininity, beauty, nature, nurturing, abundance, "
            "fertility, creativity, maternal care, sensual pleasure, connection to earth, "
            "growth, harvest, artistic expression, comfort, luxury, natural cycles."
        ),
        meaning_reversed=(
            "Reversed, The Empress indicates creative blocks, dependence on others, "
            "smothering love, emptiness, infertility (literal or metaphorical), "
            "neglect of self-care, stifled creativity, overbearing behavior, "
            "or disconnection from nature."
        ),
        astrology="Venus",
        image_placeholder="major_03_empress.png",
    ),
    Card(
        number=4,
        suit=CardSuit.MAJOR,
        name="The Emperor",
        keywords=["authority", "structure", "father figure", "control", "stability"],
        keywords_reversed=["tyranny", "rigidity", "coldness", "domination", "chaos"],
        meaning=(
            "The Emperor represents authority, structure, father figure, control, stability, "
            "logic, discipline, leadership, creating order, setting boundaries, "
            "protection, practical wisdom, rules and systems, fatherhood, "
            "achievement through structure, strategic planning."
        ),
        meaning_reversed=(
            "Reversed, The Emperor warns of tyranny, rigidity, coldness, domination, "
            "chaos, lack of discipline, authoritarian abuse, inflexibility, "
            "overbearing control, or collapse of structure."
        ),
        astrology="Aries",
        image_placeholder="major_04_emperor.png",
    ),
    Card(
        number=5,
        suit=CardSuit.MAJOR,
        name="The Hierophant",
        keywords=["tradition", "conformity", "institutions", "spiritual wisdom", "belief"],
        keywords_reversed=["rebellion", "subversiveness", "freedom", "personal beliefs"],
        meaning=(
            "The Hierophant represents tradition, conformity, institutions, spiritual wisdom, "
            "religious beliefs, education, seeking guidance, conventional approach, "
            "marriage or commitment, mentorship, spiritual teaching, "
            "honoring customs, community values, established systems."
        ),
        meaning_reversed=(
            "Reversed, The Hierophant suggests rebellion, subversiveness, freedom from tradition, "
            "personal beliefs over dogma, nonconformity, challenging authority, "
            "breaking rules, alternative approaches, or institutional corruption."
        ),
        astrology="Taurus",
        image_placeholder="major_05_hierophant.png",
    ),
    Card(
        number=6,
        suit=CardSuit.MAJOR,
        name="The Lovers",
        keywords=["love", "harmony", "choices", "values alignment", "partnership"],
        keywords_reversed=["disharmony", "imbalance", "conflict", "avoiding choices"],
        meaning=(
            "The Lovers represent love, harmony, relationships, choices, values alignment, "
            "partnership, union, meaningful connections, important decisions, "
            "commitment, mutual attraction, balance, coming together, "
            "alignment of heart and mind, soul connections."
        ),
        meaning_reversed=(
            "Reversed, The Lovers indicate disharmony, imbalance in relationships, "
            "conflict, avoiding important choices, misaligned values, "
            "temptation, codependency, difficult decisions, or separation."
        ),
        astrology="Gemini",
        image_placeholder="major_06_lovers.png",
    ),
    Card(
        number=7,
        suit=CardSuit.MAJOR,
        name="The Chariot",
        keywords=["control", "willpower", "victory", "determination", "action"],
        keywords_reversed=["lack of control", "aggression", "defeat", "self-discipline"],
        meaning=(
            "The Chariot represents control, willpower, victory, determination, action, "
            "overcoming obstacles, confidence, forward momentum, triumph, "
            "harnessing opposing forces, focus, ambition, self-assertion, "
            "overcoming challenges through will."
        ),
        meaning_reversed=(
            "Reversed, The Chariot warns of lack of control, aggression, defeat, "
            "lack of direction, losing focus, obstacles overwhelming you, "
            "internal conflict, need for self-discipline, or giving up too soon."
        ),
        astrology="Cancer",
        image_placeholder="major_07_chariot.png",
    ),
    Card(
        number=8,
        suit=CardSuit.MAJOR,
        name="Strength",
        keywords=["courage", "persuasion", "influence", "compassion", "inner strength"],
        keywords_reversed=["self-doubt", "weakness", "insecurity", "raw emotion"],
        meaning=(
            "Strength represents courage, persuasion, influence, compassion, inner strength, "
            "patience, gentle control, mastering emotions, taming inner beasts, "
            "fortitude, self-confidence, calm power, resilience, "
            "overcoming through understanding rather than force."
        ),
        meaning_reversed=(
            "Reversed, Strength indicates self-doubt, weakness, insecurity, "
            "raw emotion, impatience, lack of courage, being overwhelmed, "
            "feeling inadequate, giving in to impulses, or external pressure."
        ),
        astrology="Leo",
        image_placeholder="major_08_strength.png",
    ),
    Card(
        number=9,
        suit=CardSuit.MAJOR,
        name="The Hermit",
        keywords=["introspection", "searching within", "solitude", "guidance", "wisdom"],
        keywords_reversed=["isolation", "loneliness", "withdrawal", "rejection"],
        meaning=(
            "The Hermit represents introspection, searching within, solitude, guidance, "
            "inner wisdom, soul-searching, being alone, introspection, "
            "seeking truth, meditation, spiritual journey, looking inward, "
            "finding answers within, mentor energy."
        ),
        meaning_reversed=(
            "Reversed, The Hermit suggests isolation, loneliness, withdrawal, "
            "rejection of others, being lost, excessive isolation, "
            "avoiding help, being stuck in solitude, or refusing guidance."
        ),
        astrology="Virgo",
        image_placeholder="major_09_hermit.png",
    ),
    Card(
        number=10,
        suit=CardSuit.MAJOR,
        name="Wheel of Fortune",
        keywords=["change", "cycles", "inevitable fate", "turning point", "luck"],
        keywords_reversed=["bad luck", "resistance to change", "breaking cycles", "unforeseen"],
        meaning=(
            "The Wheel of Fortune represents change, cycles, inevitable fate, "
            "turning points, good luck, destiny, life's ups and downs, "
            "karma, moving with the cycles, opportunity, "
            "being at the right place at the right time, divine timing."
        ),
        meaning_reversed=(
            "Reversed, the Wheel indicates bad luck, resistance to change, "
            "breaking cycles, unforeseen setbacks, feeling stuck, "
            "external forces working against you, or unwelcome change."
        ),
        astrology="Jupiter",
        image_placeholder="major_10_wheel_of_fortune.png",
    ),
    Card(
        number=11,
        suit=CardSuit.MAJOR,
        name="Justice",
        keywords=["fairness", "truth", "cause and effect", "law", "balance"],
        keywords_reversed=["unfairness", "dishonesty", "imbalance", "karmic retribution"],
        meaning=(
            "Justice represents fairness, truth, cause and effect, law, balance, "
            "objectivity, clarity, facing consequences, legal matters, "
            "honesty, integrity, making balanced decisions, "
            "karmic justice, truth coming to light."
        ),
        meaning_reversed=(
            "Reversed, Justice warns of unfairness, dishonesty, imbalance, "
            "karmic retribution, injustice, bias, legal complications, "
            "avoiding accountability, or dishonesty in dealings."
        ),
        astrology="Libra",
        image_placeholder="major_11_justice.png",
    ),
    Card(
        number=12,
        suit=CardSuit.MAJOR,
        name="The Hanged Man",
        keywords=["surrender", "letting go", "new perspective", "sacrifice", "pause"],
        keywords_reversed=["resistance", "stalling", "indecision", "delay", "stalling"],
        meaning=(
            "The Hanged Man represents surrender, letting go, new perspective, "
            "sacrifice for greater good, pause, suspension, waiting, "
            "voluntary discomfort for growth, seeing things differently, "
            "suspending action, spiritual enlightenment through sacrifice."
        ),
        meaning_reversed=(
            "Reversed, The Hanged Man indicates resistance to change, stalling, "
            "indecision, delay, wasted sacrifice, fear of letting go, "
            "forced sacrifice, or resisting necessary pause."
        ),
        astrology="Neptune",
        image_placeholder="major_12_hanged_man.png",
    ),
    Card(
        number=13,
        suit=CardSuit.MAJOR,
        name="Death",
        keywords=["endings", "change", "transformation", "transition", "release"],
        keywords_reversed=["resistance to change", "stagnation", "decay", "fear of change"],
        meaning=(
            "Death represents endings, change, transformation, transition, release, "
            "letting go of the old, major life changes, rebirth, "
            "necessary endings, clearing space for new beginnings, "
            "transformation through loss, accepting change."
        ),
        meaning_reversed=(
            "Reversed, Death warns of resistance to change, stagnation, decay, "
            "fear of endings, clinging to the past, delayed transformation, "
            "inability to move on, or avoiding necessary closure."
        ),
        astrology="Scorpio",
        image_placeholder="major_13_death.png",
    ),
    Card(
        number=14,
        suit=CardSuit.MAJOR,
        name="Temperance",
        keywords=["balance", "moderation", "patience", "purpose", "blending"],
        keywords_reversed=["imbalance", "excess", "self-healing", "re-alignment"],
        meaning=(
            "Temperance represents balance, moderation, patience, purpose, blending, "
            "finding middle ground, harmony, healing, self-control, "
            "alchemy, combining opposites, flow, adaptation, "
            "moderation in all things, divine timing."
        ),
        meaning_reversed=(
            "Reversed, Temperance indicates imbalance, excess, lack of harmony, "
            "extremes, rushing, impatience, misalignment, "
            "overindulgence, or need for self-healing."
        ),
        astrology="Sagittarius",
        image_placeholder="major_14_temperance.png",
    ),
    Card(
        number=15,
        suit=CardSuit.MAJOR,
        name="The Devil",
        keywords=["shadow self", "attachment", "addiction", "restriction", "materialism"],
        keywords_reversed=["releasing limiting beliefs", "detachment", "freedom", "reclaiming"],
        meaning=(
            "The Devil represents the shadow self, attachment, addiction, restriction, "
            "materialism, being trapped by desires, bondage to habits, "
            "temptation, material focus, self-imposed limitations, "
            "shadow work, facing inner darkness, unhealthy attachments."
        ),
        meaning_reversed=(
            "Reversed, The Devil indicates releasing limiting beliefs, detachment, "
            "freedom, reclaiming power, breaking addictions, "
            "escaping negative patterns, awareness of self-imposed chains."
        ),
        astrology="Capricorn",
        image_placeholder="major_15_devil.png",
    ),
    Card(
        number=16,
        suit=CardSuit.MAJOR,
        name="The Tower",
        keywords=["sudden change", "upheaval", "awakening", "destruction", "revelation"],
        keywords_reversed=["avoiding disaster", "fear of change", "delaying the inevitable"],
        meaning=(
            "The Tower represents sudden change, upheaval, awakening, destruction, "
            "revelation of truth, breaking down false structures, "
            "chaos that leads to clarity, unexpected events, "
            "liberation through destruction, shattering illusions."
        ),
        meaning_reversed=(
            "Reversed, The Tower suggests avoiding disaster, fear of change, "
            "delaying the inevitable, resisting necessary upheaval, "
            "internal rather than external change, or personal transformation."
        ),
        astrology="Mars",
        image_placeholder="major_16_tower.png",
    ),
    Card(
        number=17,
        suit=CardSuit.MAJOR,
        name="The Star",
        keywords=["hope", "faith", "purpose", "renewal", "inspiration"],
        keywords_reversed=["despair", "discouragement", "lack of faith", "disconnection"],
        meaning=(
            "The Star represents hope, faith, purpose, renewal, inspiration, "
            "spiritual connection, healing after hardship, optimism, "
            "guidance, calm after the storm, divine blessing, "
            "wish fulfillment, following your North Star."
        ),
        meaning_reversed=(
            "Reversed, The Star indicates despair, discouragement, lack of faith, "
            "disconnection from spirit, lost hope, pessimism, "
            "creative blocks, or feeling uninspired."
        ),
        astrology="Aquarius",
        image_placeholder="major_17_star.png",
    ),
    Card(
        number=18,
        suit=CardSuit.MAJOR,
        name="The Moon",
        keywords=["illusion", "fear", "anxiety", "subconscious", "intuition"],
        keywords_reversed=["release of fear", "repressed emotion", "confusion", "deception"],
        meaning=(
            "The Moon represents illusion, fear, anxiety, the subconscious, "
            "intuition, dreams, uncertainty, hidden things coming to light, "
            "facing shadows, psychic awareness, deception, "
            "navigating through uncertainty, the unknown."
        ),
        meaning_reversed=(
            "Reversed, The Moon suggests release of fear, repressed emotion, "
            "confusion lifting, deception revealed, clarity emerging, "
            "overcoming anxiety, or suppressed intuition surfacing."
        ),
        astrology="Pisces",
        image_placeholder="major_18_moon.png",
    ),
    Card(
        number=19,
        suit=CardSuit.MAJOR,
        name="The Sun",
        keywords=["positivity", "fun", "warmth", "success", "vitality"],
        keywords_reversed=["depression", "sadness", "lack of energy", "overly optimistic"],
        meaning=(
            "The Sun represents positivity, fun, warmth, success, vitality, "
            "joy, confidence, enlightenment, truth revealed, "
            "happiness, achievement, good health, clarity, "
            "consciousness, childlike wonder, everything illuminated."
        ),
        meaning_reversed=(
            "Reversed, The Sun indicates temporary depression, sadness, "
            "lack of energy, being overly optimistic, delayed success, "
            "clouded judgment, or temporary setbacks to joy."
        ),
        astrology="The Sun",
        image_placeholder="major_19_sun.png",
    ),
    Card(
        number=20,
        suit=CardSuit.MAJOR,
        name="Judgement",
        keywords=["judgement", "rebirth", "inner calling", "absolution", "awakening"],
        keywords_reversed=["self-doubt", "refusal of self-examination", "unwillingness"],
        meaning=(
            "Judgement represents judgement, rebirth, inner calling, absolution, "
            "spiritual awakening, hearing the call, self-evaluation, "
            "redemption, renewal, answering your true calling, "
            "forgiveness, rising to a new level, karmic reckoning."
        ),
        meaning_reversed=(
            "Reversed, Judgement indicates self-doubt, refusal of self-examination, "
            "unwillingness to hear the truth, ignoring the call, "
            "harsh judgment of self or others, or avoiding accountability."
        ),
        astrology="Pluto",
        image_placeholder="major_20_judgement.png",
    ),
    Card(
        number=21,
        suit=CardSuit.MAJOR,
        name="The World",
        keywords=["completion", "integration", "accomplishment", "travel", "fulfillment"],
        keywords_reversed=["lack of completion", "emptiness", "seeking closure", "delays"],
        meaning=(
            "The World represents completion, integration, accomplishment, travel, "
            "fulfillment, wholeness, achieving goals, successful completion, "
            "graduation, reaching the finish line, unity, "
            "enlightenment, mastery, the end of a journey."
        ),
        meaning_reversed=(
            "Reversed, The World suggests lack of completion, emptiness, "
            "seeking closure, delays in finishing, unfinished business, "
            "loose ends, or feeling incomplete despite achievements."
        ),
        astrology="Saturn",
        image_placeholder="major_21_world.png",
    ),
]

# =============================================================================
# MINOR ARCANA - WANDS (Fire - Creativity, Action, Passion)
# =============================================================================

WANDS_CARDS = [
    Card(
        number=1,
        suit=CardSuit.WANDS,
        name="Ace of Wands",
        keywords=["inspiration", "new opportunities", "growth", "potential"],
        keywords_reversed=["delays", "lack of motivation", "weighed down"],
        meaning="Spark of inspiration, new creative venture, passion ignited, growth potential.",
        meaning_reversed="Delayed inspiration, creative blocks, extinguished passion.",
        element="Fire",
        astrology="Aries, Leo, Sagittarius",
        image_placeholder="wands_01_ace.png",
    ),
    Card(
        number=2,
        suit=CardSuit.WANDS,
        name="Two of Wands",
        keywords=["future planning", "progress", "decisions", "discovery"],
        keywords_reversed=["fear of unknown", "lack of planning", "disorganization"],
        meaning="Planning for the future, making decisions, expanding horizons, partnerships.",
        meaning_reversed="Fear of leaving comfort zone, poor planning, playing it safe.",
        element="Fire",
        astrology="Mars in Aries",
        image_placeholder="wands_02.png",
    ),
    Card(
        number=3,
        suit=CardSuit.WANDS,
        name="Three of Wands",
        keywords=["expansion", "foresight", "overseas opportunities", "leadership"],
        keywords_reversed=["obstacles", "delays", "frustration", "limitations"],
        meaning="Expansion, opportunities coming, foresight paying off, looking ahead.",
        meaning_reversed="Obstacles to plans, delays, frustration with progress.",
        element="Fire",
        astrology="Sun in Aries",
        image_placeholder="wands_03.png",
    ),
    Card(
        number=4,
        suit=CardSuit.WANDS,
        name="Four of Wands",
        keywords=["celebration", "joy", "harmony", "homecoming", "community"],
        keywords_reversed=["lack of support", "transience", "instability"],
        meaning="Celebration, harmony, happy home life, community, milestones achieved.",
        meaning_reversed="Lack of community support, temporary joy, unstable foundation.",
        element="Fire",
        astrology="Venus in Aries",
        image_placeholder="wands_04.png",
    ),
    Card(
        number=5,
        suit=CardSuit.WANDS,
        name="Five of Wands",
        keywords=["conflict", "competition", "tension", "diversity", "clashing"],
        keywords_reversed=["resolution", "avoiding conflict", "respecting differences"],
        meaning="Conflict, competition, healthy rivalry, clashing ideas, tension.",
        meaning_reversed="Resolution of conflict, avoiding competition, finding common ground.",
        element="Fire",
        astrology="Saturn in Leo",
        image_placeholder="wands_05.png",
    ),
    Card(
        number=6,
        suit=CardSuit.WANDS,
        name="Six of Wands",
        keywords=["success", "public recognition", "victory", "pride", "progress"],
        keywords_reversed=["excess pride", "lack of recognition", "punishment"],
        meaning="Victory, public recognition, success, self-confidence, good news.",
        meaning_reversed="Ego getting too big, lack of recognition, temporary success.",
        element="Fire",
        astrology="Jupiter in Leo",
        image_placeholder="wands_06.png",
    ),
    Card(
        number=7,
        suit=CardSuit.WANDS,
        name="Seven of Wands",
        keywords=["perseverance", "defensive stance", "maintaining position", "protection"],
        keywords_reversed=["giving up", "overwhelmed", "inability to fight"],
        meaning="Standing your ground, defending position, perseverance against odds.",
        meaning_reversed="Overwhelmed by challenges, giving up, unable to defend position.",
        element="Fire",
        astrology="Mars in Leo",
        image_placeholder="wands_07.png",
    ),
    Card(
        number=8,
        suit=CardSuit.WANDS,
        name="Eight of Wands",
        keywords=["speed", "action", "air travel", "movement", "quick decisions"],
        keywords_reversed=["delays", "frustration", "resisting change", "panic"],
        meaning="Fast movement, quick results, travel, swift communication, momentum.",
        meaning_reversed="Delays, slow progress, miscommunication, rushing into mistakes.",
        element="Fire",
        astrology="Mercury in Sagittarius",
        image_placeholder="wands_08.png",
    ),
    Card(
        number=9,
        suit=CardSuit.WANDS,
        name="Nine of Wands",
        keywords=["resilience", "courage", "last stand", "persistence", "fatigue"],
        keywords_reversed=["exhaustion", "giving up", "chronic fatigue", "inability"],
        meaning="Resilience, courage, last stand before victory, perseverance despite wounds.",
        meaning_reversed="Exhaustion, giving up, too many battles, chronic fatigue.",
        element="Fire",
        astrology="Moon in Sagittarius",
        image_placeholder="wands_09.png",
    ),
    Card(
        number=10,
        suit=CardSuit.WANDS,
        name="Ten of Wands",
        keywords=["burden", "responsibility", "hard work", "stress", "achievement"],
        keywords_reversed=["release", "delegation", "recovering", "burnout"],
        meaning="Heavy burdens, responsibility, hard work taking its toll, stress.",
        meaning_reversed="Releasing burdens, delegating, recovering from burnout.",
        element="Fire",
        astrology="Saturn in Sagittarius",
        image_placeholder="wands_10.png",
    ),
    Card(
        number=11,
        suit=CardSuit.WANDS,
        name="Page of Wands",
        keywords=["enthusiasm", "discovery", "freedom", "adventure", "fresh ideas"],
        keywords_reversed=["impulsiveness", "lack of direction", "bad news", "hasty"],
        meaning="New enthusiasm, exploring passions, adventurous spirit, creative spark.",
        meaning_reversed="Impulsive actions, lack of direction, scattered energy.",
        element="Fire",
        astrology="Earth of Fire",
        image_placeholder="wands_11_page.png",
    ),
    Card(
        number=12,
        suit=CardSuit.WANDS,
        name="Knight of Wands",
        keywords=["action", "adventure", "fearlessness", "impulsiveness", "energy"],
        keywords_reversed=["anger", "impulsiveness", "recklessness", "frustration"],
        meaning="Charging forward, adventure, fearless action, pursuing passions.",
        meaning_reversed="Reckless action, anger issues, haste making waste.",
        element="Fire",
        astrology="Air of Fire",
        image_placeholder="wands_12_knight.png",
    ),
    Card(
        number=13,
        suit=CardSuit.WANDS,
        name="Queen of Wands",
        keywords=["confidence", "social butterfly", "determination", "charisma", "warmth"],
        keywords_reversed=["selfishness", "jealousy", "insecurities", "manipulation"],
        meaning="Confident, charismatic leader, social warmth, determined, passionate.",
        meaning_reversed="Selfishness, jealousy, insecurity masking as confidence.",
        element="Fire",
        astrology="Water of Fire",
        image_placeholder="wands_13_queen.png",
    ),
    Card(
        number=14,
        suit=CardSuit.WANDS,
        name="King of Wands",
        keywords=["leadership", "vision", "entrepreneur", "honor", "boldness"],
        keywords_reversed=["impulsiveness", "haste", "ruthless", "high expectations"],
        meaning="Natural leader, vision and charisma, entrepreneurial spirit, honorable.",
        meaning_reversed="Tyrannical leadership, impulsive decisions, ruthless ambition.",
        element="Fire",
        astrology="Fire of Fire",
        image_placeholder="wands_14_king.png",
    ),
]

# =============================================================================
# MINOR ARCANA - CUPS (Water - Emotions, Relationships, Intuition)
# =============================================================================

CUPS_CARDS = [
    Card(
        number=1,
        suit=CardSuit.CUPS,
        name="Ace of Cups",
        keywords=["new feelings", "spiritual awakening", "intuition", "love"],
        keywords_reversed=["emotional loss", "blocked creativity", "emptiness"],
        meaning="New love, emotional awakening, spiritual connection, overflowing feelings.",
        meaning_reversed="Emotional block, emptiness, lost love, creative drought.",
        element="Water",
        astrology="Cancer, Scorpio, Pisces",
        image_placeholder="cups_01_ace.png",
    ),
    Card(
        number=2,
        suit=CardSuit.CUPS,
        name="Two of Cups",
        keywords=["partnership", "unity", "love", "harmony", "mutual attraction"],
        keywords_reversed=["breakup", "imbalance", "conflict", "disconnection"],
        meaning="Partnership, mutual attraction, harmonious union, soul connection.",
        meaning_reversed="Relationship imbalance, breakup, disconnection, unrequited love.",
        element="Water",
        astrology="Venus in Cancer",
        image_placeholder="cups_02.png",
    ),
    Card(
        number=3,
        suit=CardSuit.CUPS,
        name="Three of Cups",
        keywords=["friendship", "community", "celebration", "joy", "collaboration"],
        keywords_reversed=["gossip", "isolation", "party too hard", "conflict"],
        meaning="Friendship, celebration, community joy, creative collaboration.",
        meaning_reversed="Gossip, excessive partying, isolation, shallow connections.",
        element="Water",
        astrology="Mercury in Cancer",
        image_placeholder="cups_03.png",
    ),
    Card(
        number=4,
        suit=CardSuit.CUPS,
        name="Four of Cups",
        keywords=["contemplation", "apathy", "reevaluation", "boredom", "disconnect"],
        keywords_reversed=["awareness", "new possibilities", "seizing opportunities"],
        meaning="Contemplation, apathy, reevaluating choices, emotional dissatisfaction.",
        meaning_reversed="New awareness, fresh perspective, seizing new opportunities.",
        element="Water",
        astrology="Moon in Cancer",
        image_placeholder="cups_04.png",
    ),
    Card(
        number=5,
        suit=CardSuit.CUPS,
        name="Five of Cups",
        keywords=["loss", "grief", "disappointment", "regret", "mourning"],
        keywords_reversed=["acceptance", "moving on", "forgiveness", "hope"],
        meaning="Grief, loss, disappointment, focusing on what was lost, mourning.",
        meaning_reversed="Acceptance, moving forward, forgiveness, hope returning.",
        element="Water",
        astrology="Mars in Scorpio",
        image_placeholder="cups_05.png",
    ),
    Card(
        number=6,
        suit=CardSuit.CUPS,
        name="Six of Cups",
        keywords=["nostalgia", "childhood", "innocence", "joy", "past influences"],
        keywords_reversed=["stuck in past", "naivety", "unrealistic", "immaturity"],
        meaning="Nostalgia, childhood memories, innocence, reconnecting with the past.",
        meaning_reversed="Stuck in the past, unrealistic nostalgia, inability to grow up.",
        element="Water",
        astrology="Sun in Scorpio",
        image_placeholder="cups_06.png",
    ),
    Card(
        number=7,
        suit=CardSuit.CUPS,
        name="Seven of Cups",
        keywords=["choices", "fantasy", "wishful thinking", "illusion", "dreams"],
        keywords_reversed=["clarity", "reality check", "decisiveness", "commitment"],
        meaning="Many choices, wishful thinking, dreams and fantasies, illusions.",
        meaning_reversed="Clarity, facing reality, making decisions, commitment.",
        element="Water",
        astrology="Venus in Scorpio",
        image_placeholder="cups_07.png",
    ),
    Card(
        number=8,
        suit=CardSuit.CUPS,
        name="Eight of Cups",
        keywords=["walking away", "disillusionment", "seeking more", "abandonment"],
        keywords_reversed=["clinging", "fear of moving on", "stagnation", "indecision"],
        meaning="Walking away, leaving the past behind, seeking deeper meaning.",
        meaning_reversed="Clinging to the past, fear of moving on, stagnation.",
        element="Water",
        astrology="Saturn in Pisces",
        image_placeholder="cups_08.png",
    ),
    Card(
        number=9,
        suit=CardSuit.CUPS,
        name="Nine of Cups",
        keywords=["contentment", "satisfaction", "emotional stability", "wish granted"],
        keywords_reversed=["inner emptiness", "dissatisfaction", "smugness", "excess"],
        meaning="Emotional fulfillment, contentment, wishes granted, satisfaction.",
        meaning_reversed="Inner emptiness despite outer success, smugness, dissatisfaction.",
        element="Water",
        astrology="Jupiter in Pisces",
        image_placeholder="cups_09.png",
    ),
    Card(
        number=10,
        suit=CardSuit.CUPS,
        name="Ten of Cups",
        keywords=["emotional fulfillment", "happy family", "harmony", "joy", "bliss"],
        keywords_reversed=["domestic conflict", "broken home", "discord", "misalignment"],
        meaning="Emotional fulfillment, happy family life, harmony, complete joy.",
        meaning_reversed="Domestic conflict, broken relationships, misaligned values.",
        element="Water",
        astrology="Mars in Pisces",
        image_placeholder="cups_10.png",
    ),
    Card(
        number=11,
        suit=CardSuit.CUPS,
        name="Page of Cups",
        keywords=["creative opportunities", "intuition", "curiosity", "new emotions"],
        keywords_reversed=["emotional immaturity", "insecurity", "disappointment"],
        meaning="New emotions, creative spark, intuitive messages, romantic curiosity.",
        meaning_reversed="Emotional immaturity, insecurity, unrealistic expectations.",
        element="Water",
        astrology="Earth of Water",
        image_placeholder="cups_11_page.png",
    ),
    Card(
        number=12,
        suit=CardSuit.CUPS,
        name="Knight of Cups",
        keywords=["romance", "charm", "idealism", "imagination", "following heart"],
        keywords_reversed=["unrealistic", "moodiness", "disappointment", "escapism"],
        meaning="Romantic pursuit, following heart, charm and idealism, proposals.",
        meaning_reversed="Unrealistic expectations, moodiness, disappointment in love.",
        element="Water",
        astrology="Air of Water",
        image_placeholder="cups_12_knight.png",
    ),
    Card(
        number=13,
        suit=CardSuit.CUPS,
        name="Queen of Cups",
        keywords=["compassion", "calm", "comfort", "intuitive", "emotional security"],
        keywords_reversed=["emotional insecurity", "overwhelmed", "needy", "coldness"],
        meaning="Emotional depth, intuition, compassion, nurturing, deep understanding.",
        meaning_reversed="Emotional overwhelm, insecurity, repressing feelings.",
        element="Water",
        astrology="Water of Water",
        image_placeholder="cups_13_queen.png",
    ),
    Card(
        number=14,
        suit=CardSuit.CUPS,
        name="King of Cups",
        keywords=["emotional balance", "compassion", "diplomacy", "wisdom", "master"],
        keywords_reversed=["moodiness", "emotional manipulation", "volatility"],
        meaning="Emotional mastery, balanced compassion, diplomatic wisdom.",
        meaning_reversed="Emotional manipulation, moodiness, volatile feelings.",
        element="Water",
        astrology="Fire of Water",
        image_placeholder="cups_14_king.png",
    ),
]

# =============================================================================
# MINOR ARCANA - SWORDS (Air - Intellect, Conflict, Decisions)
# =============================================================================

SWORDS_CARDS = [
    Card(
        number=1,
        suit=CardSuit.SWORDS,
        name="Ace of Swords",
        keywords=["breakthrough", "clarity", "new idea", "mental clarity", "truth"],
        keywords_reversed=["confusion", "chaos", "lack of clarity", "miscommunication"],
        meaning="Mental breakthrough, clarity of thought, new ideas, truth revealed.",
        meaning_reversed="Confusion, chaos, lack of clarity, muddled thinking.",
        element="Air",
        astrology="Gemini, Libra, Aquarius",
        image_placeholder="swords_01_ace.png",
    ),
    Card(
        number=2,
        suit=CardSuit.SWORDS,
        name="Two of Swords",
        keywords=["indecision", "difficult choices", "stalemate", "avoidance"],
        keywords_reversed=["information overload", "indecision", "confusion", "stalemate"],
        meaning="Difficult decision, stalemate, avoidance, needing to choose.",
        meaning_reversed="Information overload, inability to decide, confusion worsening.",
        element="Air",
        astrology="Moon in Libra",
        image_placeholder="swords_02.png",
    ),
    Card(
        number=3,
        suit=CardSuit.SWORDS,
        name="Three of Swords",
        keywords=["heartbreak", "grief", "sorrow", "rejection", "loss"],
        keywords_reversed=["recovery", "forgiveness", "moving on", "releasing pain"],
        meaning="Heartbreak, grief, sorrow, emotional pain, rejection, loss.",
        meaning_reversed="Healing from heartbreak, forgiveness, releasing pain, recovery.",
        element="Air",
        astrology="Saturn in Libra",
        image_placeholder="swords_03.png",
    ),
    Card(
        number=4,
        suit=CardSuit.SWORDS,
        name="Four of Swords",
        keywords=["rest", "restoration", "contemplation", "recuperation", "meditation"],
        keywords_reversed=["restlessness", "burnout", "lack of progress", "stagnation"],
        meaning="Rest and recovery, contemplation, peace, mental recuperation.",
        meaning_reversed="Restlessness, burnout, inability to rest, pushing too hard.",
        element="Air",
        astrology="Jupiter in Libra",
        image_placeholder="swords_04.png",
    ),
    Card(
        number=5,
        suit=CardSuit.SWORDS,
        name="Five of Swords",
        keywords=["conflict", "defeat", "winning at all costs", "betrayal", "sneakiness"],
        keywords_reversed=["reconciliation", "making amends", "past resentment"],
        meaning="Conflict, winning at all costs, betrayal, hollow victory, deception.",
        meaning_reversed="Reconciliation, making amends, letting go of resentment.",
        element="Air",
        astrology="Venus in Aquarius",
        image_placeholder="swords_05.png",
    ),
    Card(
        number=6,
        suit=CardSuit.SWORDS,
        name="Six of Swords",
        keywords=["transition", "change", "moving on", "travel", "leaving behind"],
        keywords_reversed=["unfinished business", "resistance to change", "stuck"],
        meaning="Moving on, transition, leaving difficulties behind, travel, healing journey.",
        meaning_reversed="Resistance to change, unfinished business, difficulty moving on.",
        element="Air",
        astrology="Mercury in Aquarius",
        image_placeholder="swords_06.png",
    ),
    Card(
        number=7,
        suit=CardSuit.SWORDS,
        name="Seven of Swords",
        keywords=["deception", "strategy", "sneakiness", "getting away with something"],
        keywords_reversed=["coming clean", "rethinking approach", "conscience"],
        meaning="Deception, strategy, sneakiness, theft, getting away with something.",
        meaning_reversed="Coming clean, conscience catching up, rethinking dishonest approach.",
        element="Air",
        astrology="Moon in Aquarius",
        image_placeholder="swords_07.png",
    ),
    Card(
        number=8,
        suit=CardSuit.SWORDS,
        name="Eight of Swords",
        keywords=["restriction", "imprisonment", "victim mentality", "negative thoughts"],
        keywords_reversed=["freedom", "release", "taking control", "new perspective"],
        meaning="Feeling trapped, victim mentality, self-imposed restrictions, negative thinking.",
        meaning_reversed="Freedom, release from bondage, taking control, new perspective.",
        element="Air",
        astrology="Jupiter in Gemini",
        image_placeholder="swords_08.png",
    ),
    Card(
        number=9,
        suit=CardSuit.SWORDS,
        name="Nine of Swords",
        keywords=["anxiety", "worry", "fear", "nightmares", "guilt", "anguish"],
        keywords_reversed=["hope", "reaching out", "despair", "inner turmoil"],
        meaning="Anxiety, worry, fear, nightmares, mental anguish, worst-case thinking.",
        meaning_reversed="Hope emerging, reaching out for help, light at end of tunnel.",
        element="Air",
        astrology="Mars in Gemini",
        image_placeholder="swords_09.png",
    ),
    Card(
        number=10,
        suit=CardSuit.SWORDS,
        name="Ten of Swords",
        keywords=["painful endings", "deep wounds", "betrayal", "loss", "crisis"],
        keywords_reversed=["recovery", "resurrection", "incapable of change", "evolution"],
        meaning="Painful ending, deep wounds, betrayal rock bottom, final release.",
        meaning_reversed="Recovery beginning, resurrection from rock bottom, new dawn.",
        element="Air",
        astrology="Sun in Gemini",
        image_placeholder="swords_10.png",
    ),
    Card(
        number=11,
        suit=CardSuit.SWORDS,
        name="Page of Swords",
        keywords=["curiosity", "new ideas", "thirst for knowledge", "communication"],
        keywords_reversed=["deception", "manipulation", "all talk no action", "haste"],
        meaning="Curiosity, new ideas, mental energy, thirst for knowledge.",
        meaning_reversed="Deception, all talk no action, manipulation, hasty conclusions.",
        element="Air",
        astrology="Earth of Air",
        image_placeholder="swords_11_page.png",
    ),
    Card(
        number=12,
        suit=CardSuit.SWORDS,
        name="Knight of Swords",
        keywords=["action", "impulsiveness", "defending beliefs", "haste", "ambitious"],
        keywords_reversed=["no direction", "disregard for consequences", "unpredictable"],
        meaning="Swift action, charging forward, ambitious pursuit, defending beliefs.",
        meaning_reversed="Reckless action, no direction, disregard for consequences.",
        element="Air",
        astrology="Air of Air",
        image_placeholder="swords_12_knight.png",
    ),
    Card(
        number=13,
        suit=CardSuit.SWORDS,
        name="Queen of Swords",
        keywords=["independence", "clear boundaries", "perceptive", "honest", "fair"],
        keywords_reversed=["cold-hearted", "cruel", "deceptive", "manipulative"],
        meaning="Independent thought, clear boundaries, perceptive honesty, fairness.",
        meaning_reversed="Cold-heartedness, cruelty, manipulative honesty, bitterness.",
        element="Air",
        astrology="Water of Air",
        image_placeholder="swords_13_queen.png",
    ),
    Card(
        number=14,
        suit=CardSuit.SWORDS,
        name="King of Swords",
        keywords=["mental clarity", "intellectual power", "authority", "truth"],
        keywords_reversed=["quiet power", "inner truth", "misuse of power", "manipulation"],
        meaning="Intellectual authority, mental clarity, truth-seeking, fair judgment.",
        meaning_reversed="Misuse of intellect, manipulative authority, cold tyranny.",
        element="Air",
        astrology="Fire of Air",
        image_placeholder="swords_14_king.png",
    ),
]

# =============================================================================
# MINOR ARCANA - PENTACLES (Earth - Material World, Finances, Body)
# =============================================================================

PENTACLES_CARDS = [
    Card(
        number=1,
        suit=CardSuit.PENTACLES,
        name="Ace of Pentacles",
        keywords=["opportunity", "prosperity", "new venture", "manifestation", "abundance"],
        keywords_reversed=["lost opportunity", "lack of planning", "scarcity"],
        meaning="New financial opportunity, prosperity, manifestation, material abundance.",
        meaning_reversed="Missed opportunity, poor planning, financial scarcity.",
        element="Earth",
        astrology="Taurus, Virgo, Capricorn",
        image_placeholder="pentacles_01_ace.png",
    ),
    Card(
        number=2,
        suit=CardSuit.PENTACLES,
        name="Two of Pentacles",
        keywords=["balance", "adaptability", "time management", "prioritization"],
        keywords_reversed=["overwhelm", "disorganization", "reprioritization needed"],
        meaning="Juggling responsibilities, balance, adaptability, time management.",
        meaning_reversed="Overwhelm, losing balance, disorganization, dropping balls.",
        element="Earth",
        astrology="Jupiter in Capricorn",
        image_placeholder="pentacles_02.png",
    ),
    Card(
        number=3,
        suit=CardSuit.PENTACLES,
        name="Three of Pentacles",
        keywords=["teamwork", "collaboration", "learning", "implementation", "skill"],
        keywords_reversed=["lack of teamwork", "disorganized", "group conflict"],
        meaning="Teamwork, skilled collaboration, learning and implementing, recognition.",
        meaning_reversed="Lack of cooperation, disorganized team, conflict in collaboration.",
        element="Earth",
        astrology="Mars in Capricorn",
        image_placeholder="pentacles_03.png",
    ),
    Card(
        number=4,
        suit=CardSuit.PENTACLES,
        name="Four of Pentacles",
        keywords=["security", "conservation", "frugality", "control", "possessiveness"],
        keywords_reversed=["greed", "materialism", "self-protection", "generosity"],
        meaning="Financial security, holding on to resources, conservation, control.",
        meaning_reversed="Greed, materialism, inability to let go, selfishness.",
        element="Earth",
        astrology="Sun in Capricorn",
        image_placeholder="pentacles_04.png",
    ),
    Card(
        number=5,
        suit=CardSuit.PENTACLES,
        name="Five of Pentacles",
        keywords=["financial loss", "poverty", "isolation", "worry", "hardship"],
        keywords_reversed=["recovery from loss", "finding help", "improvement", "hope"],
        meaning="Financial hardship, poverty mindset, isolation, difficult times.",
        meaning_reversed="Recovery from loss, finding help, spiritual wealth, improvement.",
        element="Earth",
        astrology="Mercury in Taurus",
        image_placeholder="pentacles_05.png",
    ),
    Card(
        number=6,
        suit=CardSuit.PENTACLES,
        name="Six of Pentacles",
        keywords=["generosity", "charity", "giving", "prosperity", "sharing wealth"],
        keywords_reversed=["strings attached", "inequality", "selfishness", "debt"],
        meaning="Generosity, charity, sharing wealth, giving and receiving, prosperity.",
        meaning_reversed="Strings attached to gifts, inequality, selfishness, debt.",
        element="Earth",
        astrology="Moon in Taurus",
        image_placeholder="pentacles_06.png",
    ),
    Card(
        number=7,
        suit=CardSuit.PENTACLES,
        name="Seven of Pentacles",
        keywords=["long-term view", "sustainable results", "perseverance", "investment"],
        keywords_reversed=["lack of growth", "impatience", "bad investments", "waste"],
        meaning="Assessment of progress, long-term view, patience, investment paying off.",
        meaning_reversed="Impatience, lack of growth, bad investments, wasted effort.",
        element="Earth",
        astrology="Saturn in Taurus",
        image_placeholder="pentacles_07.png",
    ),
    Card(
        number=8,
        suit=CardSuit.PENTACLES,
        name="Eight of Pentacles",
        keywords=["apprenticeship", "repetitive tasks", "mastery", "skill development"],
        keywords_reversed=["self-development", "perfectionism", "misdirected activity"],
        meaning="Skill development, apprenticeship, diligent work, mastery through practice.",
        meaning_reversed="Perfectionism, lack of focus, misdirected efforts, boredom.",
        element="Earth",
        astrology="Sun in Virgo",
        image_placeholder="pentacles_08.png",
    ),
    Card(
        number=9,
        suit=CardSuit.PENTACLES,
        name="Nine of Pentacles",
        keywords=["abundance", "luxury", "self-sufficiency", "financial independence"],
        keywords_reversed=["self-worth issues", "working too hard", "materialism"],
        meaning="Financial independence, luxury, self-sufficiency, enjoying fruits of labor.",
        meaning_reversed="Self-worth tied to wealth, working too hard, superficiality.",
        element="Earth",
        astrology="Venus in Virgo",
        image_placeholder="pentacles_09.png",
    ),
    Card(
        number=10,
        suit=CardSuit.PENTACLES,
        name="Ten of Pentacles",
        keywords=["wealth", "financial security", "family", "long-term success", "legacy"],
        keywords_reversed=["financial failure", "loneliness", "loss", "short-term focus"],
        meaning="Family wealth, long-term security, legacy, financial culmination, inheritance.",
        meaning_reversed="Financial failure, family conflicts, lost inheritance, instability.",
        element="Earth",
        astrology="Mercury in Virgo",
        image_placeholder="pentacles_10.png",
    ),
    Card(
        number=11,
        suit=CardSuit.PENTACLES,
        name="Page of Pentacles",
        keywords=["new opportunity", "studiousness", "manifestation", "ambition"],
        keywords_reversed=["lack of progress", "procrastination", "missed opportunity"],
        meaning="New opportunity, financial prospect, studious approach, ambition.",
        meaning_reversed="Procrastination, missed opportunity, lack of progress.",
        element="Earth",
        astrology="Earth of Earth",
        image_placeholder="pentacles_11_page.png",
    ),
    Card(
        number=12,
        suit=CardSuit.PENTACLES,
        name="Knight of Pentacles",
        keywords=["hard work", "productivity", "routine", "conservatism", "persistence"],
        keywords_reversed=["stuck in routine", "laziness", "boredom", "perfectionism"],
        meaning="Hard work, methodical approach, persistence, routine, productivity.",
        meaning_reversed="Stuck in routine, laziness, boredom, slow progress.",
        element="Earth",
        astrology="Air of Earth",
        image_placeholder="pentacles_12_knight.png",
    ),
    Card(
        number=13,
        suit=CardSuit.PENTACLES,
        name="Queen of Pentacles",
        keywords=["nurturing", "practical", "abundance", "comfort", "financial security"],
        keywords_reversed=["selfishness", "jealousy", "smothering", "financial anxiety"],
        meaning="Nurturing abundance, practical comfort, financial security, earthly pleasures.",
        meaning_reversed="Selfishness, financial anxiety, smothering, work-life imbalance.",
        element="Earth",
        astrology="Water of Earth",
        image_placeholder="pentacles_13_queen.png",
    ),
    Card(
        number=14,
        suit=CardSuit.PENTACLES,
        name="King of Pentacles",
        keywords=["abundance", "prosperity", "security", "discipline", "generosity"],
        keywords_reversed=["greed", "materialism", "financially inept", "stinginess"],
        meaning="Financial mastery, abundance, business acumen, security, generosity.",
        meaning_reversed="Greed, materialism, poor financial decisions, stinginess.",
        element="Earth",
        astrology="Fire of Earth",
        image_placeholder="pentacles_14_king.png",
    ),
]

# Compile complete deck
TAROT_DECK: list[Card] = MAJOR_ARCANA + WANDS_CARDS + CUPS_CARDS + SWORDS_CARDS + PENTACLES_CARDS

# Verify deck has 78 cards
assert len(TAROT_DECK) == 78, f"Deck must have 78 cards, got {len(TAROT_DECK)}"
