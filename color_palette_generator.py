import os
import json
from groq import Groq
from dotenv import load_dotenv


load_dotenv()
import streamlit as st
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

CATEGORY_HINTS = {
    "Interior Design":    "Use livable, balanced tones like warm neutrals, earthy accents and calming shades.",
    "Fashion & Clothing": "Use wearable, trendy tones. Think seasonal palettes and fabric-inspired shades.",
    "Art & Painting":     "Use expressive, high-contrast or harmonious artistic combinations.",
    "Event & Party":      "Use festive, celebratory tones with energy and contrast.",
    "Nature & Outdoors":  "Use organic, earthy tones inspired by landscapes, plants, water and sky.",
    "Brand & Logo":       "Use strong, memorable colors that communicate brand identity.",
    "Website & UI":       "Use clean, modern tones with good contrast. Avoid clashing colors.",
    "Other":              "Use colors that best match the mood described.",
}

def generate_palette(mood, category, num_colors=5):
    hint = CATEGORY_HINTS.get(category, CATEGORY_HINTS["Other"])

    prompt = f"""
You are a color palette designer.

Generate a color palette for the mood: "{mood}"
Category: {category}
Guidance: {hint}

Rules:
- Colors must match "{mood}" visually and emotionally.
- The {category} context should influence the shades chosen.
- No two colors should be too similar.
- Return EXACTLY {num_colors} colors as a JSON array.

Output only the JSON array, no explanation:
[
  {{
    "name": "Color Name",
    "hex": "#RRGGBB",
    "rgb": [R, G, B],
    "description": "one sentence connecting this color to the mood"
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

    palette = json.loads(raw.strip())
    return palette