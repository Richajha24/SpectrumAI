# color_palette_generator.py
# Purpose: Calls Groq AI and returns a color palette

import os
import json
from groq import Groq
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_palette(mood: str, category: str, num_colors: int = 5) -> list:
    """
    Sends user mood + category to Groq AI.
    Returns a list of color dictionaries.
    """
    prompt = f"""
    You are a professional color palette designer.
    Generate a color palette for: "{mood}" in the context of "{category}".
    Return ONLY a JSON array with exactly {num_colors} colors.
    Format:
    [
      {{
        "name": "Color Name",
        "hex": "#RRGGBB",
        "rgb": [R, G, B],
        "description": "one sentence why this color fits"
      }}
    ]
    Return ONLY the JSON array. No explanation. No markdown.
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    raw = response.choices[0].message.content.strip()

    # Clean response in case AI adds backticks
    if "```" in raw:
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]

    palette = json.loads(raw.strip())
    return palette


# ── TEST ──
if __name__ == "__main__":
    result = generate_palette("tangled movie bedroom", "Interior Design", 5)
    for color in result:
        print(f"{color['name']} → {color['hex']}")