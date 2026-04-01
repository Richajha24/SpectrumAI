import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

try:
    import streamlit as st
    api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    api_key = os.environ.get("GROQ_API_KEY", "")

client = Groq(api_key=api_key)

CATEGORY_HINTS = {
    "Interior Design":    "Use livable, balanced tones like warm neutrals, earthy accents and calming shades.",
    "Fashion & Clothing": "Use wearable, trendy tones. Think seasonal palettes and fabric-inspired shades.",
    "Art & Painting":     "Use expressive, high-contrast or harmonious artistic combinations.",
    "Event & Party":      "Use festive, celebratory tones with energy and contrast.",
    "Nature & Outdoors":  "Use organic, earthy tones inspired by landscapes, plants, water and sky.",
    "Brand & Logo":       "Use strong, memorable colors that communicate brand identity.",
    "Website & UI":       "Use clean, modern tones with good contrast. Avoid clashing colors.",
    "Presentation":       "Use professional, legible colors suitable for slides. Prioritize contrast between background and text colors. Avoid overly bright or clashing tones. Colors should feel authoritative and focused.",
    "Other":              "Use colors that best match the mood described.",
}


def classify_mood(mood: str) -> str:
    """
    Pre-classification step: identifies the visual identity of the input
    before generating the palette, using low temperature for factual recall.
    """
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{
            "role": "user",
            "content": f"""In one sentence, describe the core visual identity of "{mood}".
Focus on: signature colors, dominant hues, and what makes it visually recognizable.
Example: "Spiderman is defined by red, blue, and black — the colors of his iconic suit."
Now do this for: "{mood}" """
        }],
        temperature=0.3
    )
    return response.choices[0].message.content.strip()


def generate_palette(mood, category, num_colors=5, details="", locked_colors=None):
    """
    locked_colors: list of length num_colors where each item is either
                   a color dict (locked, keep as-is) or None (regenerate this slot).
                   Pass None to generate all colors fresh.
    """
    hint = CATEGORY_HINTS.get(category, CATEGORY_HINTS["Other"])
    details_block = f"Additional context: {details.strip()}\n" if details.strip() else ""

    # ── pre-classify the mood for better color anchoring ──────────────────────
    visual_identity = classify_mood(mood)

    # ── figure out what needs generating ──────────────────────────────────────
    locked_block = ""
    positions_to_fill = list(range(num_colors))

    if locked_colors:
        locked_items      = [(i, c) for i, c in enumerate(locked_colors) if c is not None]
        positions_to_fill = [i for i, c in enumerate(locked_colors) if c is None]
        num_to_generate   = len(positions_to_fill)

        if num_to_generate == 0:
            return list(locked_colors)

        if locked_items:
            locked_block = "These colors are already fixed — generate NEW colors that complement them:\n"
            for _, c in locked_items:
                locked_block += f"  - {c['name']} ({c['hex']})\n"
            locked_block += "\n"
    else:
        num_to_generate = num_colors

    prompt = f"""
You are an expert color palette designer with deep knowledge of visual identities, pop culture, brands, characters, and design.

Generate a color palette for: "{mood}"
Visual identity of "{mood}": {visual_identity}
Category: {category}
{details_block}{locked_block}Guidance: {hint}

Rules:
- First, identify what "{mood}" represents:
    * If it's a CHARACTER (e.g. Spiderman, Batman, Elsa) → use their ICONIC costume/signature colors
    * If it's a MOVIE/SHOW (e.g. The Matrix, Breaking Bad) → use the dominant visual palette of that work
    * If it's a BRAND (e.g. Nike, Coca-Cola) → use their brand colors
    * If it's an ABSTRACT MOOD (e.g. calm, melancholy, festive) → use colors that emotionally match
    * If it's a PLACE/NATURE (e.g. ocean, autumn forest) → use colors literally found there
- Colors must be strongly and unmistakably tied to "{mood}". A viewer should immediately recognize the reference.
- The {category} context should influence tone/shade choices within the theme.
- No two colors should be too similar.

CRITICAL HEX ACCURACY RULES — violations will break the application:
- The hex code MUST literally be that color. If you name it "Red", the hex must be in range #AA0000–#FF3333. If you name it "Blue", hex must be a real blue like #0000FF or #1A3CFF. NEVER assign an orange or yellow hex to something called "red".
- For Spiderman: use #CC0000 (red), #0033CC (blue), #111111 (black) as your anchors.
- For Batman: use #1A1A1A (black), #FFD700 (yellow), #2C2C2C (dark grey).
- Double-check every hex before returning: does the actual color match the name?
- Return EXACTLY {num_to_generate} colors as a JSON array.

Output only the JSON array, no explanation:
[
  {{
    "name": "Color Name",
    "hex": "#RRGGBB",
    "rgb": [R, G, B],
    "description": "one sentence connecting this color to {mood}"
  }}
]
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    raw = response.choices[0].message.content.strip()
    if "```" in raw:
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]

    new_colors = json.loads(raw.strip())

    # ── merge locked + new colors back into original positions ─────────────────
    if locked_colors:
        result = list(locked_colors)
        j = 0
        for i in positions_to_fill:
            if j < len(new_colors):
                result[i] = new_colors[j]
                j += 1
        return result

    return new_colors