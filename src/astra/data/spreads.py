"""
Tarot Spread Definitions
========================
RESEARCH BY: Sarah (Research Lead)

Traditional tarot spreads with position meanings.
Each spread defines card positions and their interpretations.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class SpreadPosition:
    """
    Represents a single position in a tarot spread.

    Attributes:
        position: Position number (1-indexed)
        name: Position name
        meaning: What this position represents
        description: Detailed explanation
    """

    position: int
    name: str
    meaning: str
    description: str


@dataclass(frozen=True)
class Spread:
    """
    Represents a complete tarot spread layout.

    Attributes:
        name: Spread name
        description: Brief description
        num_cards: Number of cards in spread
        positions: List of position definitions
        best_for: Types of questions this spread answers
        difficulty: Beginner/Intermediate/Advanced
    """

    name: str
    description: str
    num_cards: int
    positions: list[SpreadPosition]
    best_for: list[str]
    difficulty: str
    estimated_time: str


# =============================================================================
# SPREAD DEFINITIONS
# =============================================================================

SINGLE_CARD = Spread(
    name="Single Card",
    description="A simple one-card draw for quick guidance or daily reflection.",
    num_cards=1,
    positions=[
        SpreadPosition(
            position=1,
            name="The Message",
            meaning="The core energy or answer",
            description=(
                "This card represents the primary energy surrounding your question "
                "or situation. For daily draws, it offers guidance for the day ahead. "
                "For specific questions, it provides direct insight or advice."
            ),
        ),
    ],
    best_for=[
        "Daily guidance",
        "Quick decisions",
        "Mood/energy check",
        "Simple yes/no clarity",
        "Meditation focus",
    ],
    difficulty="Beginner",
    estimated_time="1-2 minutes",
)

THREE_CARD_SPREAD = Spread(
    name="Three Card Spread",
    description="The classic Past-Present-Future spread for timeline readings.",
    num_cards=3,
    positions=[
        SpreadPosition(
            position=1,
            name="Past",
            meaning="Foundation and influences",
            description=(
                "This card represents the past events, experiences, or energies that "
                "have shaped your current situation. It shows the foundation upon which "
                "the present is built."
            ),
        ),
        SpreadPosition(
            position=2,
            name="Present",
            meaning="Current situation and energies",
            description=(
                "This card reflects your current state, the energies surrounding you now, "
                "and the heart of the matter. It shows where you stand today."
            ),
        ),
        SpreadPosition(
            position=3,
            name="Future",
            meaning="Potential outcome or direction",
            description=(
                "This card indicates the likely outcome if current energies continue. "
                "Remember: the future is not fixed; this shows the trajectory based on "
                "present circumstances."
            ),
        ),
    ],
    best_for=[
        "Timeline readings",
        "Understanding progression",
        "Career path questions",
        "Relationship development",
        "General life situations",
    ],
    difficulty="Beginner",
    estimated_time="3-5 minutes",
)

THREE_CARD_MIND_BODY_SPIRIT = Spread(
    name="Mind-Body-Spirit",
    description="A holistic spread examining different aspects of self.",
    num_cards=3,
    positions=[
        SpreadPosition(
            position=1,
            name="Mind",
            meaning="Thoughts, intellect, mental state",
            description=(
                "This card represents your mental state, thought patterns, intellectual "
                "approach, and what your mind needs right now."
            ),
        ),
        SpreadPosition(
            position=2,
            name="Body",
            meaning="Physical health, action, practical matters",
            description=(
                "This card reflects your physical state, what actions to take, "
                "and practical aspects of your situation."
            ),
        ),
        SpreadPosition(
            position=3,
            name="Spirit",
            meaning="Soul, intuition, spiritual path",
            description=(
                "This card indicates your spiritual state, intuitive guidance, "
                "and what your soul needs for fulfillment."
            ),
        ),
    ],
    best_for=[
        "Self-care check-ins",
        "Holistic wellness",
        "Balancing life aspects",
        "Personal growth",
        "Stress management",
    ],
    difficulty="Beginner",
    estimated_time="3-5 minutes",
)

THREE_CARD_SITUATION_ACTION_OUTCOME = Spread(
    name="Situation-Action-Outcome",
    description="Problem-solving spread for decision making.",
    num_cards=3,
    positions=[
        SpreadPosition(
            position=1,
            name="Situation",
            meaning="The current challenge or context",
            description=(
                "This card describes the present situation, the challenge you're facing, "
                "or the context surrounding your question."
            ),
        ),
        SpreadPosition(
            position=2,
            name="Action",
            meaning="Recommended approach or action",
            description=(
                "This card suggests the best course of action, approach to take, "
                "or attitude to adopt."
            ),
        ),
        SpreadPosition(
            position=3,
            name="Outcome",
            meaning="Result of taking the suggested action",
            description=(
                "This card shows the likely result if you follow the recommended action. "
                "It represents the potential resolution or next phase."
            ),
        ),
    ],
    best_for=[
        "Decision making",
        "Problem solving",
        "Course of action",
        "Conflict resolution",
        "Goal achievement",
    ],
    difficulty="Beginner",
    estimated_time="3-5 minutes",
)

CELTIC_CROSS = Spread(
    name="Celtic Cross",
    description="The classic 10-card spread for in-depth comprehensive readings.",
    num_cards=10,
    positions=[
        SpreadPosition(
            position=1,
            name="Present Situation",
            meaning="The heart of the matter",
            description=(
                "This card represents the current situation, the core energy, "
                "or the primary factor at play right now."
            ),
        ),
        SpreadPosition(
            position=2,
            name="Challenge/Cross",
            meaning="Immediate obstacle or opposing force",
            description=(
                "This card crosses the first card and represents the challenge, "
                "obstacle, or opposing force you're facing. It may be external "
                "or internal."
            ),
        ),
        SpreadPosition(
            position=3,
            name="Foundation",
            meaning="Root cause or basis of situation",
            description=(
                "This card lies beneath and represents the foundation, past influences, "
                "or the root cause that led to the present situation."
            ),
        ),
        SpreadPosition(
            position=4,
            name="Recent Past",
            meaning="Events leaving but still influential",
            description=(
                "This card represents recent events or energies that are passing away "
                "but still have some influence on the situation."
            ),
        ),
        SpreadPosition(
            position=5,
            name="Crown/Goal",
            meaning="Best possible outcome or aspiration",
            description=(
                "This card above represents your goal, aspiration, or the best possible "
                "outcome you hope to achieve."
            ),
        ),
        SpreadPosition(
            position=6,
            name="Near Future",
            meaning="What is coming next",
            description=(
                "This card indicates the immediate future, events coming in the "
                "next days or weeks."
            ),
        ),
        SpreadPosition(
            position=7,
            name="Self",
            meaning="Your attitude and approach",
            description=(
                "This card represents how you see yourself, your attitude, "
                "or your approach to the situation."
            ),
        ),
        SpreadPosition(
            position=8,
            name="Environment",
            meaning="External influences and others' views",
            description=(
                "This card represents external influences, how others see the situation, "
                "or the environment surrounding you."
            ),
        ),
        SpreadPosition(
            position=9,
            name="Hopes & Fears",
            meaning="What you desire or dread",
            description=(
                "This card reveals your hopes, fears, or expectations about "
                "the situation. Often hopes and fears are two sides of the same coin."
            ),
        ),
        SpreadPosition(
            position=10,
            name="Outcome",
            meaning="Final result if path continues",
            description=(
                "This final card represents the ultimate outcome, the culmination "
                "of all energies, if current paths continue."
            ),
        ),
    ],
    best_for=[
        "Complex situations",
        "Life transitions",
        "Major decisions",
        "Comprehensive overview",
        "Deep self-reflection",
    ],
    difficulty="Advanced",
    estimated_time="15-30 minutes",
)

RELATIONSHIP_SPREAD = Spread(
    name="Relationship Spread",
    description="Seven-card spread examining relationship dynamics.",
    num_cards=7,
    positions=[
        SpreadPosition(
            position=1,
            name="You",
            meaning="Your position in the relationship",
            description=(
                "This card represents your energy, perspective, and role "
                "in the relationship right now."
            ),
        ),
        SpreadPosition(
            position=2,
            name="Partner/Other",
            meaning="The other person's position",
            description=(
                "This card represents the other person's energy, perspective, "
                "and role in the relationship."
            ),
        ),
        SpreadPosition(
            position=3,
            name="Relationship Foundation",
            meaning="What binds you together",
            description=(
                "This card represents the foundation of the relationship, "
                "shared values, or what originally brought you together."
            ),
        ),
        SpreadPosition(
            position=4,
            name="Current Dynamic",
            meaning="How you currently interact",
            description=(
                "This card reflects the current state of the relationship, "
                "the energy between you, and how you're currently interacting."
            ),
        ),
        SpreadPosition(
            position=5,
            name="Strengths",
            meaning="What works well between you",
            description=(
                "This card highlights the strengths of the relationship, "
                "what supports you both, and positive aspects."
            ),
        ),
        SpreadPosition(
            position=6,
            name="Challenges",
            meaning="What needs attention or work",
            description=(
                "This card reveals challenges, obstacles, or areas that need "
                "attention and growth in the relationship."
            ),
        ),
        SpreadPosition(
            position=7,
            name="Potential/Future",
            meaning="Where the relationship is heading",
            description=(
                "This card indicates the potential direction of the relationship, "
                "what it could become, or the likely future if current patterns continue."
            ),
        ),
    ],
    best_for=[
        "Romantic relationships",
        "Friendship dynamics",
        "Family relationships",
        "Business partnerships",
        "Understanding connection",
    ],
    difficulty="Intermediate",
    estimated_time="10-15 minutes",
)

CAREER_PATH_SPREAD = Spread(
    name="Career Path Spread",
    description="Five-card spread for professional guidance.",
    num_cards=5,
    positions=[
        SpreadPosition(
            position=1,
            name="Current Position",
            meaning="Where you are professionally",
            description=(
                "This card represents your current career situation, "
                "your standing, and present circumstances."
            ),
        ),
        SpreadPosition(
            position=2,
            name="Strengths & Skills",
            meaning="What you bring to the table",
            description=(
                "This card highlights your strengths, skills, and talents "
                "that serve you in your career."
            ),
        ),
        SpreadPosition(
            position=3,
            name="Challenges & Blocks",
            meaning="What holds you back",
            description=(
                "This card reveals obstacles, challenges, or limiting beliefs "
                "that may be blocking your career progress."
            ),
        ),
        SpreadPosition(
            position=4,
            name="Opportunities",
            meaning="What is available to you",
            description=(
                "This card indicates opportunities, potential paths, "
                "or resources available for your career growth."
            ),
        ),
        SpreadPosition(
            position=5,
            name="Outcome",
            meaning="Where this path leads",
            description=(
                "This card suggests the potential outcome, the direction "
                "your career is heading, or advice for best results."
            ),
        ),
    ],
    best_for=[
        "Career decisions",
        "Job changes",
        "Professional development",
        "Workplace issues",
        "Finding direction",
    ],
    difficulty="Intermediate",
    estimated_time="8-12 minutes",
)

# =============================================================================
# SPREAD REGISTRY
# =============================================================================

SPREADS: dict[str, Spread] = {
    "single": SINGLE_CARD,
    "three": THREE_CARD_SPREAD,
    "mind_body_spirit": THREE_CARD_MIND_BODY_SPIRIT,
    "situation_action": THREE_CARD_SITUATION_ACTION_OUTCOME,
    "celtic": CELTIC_CROSS,
    "relationship": RELATIONSHIP_SPREAD,
    "career": CAREER_PATH_SPREAD,
}

# For display purposes
SPREAD_DISPLAY_ORDER = [
    "single",
    "three",
    "mind_body_spirit",
    "situation_action",
    "relationship",
    "career",
    "celtic",
]
