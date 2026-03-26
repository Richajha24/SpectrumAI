# SpectrumAI 🎨
### AI-Powered Color Palette Generator

A web application that generates custom color palettes based on a mood, theme or idea using AI.

🔗 **Live Demo:** https://spectrumai-24.streamlit.app

---

## What it does

You type in a mood or theme (like "sunset beach" or "dark academia") and the app uses AI to generate a matching color palette with color names, HEX codes, RGB values and a short description for each color.

---

## Features

- Generate 3 to 8 colors based on any mood or theme
- Choose a category like Interior Design, Fashion, Website UI and more
- Copy HEX codes with one click
- Download the palette as a PNG image or TXT file

---

## Tech Stack

- **Python** — core language
- **Streamlit** — web app framework
- **Groq API (LLaMA 3)** — AI model for generating palettes
- **Pillow** — for creating the downloadable PNG image

---

## How to run locally

1. Clone the repository
```bash
git clone https://github.com/Richajha24/SpectrumAI.git
cd SpectrumAI
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Add your Groq API key — create a `.env` file in the root folder
```
GROQ_API_KEY=your_api_key_here
```

4. Run the app
```bash
streamlit run main.py
```

---

## Project Structure

```
SpectrumAI/
├── main.py                     # Streamlit UI
├── color_palette_generator.py  # AI palette generation using Groq
├── features.py                 # PNG image creation
├── requirements.txt
├── .streamlit/
│   └── config.toml             # Theme configuration
├── bg9.png                     # Background image
└── logo3.png                   # App logo
```

 College Mini Project