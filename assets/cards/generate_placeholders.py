"""
Placeholder Image Generator
===========================
IMPLEMENTATION BY: Maya (Assets Lead)

Generates simple placeholder images for all 78 tarot cards.
These are basic colored rectangles with text that can be easily replaced.
"""

import os
from PIL import Image, ImageDraw, ImageFont


# Card dimensions (tarot aspect ratio)
CARD_WIDTH = 300
CARD_HEIGHT = 500

# Suit colors (RGB)
SUIT_COLORS = {
    "major": (218, 165, 32),    # Gold
    "wands": (231, 126, 34),    # Orange
    "cups": (52, 152, 219),     # Blue
    "swords": (149, 165, 166),  # Silver
    "pentacles": (39, 174, 96), # Green
}

# Background colors
BG_COLOR = (30, 30, 46)         # Dark purple-black
TEXT_COLOR = (255, 255, 255)    # White
BORDER_COLOR = (200, 200, 200)  # Light gray


def generate_card(suit: str, name: str, number: str, output_path: str):
    """Generate a single placeholder card."""
    
    # Create image
    img = Image.new('RGB', (CARD_WIDTH, CARD_HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    # Get suit color
    color = SUIT_COLORS.get(suit, SUIT_COLORS["major"])
    
    # Draw border
    border_width = 4
    draw.rectangle(
        [(border_width, border_width), 
         (CARD_WIDTH - border_width, CARD_HEIGHT - border_width)],
        outline=color,
        width=border_width
    )
    
    # Draw inner border
    inner_margin = 20
    draw.rectangle(
        [(inner_margin, inner_margin), 
         (CARD_WIDTH - inner_margin, CARD_HEIGHT - inner_margin)],
        outline=color,
        width=2
    )
    
    # Draw suit symbol at top
    symbols = {
        "major": "★",
        "wands": "🔥",
        "cups": "🌊",
        "swords": "⚔",
        "pentacles": "⬟",
    }
    
    try:
        # Try to use a nice font
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 28)
        text_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
        symbol_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 48)
    except:
        # Fallback to default
        title_font = ImageFont.load_default()
        text_font = ImageFont.load_default()
        symbol_font = ImageFont.load_default()
    
    # Draw symbol
    symbol = symbols.get(suit, "★")
    # Simple text symbol fallback
    if suit == "wands":
        symbol_text = "W"
    elif suit == "cups":
        symbol_text = "C"
    elif suit == "swords":
        symbol_text = "S"
    elif suit == "pentacles":
        symbol_text = "P"
    else:
        symbol_text = "M"
    
    # Center the symbol
    bbox = draw.textbbox((0, 0), symbol_text, font=symbol_font)
    symbol_width = bbox[2] - bbox[0]
    symbol_x = (CARD_WIDTH - symbol_width) // 2
    draw.text((symbol_x, 60), symbol_text, fill=color, font=symbol_font)
    
    # Draw card name
    # Wrap text if needed
    words = name.split()
    lines = []
    current_line = []
    
    for word in words:
        test_line = ' '.join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=title_font)
        if bbox[2] - bbox[0] <= CARD_WIDTH - 60:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
    if current_line:
        lines.append(' '.join(current_line))
    
    # Draw name lines
    y_offset = 180
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=title_font)
        line_width = bbox[2] - bbox[0]
        line_x = (CARD_WIDTH - line_width) // 2
        draw.text((line_x, y_offset), line, fill=TEXT_COLOR, font=title_font)
        y_offset += 40
    
    # Draw number
    bbox = draw.textbbox((0, 0), number, font=text_font)
    num_width = bbox[2] - bbox[0]
    num_x = (CARD_WIDTH - num_width) // 2
    draw.text((num_x, 350), number, fill=color, font=text_font)
    
    # Draw placeholder text
    placeholder_text = "[PLACEHOLDER]"
    bbox = draw.textbbox((0, 0), placeholder_text, font=text_font)
    placeholder_width = bbox[2] - bbox[0]
    placeholder_x = (CARD_WIDTH - placeholder_width) // 2
    draw.text((placeholder_x, 420), placeholder_text, fill=(150, 150, 150), font=text_font)
    
    # Save
    img.save(output_path)
    print(f"Generated: {output_path}")


def generate_all_placeholders(output_dir: str = "."):
    """Generate all 78 placeholder cards."""
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Major Arcana
    major_arcana = [
        ("0", "The Fool"),
        ("I", "The Magician"),
        ("II", "The High Priestess"),
        ("III", "The Empress"),
        ("IV", "The Emperor"),
        ("V", "The Hierophant"),
        ("VI", "The Lovers"),
        ("VII", "The Chariot"),
        ("VIII", "Strength"),
        ("IX", "The Hermit"),
        ("X", "Wheel of Fortune"),
        ("XI", "Justice"),
        ("XII", "The Hanged Man"),
        ("XIII", "Death"),
        ("XIV", "Temperance"),
        ("XV", "The Devil"),
        ("XVI", "The Tower"),
        ("XVII", "The Star"),
        ("XVIII", "The Moon"),
        ("XIX", "The Sun"),
        ("XX", "Judgement"),
        ("XXI", "The World"),
    ]
    
    # Roman numeral to integer mapping
    roman_to_int = {
        '0': 0, 'I': 1, 'II': 2, 'III': 3, 'IV': 4, 'V': 5,
        'VI': 6, 'VII': 7, 'VIII': 8, 'IX': 9, 'X': 10,
        'XI': 11, 'XII': 12, 'XIII': 13, 'XIV': 14, 'XV': 15,
        'XVI': 16, 'XVII': 17, 'XVIII': 18, 'XIX': 19, 'XX': 20, 'XXI': 21
    }
    
    for num, name in major_arcana:
        num_int = roman_to_int.get(num, 0)
        filename = f"major_{num_int:02d}_{name.lower().replace(' ', '_')}.png"
        generate_card("major", name, num, os.path.join(output_dir, filename))
    
    # Minor Arcana suits
    suits = [
        ("wands", "Wands"),
        ("cups", "Cups"),
        ("swords", "Swords"),
        ("pentacles", "Pentacles"),
    ]
    
    number_names = {
        1: "Ace",
        2: "Two",
        3: "Three",
        4: "Four",
        5: "Five",
        6: "Six",
        7: "Seven",
        8: "Eight",
        9: "Nine",
        10: "Ten",
        11: "Page",
        12: "Knight",
        13: "Queen",
        14: "King",
    }
    
    for suit_key, suit_name in suits:
        for num in range(1, 15):
            card_name = f"{number_names[num]} of {suit_name}"
            
            if num == 1:
                filename = f"{suit_key}_01_ace.png"
            elif num <= 10:
                filename = f"{suit_key}_{num:02d}.png"
            else:
                court_names = {11: "page", 12: "knight", 13: "queen", 14: "king"}
                filename = f"{suit_key}_{num:02d}_{court_names[num]}.png"
            
            generate_card(suit_key, card_name, str(num), os.path.join(output_dir, filename))
    
    print(f"\nAll 78 placeholder cards generated in: {output_dir}")


if __name__ == "__main__":
    generate_all_placeholders()
