# features.py
from PIL import Image, ImageDraw, ImageFont
import io

def create_palette_image(palette: list) -> bytes:
    """
    Takes a list of colors and creates a PNG image.
    Returns the image as bytes for Streamlit download.
    """
   
    swatch_width = 300
    swatch_height = 300
    text_height = 80
    total_width = swatch_width * len(palette)
    total_height = swatch_height + text_height


    img = Image.new("RGB", (total_width, total_height), "#1a1a2e")
    draw = ImageDraw.Draw(img)

    for i, color in enumerate(palette):
        x = i * swatch_width
        r, g, b = color["rgb"]
        draw.rectangle(
            [x, 0, x + swatch_width, swatch_height],
            fill=(r, g, b)
        )
        draw.text(
            (x + 10, swatch_height + 10),
            color["name"],
            fill="white"
        )

        
        draw.text(
            (x + 10, swatch_height + 35),
            color["hex"],
            fill="#a78bfa"
        )


        draw.text(
            (x + 10, swatch_height + 58),
            f"RGB {r},{g},{b}",
            fill="#6b7280"
        )

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer.getvalue()