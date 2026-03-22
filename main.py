#main.py
import streamlit as st
from color_palette_generator import generate_palette
from features import create_palette_image
from PIL import Image
import base64
import streamlit.components.v1 as components

icon = Image.open("logo3.png")
st.set_page_config(page_title="SpectrumAI", page_icon=icon, layout="wide")

def get_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

bg = get_base64("bg9.png")
logo = get_base64("logo3.png")

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@600;700&family=DM+Sans:wght@400;500;600&display=swap');

.stApp {{
    background: linear-gradient(rgba(10,8,6,0.72), rgba(10,8,6,0.72)),
                url("data:image/jpg;base64,{bg}") center/cover fixed;
}}
html, body, [class*="css"] {{ font-family: 'DM Sans', sans-serif !important; color: #f0ece4 !important; }}
#MainMenu, footer, header {{ visibility: hidden; }}
.block-container {{ padding: 0 1.5rem 3rem !important; max-width: 100% !important; }}

.navbar {{ display:flex; align-items:center; gap:16px; padding:20px 10px 16px; margin-bottom:32px; }}
.navbar img {{ height:64px; width:64px; border-radius:50%; border:2px solid rgba(201,168,76,0.5); }}
.navbar h1 {{ font-family:'Cormorant Garamond',serif; font-size:2.6rem; font-weight:700; color:#f0ece4; margin:0; }}
.navbar p  {{ font-size:.72rem; letter-spacing:3px; text-transform:uppercase; color:#c9a84c; margin:4px 0 0; }}
.gold-line {{ height:1px; background:linear-gradient(90deg,transparent,#c9a84c,transparent); opacity:.4; margin-bottom:36px; }}

.section-title {{ font-size:.7rem; font-weight:600; letter-spacing:4px; text-transform:uppercase; color:#c9a84c; margin-bottom:10px; }}
.result-title {{ font-family:'Cormorant Garamond',serif; font-size:2.2rem; font-weight:600; color:#f0ece4; margin:0 0 24px; }}

[data-testid="stHorizontalBlock"]:has([data-testid="stTextInput"]) {{
    background:rgba(20,18,16,0.72); border:1px solid rgba(201,168,76,0.18);
    border-radius:14px; padding:28px 28px 22px !important;
    box-shadow:0 8px 32px rgba(0,0,0,0.5); margin-bottom:28px !important;
}}
label[data-testid="stWidgetLabel"] p {{
    font-size:.72rem !important; font-weight:600 !important;
    letter-spacing:2px !important; text-transform:uppercase !important; color:#c9a84c !important;
}}
.stTextInput input {{
    background:rgba(255,255,255,0.05) !important; border:1px solid rgba(201,168,76,0.25) !important;
    border-radius:10px !important; color:#f0ece4 !important; font-size:1rem !important;
    padding:13px 16px !important; height:52px !important;
}}
.stTextInput input:focus {{ border-color:#c9a84c !important; box-shadow:0 0 0 3px rgba(201,168,76,0.1) !important; }}
.stTextInput input::placeholder {{ color:#8a8078 !important; }}
.stSelectbox > div > div {{
    background:rgba(255,255,255,0.05) !important; border:1px solid rgba(201,168,76,0.25) !important;
    border-radius:10px !important; color:#f0ece4 !important; min-height:52px !important;
}}

div[data-testid="stButton"] > button {{
    background:linear-gradient(135deg, #4a2020, #331515) !important;
    color:#c9a84c !important; border:1px solid rgba(201,168,76,0.25) !important;
    border-radius:12px !important; padding:14px 0 !important;
    font-size:1rem !important; font-weight:600 !important; letter-spacing:1.5px !important;
    text-transform:uppercase !important; width:100% !important;
    box-shadow:0 4px 20px rgba(30,10,10,0.5) !important;
    transition:all .2s ease !important;
}}
div[data-testid="stButton"] > button:hover {{
    background:linear-gradient(135deg, #5c2a2a, #4a2020) !important;
    border-color:rgba(201,168,76,0.45) !important;
    transform:translateY(-2px) !important;
}}

.card {{
    background:#222; border:1.5px solid rgba(201,168,76,0.35);
    border-radius:3px; padding:10px 10px 26px;
    box-shadow:0 10px 30px rgba(0,0,0,0.6);
    transform:rotate(var(--tilt,0deg));
    transition:transform .25s, box-shadow .25s;
    margin-bottom:8px;
}}
.card:hover {{
    transform:rotate(0deg) scale(1.03) translateY(-5px);
    box-shadow:0 20px 50px rgba(0,0,0,0.7), 0 0 0 1.5px rgba(201,168,76,0.5);
    position:relative; z-index:10;
}}
.tilt-l {{ --tilt: -0.8deg; }}
.tilt-r {{ --tilt:  0.8deg; }}
.tilt-0 {{ --tilt:  0deg;   }}

.card-swatch {{ width:100%; height:220px; border-radius:2px; display:block; }}
.card-body {{ padding:14px 8px 4px; }}
.card-name {{ font-family:'Cormorant Garamond',serif; font-size:1.1rem; font-weight:600; color:#f0ece4; margin-bottom:7px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }}
.hex-chip {{ display:inline-flex; align-items:center; gap:6px; background:rgba(201,168,76,0.12); border:1px solid rgba(201,168,76,0.35); color:#e8cc7a; font-family:'Courier New',monospace; font-size:.8rem; font-weight:700; padding:4px 10px; border-radius:4px; margin-bottom:6px; letter-spacing:1.5px; }}
.hex-dot {{ width:10px; height:10px; border-radius:50%; display:inline-block; border:1px solid rgba(255,255,255,0.15); flex-shrink:0; }}
.rgb-text {{ font-size:.72rem; color:#8a8078; margin-bottom:4px; }}
.desc-text {{ font-size:.76rem; color:#5a5248; font-style:italic; line-height:1.4; display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden; }}

[data-testid="stHorizontalBlock"]:has([data-testid="stDownloadButton"]) {{
    background:rgba(20,18,16,0.72); border:1px solid rgba(201,168,76,0.18);
    border-radius:14px; padding:22px 28px !important;
    box-shadow:0 8px 32px rgba(0,0,0,0.5); margin-top:8px !important;
}}
div[data-testid="stDownloadButton"] > button {{
    background:transparent !important; border:1px solid rgba(201,168,76,0.28) !important;
    color:#c9a84c !important; border-radius:10px !important; padding:12px 0 !important;
    font-weight:600 !important; font-size:.88rem !important; letter-spacing:1px !important;
    text-transform:uppercase !important; width:100% !important;
    transition:all .2s ease !important;
}}
div[data-testid="stDownloadButton"] > button:hover {{
    background:rgba(201,168,76,0.08) !important; color:#e8cc7a !important;
    border-color:#c9a84c !important; transform:translateY(-1px) !important;
}}

hr {{ border:none !important; border-top:1px solid rgba(201,168,76,0.12) !important; margin:28px 0 !important; }}
.footer {{ text-align:center; font-size:.78rem; color:#5a5248; padding:10px 0 28px; letter-spacing:1px; }}
</style>
""", unsafe_allow_html=True)

if "palette" not in st.session_state:
    st.session_state.palette = None
if "mood" not in st.session_state:
    st.session_state.mood = ""

components.html("""
<style>
div[data-baseweb="slider"] div[role="progressbar"],
div[data-baseweb="slider"] > div > div:nth-child(2) {
    background: #5c3d1e !important;
}
div[data-baseweb="slider"] div[role="slider"] {
    background: #8a6030 !important;
    border-color: #c9a84c !important;
    box-shadow: 0 0 0 4px rgba(201,168,76,0.12) !important;
}
</style>
<script>
function fixSlider() {
    document.querySelectorAll('div[data-baseweb="slider"] div[role="progressbar"]')
        .forEach(el => el.style.setProperty('background','#5c3d1e','important'));
    document.querySelectorAll('div[data-baseweb="slider"] div[role="slider"]')
        .forEach(el => {
            el.style.setProperty('background','#8a6030','important');
            el.style.setProperty('border-color','#c9a84c','important');
        });
}
fixSlider(); setTimeout(fixSlider, 600); setTimeout(fixSlider, 1500);
</script>
""", height=0)

st.markdown(f"""
<div class="navbar">
    <img src="data:image/png;base64,{logo}" alt="logo" />
    <div>
        <h1>SpectrumAI</h1>
        <p>AI-Powered Color Palette Generator</p>
    </div>
</div>
<div class="gold-line"></div>
""", unsafe_allow_html=True)

st.markdown('<p class="section-title">✦ Describe your palette</p>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1.8, 1.8, 0.9])
with col1:
    mood = st.text_input("Mood, theme or idea", placeholder="e.g. dark academia library, sunset beach…")
with col2:
    category = st.selectbox("Category", [
        "Interior Design", "Fashion & Clothing", "Art & Painting",
        "Event & Party", "Nature & Outdoors", "Brand & Logo", "Website & UI", "Other"
    ])
with col3:
    num_colors = st.slider("Colors", 3, 8, 5)

st.write("")
_, btn, _ = st.columns([2.5, 1, 2.5])
with btn:
    clicked = st.button("Generate Palette →")

if clicked:
    if not mood.strip():
        st.error("Please enter a mood or theme first.")
    else:
        with st.spinner("Generating your palette…"):
            try:
                st.session_state.palette = generate_palette(mood.strip(), category, num_colors)
                st.session_state.mood = mood.strip()
            except Exception as e:
                st.error(f"Something went wrong: {e}")

if st.session_state.palette:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        f'<p class="section-title">✦ Your palette</p>'
        f'<p class="result-title">"{st.session_state.mood}"</p>',
        unsafe_allow_html=True
    )

    tilts = ["tilt-l", "tilt-0", "tilt-r", "tilt-l", "tilt-0", "tilt-r", "tilt-l", "tilt-0"]

    ROW_SIZE = 5
    palette = st.session_state.palette
    chunks = [palette[i : i + ROW_SIZE] for i in range(0, len(palette), ROW_SIZE)]
    global_i = 0

    for chunk in chunks:
        cols = st.columns(ROW_SIZE, gap="medium")
        for col, color in zip(cols, chunk):
            r, g, b = color["rgb"]
            hex_val = color["hex"]
            tilt_cls = tilts[global_i % len(tilts)]

            with col:
                st.markdown(f"""
                <div class="card {tilt_cls}">
                    <div class="card-swatch" style="background:{hex_val};"></div>
                    <div class="card-body">
                        <div class="card-name">{color['name']}</div>
                        <div class="hex-chip">
                            <span class="hex-dot" style="background:{hex_val};"></span>
                            {hex_val}
                        </div>
                        <div class="rgb-text">rgb({r}, {g}, {b})</div>
                        <div class="desc-text">{color['description']}</div>
                    </div>
                </div>""", unsafe_allow_html=True)

                components.html(f"""
                <button
                    onclick="
                        navigator.clipboard.writeText('{hex_val}')
                            .then(() => {{ this.textContent = '✓ Copied!'; setTimeout(() => this.textContent = 'Copy HEX', 1500); }})
                            .catch(() => {{
                                var ta = document.createElement('textarea');
                                ta.value = '{hex_val}';
                                document.body.appendChild(ta);
                                ta.select();
                                document.execCommand('copy');
                                document.body.removeChild(ta);
                                this.textContent = '✓ Copied!';
                                setTimeout(() => this.textContent = 'Copy HEX', 1500);
                            }});
                    "
                    style="
                        width:100%; background:transparent;
                        border:1px solid rgba(201,168,76,0.3);
                        color:#c9a84c; padding:8px 0; border-radius:8px;
                        font-size:.78rem; letter-spacing:1px;
                        cursor:pointer; font-family:'DM Sans',sans-serif;
                        transition: background .2s, color .2s, border-color .2s;
                    "
                    onmouseover="this.style.background='rgba(201,168,76,0.1)';this.style.color='#e8cc7a';this.style.borderColor='#c9a84c';"
                    onmouseout="this.style.background='transparent';this.style.color='#c9a84c';this.style.borderColor='rgba(201,168,76,0.3)';"
                >Copy HEX</button>
                """, height=40)

            global_i += 1

        if len(chunks) > 1:
            st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<p class="section-title">✦ Export your palette</p>', unsafe_allow_html=True)

    dl1, dl2, _, _ = st.columns([1, 1, 0.4, 1.6])
    with dl1:
        try:
            st.download_button(
                "⬇ Download PNG",
                create_palette_image(st.session_state.palette),
                file_name=f"SpectrumAI_{st.session_state.mood[:20]}.png",
                mime="image/png",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"Image error: {e}")
    with dl2:
        txt = "\n".join([
            f"{c['name']} | HEX: {c['hex']} | RGB: {c['rgb']}"
            for c in st.session_state.palette
        ])
        st.download_button(
            "⬇ Download TXT", txt,
            file_name=f"SpectrumAI_{st.session_state.mood[:20]}.txt",
            mime="text/plain",
            use_container_width=True
        )

st.divider()
st.markdown('<p class="footer">Made with ❤️ by the SpectrumAI team</p>', unsafe_allow_html=True)