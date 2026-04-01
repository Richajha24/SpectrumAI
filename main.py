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

def save_to_history(palette, mood):
    entry = {"palette": palette, "mood": mood}
    prev = st.session_state.history
    if prev and prev[0]["mood"] == mood and prev[0]["palette"] == palette:
        return
    st.session_state.history = ([entry] + prev)[:5]

defaults = {
    "palette": None,
    "mood": "",
    "last_category": "Interior Design",
    "last_details": "",
    "locks": [],
    "history": [],
}
for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

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

.navbar {{ display: flex; align-items: center; gap: 16px; padding: 20px 10px 16px; margin-bottom: 32px; }}
.navbar img {{ height: 64px; width: 64px; border-radius: 50%; border: 2px solid rgba(201,168,76,0.5); }}
.navbar h1 {{ font-family: 'Cormorant Garamond', serif; font-size: 2.6rem; font-weight: 700; color: #f0ece4; margin: 0; }}
.navbar p {{ font-size: .72rem; letter-spacing: 3px; text-transform: uppercase; color: #c9a84c; margin: 4px 0 0; }}
.gold-line {{ height: 1px; background: linear-gradient(90deg, transparent, #c9a84c, transparent); opacity: .4; margin-bottom: 36px; }}

.section-title {{ font-size: .7rem; font-weight: 600; letter-spacing: 4px; text-transform: uppercase; color: #c9a84c; margin-bottom: 10px; }}
.result-title {{ font-family: 'Cormorant Garamond', serif; font-size: 2.2rem; font-weight: 600; color: #f0ece4; margin: 0 0 12px; }}

[data-testid="stHorizontalBlock"]:has([data-testid="stTextInput"]) {{
    background: rgba(20,18,16,0.72); border: 1px solid rgba(201,168,76,0.18);
    border-radius: 14px; padding: 24px 28px !important;
    box-shadow: 0 8px 32px rgba(0,0,0,0.5); margin-bottom: 28px !important;
    align-items: flex-end !important;
}}
label[data-testid="stWidgetLabel"] p {{
    font-size: .72rem !important; font-weight: 600 !important;
    letter-spacing: 2px !important; text-transform: uppercase !important; color: #c9a84c !important;
}}

.stTextInput > div > div {{ height: 48px !important; }}
.stTextInput input {{
    background: rgba(255,255,255,0.05) !important; border: 1px solid rgba(201,168,76,0.25) !important;
    border-radius: 10px !important; color: #f0ece4 !important; font-size: 1rem !important;
    padding: 0 16px !important; height: 48px !important; line-height: 48px !important;
    box-sizing: border-box !important;
}}
.stTextInput input:focus {{ border-color: #c9a84c !important; box-shadow: 0 0 0 3px rgba(201,168,76,0.1) !important; }}
.stTextInput input::placeholder {{ color: #8a8078 !important; }}

.stSelectbox > div > div {{
    background: rgba(255,255,255,0.05) !important; border: 1px solid rgba(201,168,76,0.25) !important;
    border-radius: 10px !important; color: #f0ece4 !important;
    height: 48px !important; min-height: 48px !important;
}}
[data-baseweb="select"] > div:first-child {{
    height: 48px !important; padding-top: 0 !important; padding-bottom: 0 !important;
    display: flex !important; align-items: center !important;
    background: transparent !important; border: none !important;
}}
[data-baseweb="select"] input {{ pointer-events: none !important; cursor: default !important; caret-color: transparent !important; }}

div[data-testid="stSlider"] {{
    background: rgba(255,255,255,0.05) !important; border: 1px solid rgba(201,168,76,0.25) !important;
    border-radius: 10px !important; padding: 8px 16px 6px !important; box-sizing: border-box !important;
}}

.stTextArea textarea {{
    background: rgba(255,255,255,0.05) !important; border: 1px solid rgba(201,168,76,0.25) !important;
    border-radius: 10px !important; color: #f0ece4 !important; font-size: .92rem !important;
    padding: 12px 16px !important;
}}
.stTextArea textarea:focus {{ border-color: #c9a84c !important; box-shadow: 0 0 0 3px rgba(201,168,76,0.1) !important; }}
.stTextArea textarea::placeholder {{ color: #8a8078 !important; }}

.stCheckbox label {{ font-size: .72rem !important; color: #8a8078 !important; gap: 6px !important; }}
.stCheckbox label:hover {{ color: #c9a84c !important; }}

div[data-testid="stButton"] > button {{
    background: linear-gradient(135deg, #4a2020, #331515) !important;
    color: #c9a84c !important; border: 1px solid rgba(201,168,76,0.25) !important;
    border-radius: 12px !important; padding: 14px 0 !important;
    font-size: 1rem !important; font-weight: 600 !important; letter-spacing: 1.5px !important;
    text-transform: uppercase !important; width: 100% !important;
    box-shadow: 0 4px 20px rgba(30,10,10,0.5) !important; transition: all .2s ease !important;
}}
div[data-testid="stButton"] > button:hover {{
    background: linear-gradient(135deg, #5c2a2a, #4a2020) !important;
    border-color: rgba(201,168,76,0.45) !important; transform: translateY(-2px) !important;
}}

[data-testid="stHorizontalBlock"]:has([data-testid="stDownloadButton"]) {{
    background: rgba(20,18,16,0.72); border: 1px solid rgba(201,168,76,0.18);
    border-radius: 14px; padding: 22px 28px !important;
    box-shadow: 0 8px 32px rgba(0,0,0,0.5); margin-top: 8px !important;
}}
div[data-testid="stDownloadButton"] > button {{
    background: transparent !important; border: 1px solid rgba(201,168,76,0.28) !important;
    color: #c9a84c !important; border-radius: 10px !important; padding: 12px 0 !important;
    font-weight: 600 !important; font-size: .88rem !important; letter-spacing: 1px !important;
    text-transform: uppercase !important; width: 100% !important; transition: all .2s ease !important;
}}
div[data-testid="stDownloadButton"] > button:hover {{
    background: rgba(201,168,76,0.08) !important; color: #e8cc7a !important;
    border-color: #c9a84c !important; transform: translateY(-1px) !important;
}}

.card {{
    background: #222; border: 1.5px solid rgba(201,168,76,0.35); border-radius: 3px;
    padding: 10px 10px 14px; box-shadow: 0 10px 30px rgba(0,0,0,0.6);
    transform: rotate(var(--tilt, 0deg)); transition: transform .25s, box-shadow .25s; margin-bottom: 8px;
}}
.card.locked {{ border-color: rgba(201,168,76,0.75) !important; box-shadow: 0 0 0 1.5px rgba(201,168,76,0.4), 0 10px 30px rgba(0,0,0,0.6); }}
.card:hover {{
    transform: rotate(0deg) scale(1.03) translateY(-5px);
    box-shadow: 0 20px 50px rgba(0,0,0,0.7), 0 0 0 1.5px rgba(201,168,76,0.5);
    position: relative; z-index: 10;
}}
.tilt-l {{ --tilt: -0.8deg; }} .tilt-r {{ --tilt: 0.8deg; }} .tilt-0 {{ --tilt: 0deg; }}
.card-swatch {{ width: 100%; height: 200px; border-radius: 2px; display: block; }}
.card-body {{ padding: 14px 8px 4px; }}
.card-name {{ font-family: 'Cormorant Garamond', serif; font-size: 1.1rem; font-weight: 600; color: #f0ece4; margin-bottom: 7px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
.hex-chip {{ display: inline-flex; align-items: center; gap: 6px; background: rgba(201,168,76,0.12); border: 1px solid rgba(201,168,76,0.35); color: #e8cc7a; font-family: 'Courier New', monospace; font-size: .8rem; font-weight: 700; padding: 4px 10px; border-radius: 4px; margin-bottom: 6px; letter-spacing: 1.5px; }}
.hex-dot {{ width: 10px; height: 10px; border-radius: 50%; display: inline-block; border: 1px solid rgba(255,255,255,0.15); flex-shrink: 0; }}
.rgb-text {{ font-size: .72rem; color: #8a8078; margin-bottom: 4px; }}
.desc-text {{ font-size: .76rem; color: #5a5248; font-style: italic; line-height: 1.4; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }}

.hist-strip {{ display: flex; border-radius: 6px; overflow: hidden; border: 1px solid rgba(201,168,76,0.2); margin-bottom: 5px; cursor: pointer; transition: border-color .2s; }}
.hist-strip:hover {{ border-color: rgba(201,168,76,0.5); }}
.hist-mood {{ font-size: .68rem; color: #8a8078; text-align: center; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; padding: 0 4px; }}

.presentation-tip {{
    background: rgba(201,168,76,0.07); border: 1px solid rgba(201,168,76,0.2);
    border-radius: 10px; padding: 12px 18px; font-size: .78rem;
    color: #c9a84c; margin-bottom: 18px; letter-spacing: .5px;
}}

hr {{ border: none !important; border-top: 1px solid rgba(201,168,76,0.12) !important; margin: 28px 0 !important; }}
.footer {{ text-align: center; font-size: .78rem; color: #5a5248; padding: 10px 0 28px; letter-spacing: 1px; }}
</style>
""", unsafe_allow_html=True)

components.html("""
<style>
div[data-baseweb="slider"] div[role="progressbar"],
div[data-baseweb="slider"] > div > div:nth-child(2) { background: #5c3d1e !important; }
div[data-baseweb="slider"] div[role="slider"] {
    background: #8a6030 !important; border-color: #c9a84c !important;
    box-shadow: 0 0 0 4px rgba(201,168,76,0.12) !important;
}
</style>
<script>
function fixSlider() {
    document.querySelectorAll('div[data-baseweb="slider"] div[role="progressbar"]')
        .forEach(el => el.style.setProperty('background', '#5c3d1e', 'important'));
    document.querySelectorAll('div[data-baseweb="slider"] div[role="slider"]')
        .forEach(el => {
            el.style.setProperty('background', '#8a6030', 'important');
            el.style.setProperty('border-color', '#c9a84c', 'important');
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
        "Event & Party", "Nature & Outdoors", "Brand & Logo",
        "Website & UI", "Presentation", "Other"
    ])
with col3:
    num_colors = st.slider("Colors", 3, 8, 5)

details = ""
if category == "Presentation":
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="presentation-tip">
        ✦ &nbsp;Tip — describe your topic, audience, and tone for best results
        (e.g. "Tech startup pitch for investors, confident and modern")
    </div>""", unsafe_allow_html=True)
    details = st.text_area(
        "Presentation details",
        placeholder="Topic, audience, tone… e.g. Marketing campaign for a luxury skincare brand",
        height=90
    )

st.write("")
_, btn_col, _ = st.columns([2.5, 1, 2.5])
with btn_col:
    clicked = st.button("Generate Palette →")

if clicked:
    if not mood.strip():
        st.error("Please enter a mood or theme first.")
    else:
        with st.spinner("Generating your palette…"):
            try:
                palette = generate_palette(mood.strip(), category, num_colors, details)
                st.session_state.palette = palette
                st.session_state.mood = mood.strip()
                st.session_state.last_category = category
                st.session_state.last_details = details
                st.session_state.locks = [False] * len(palette)
                save_to_history(palette, mood.strip())
            except Exception as e:
                st.error(f"Something went wrong: {e}")

if st.session_state.palette:
    palette = st.session_state.palette

    while len(st.session_state.locks) < len(palette):
        st.session_state.locks.append(False)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        f'<p class="section-title">✦ Your palette</p>'
        f'<p class="result-title">"{st.session_state.mood}"</p>',
        unsafe_allow_html=True
    )

    tilts = ["tilt-l", "tilt-0", "tilt-r", "tilt-l", "tilt-0", "tilt-r", "tilt-l", "tilt-0"]
    ROW_SIZE = 5
    chunks = [palette[i:i+ROW_SIZE] for i in range(0, len(palette), ROW_SIZE)]
    global_i = 0

    for chunk in chunks:
        cols = st.columns(ROW_SIZE, gap="medium")
        for col, color in zip(cols, chunk):
            r, g, b = color["rgb"]
            hex_val = color["hex"]
            tilt_cls = tilts[global_i % len(tilts)]
            is_locked = st.session_state.locks[global_i]
            locked_cls = "locked" if is_locked else ""

            with col:
                st.markdown(f"""
                <div class="card {tilt_cls} {locked_cls}">
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
                <button onclick="
                    navigator.clipboard.writeText('{hex_val}')
                        .then(()=>{{this.textContent='✓ Copied!';setTimeout(()=>this.textContent='Copy HEX',1500);}})
                        .catch(()=>{{
                            var ta=document.createElement('textarea');
                            ta.value='{hex_val}';document.body.appendChild(ta);
                            ta.select();document.execCommand('copy');
                            document.body.removeChild(ta);
                            this.textContent='✓ Copied!';
                            setTimeout(()=>this.textContent='Copy HEX',1500);
                        }});"
                    style="width:100%;background:transparent;border:1px solid rgba(201,168,76,0.3);
                           color:#c9a84c;padding:8px 0;border-radius:8px;font-size:.78rem;
                           letter-spacing:1px;cursor:pointer;font-family:'DM Sans',sans-serif;
                           transition:background .2s,color .2s,border-color .2s;margin-bottom:4px;"
                    onmouseover="this.style.background='rgba(201,168,76,0.1)';this.style.color='#e8cc7a';this.style.borderColor='#c9a84c';"
                    onmouseout="this.style.background='transparent';this.style.color='#c9a84c';this.style.borderColor='rgba(201,168,76,0.3)';"
                >Copy HEX</button>
                """, height=40)

                lock_val = st.checkbox(
                    "🔒 Lock color" if is_locked else "🔓 Lock color",
                    value=is_locked,
                    key=f"lock_{global_i}"
                )
                if lock_val != is_locked:
                    st.session_state.locks[global_i] = lock_val
                    st.rerun()

            global_i += 1

        if len(chunks) > 1:
            st.markdown("<br>", unsafe_allow_html=True)

    any_locked = any(st.session_state.locks[:len(palette)])
    if any_locked:
        st.markdown("<br>", unsafe_allow_html=True)
        _, regen_col, _ = st.columns([2.5, 1, 2.5])
        with regen_col:
            if st.button("Regenerate Unlocked →"):
                locked_colors = [
                    palette[i] if st.session_state.locks[i] else None
                    for i in range(len(palette))
                ]
                with st.spinner("Regenerating unlocked colors…"):
                    try:
                        new_palette = generate_palette(
                            st.session_state.mood,
                            st.session_state.last_category,
                            len(palette),
                            st.session_state.last_details,
                            locked_colors
                        )
                        st.session_state.palette = new_palette
                        save_to_history(new_palette, st.session_state.mood)
                        st.rerun()
                    except Exception as e:
                        st.error(f"Something went wrong: {e}")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<p class="section-title">✦ Export your palette</p>', unsafe_allow_html=True)

    _, dl_col, _ = st.columns([1, 1, 1])
    with dl_col:
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

if st.session_state.history:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<p class="section-title">✦ Recent palettes</p>', unsafe_allow_html=True)

    hist_cols = st.columns(len(st.session_state.history), gap="medium")
    for idx, (hcol, entry) in enumerate(zip(hist_cols, st.session_state.history)):
        with hcol:
            swatches = "".join(
                f'<div style="background:{c["hex"]};flex:1;height:28px;"></div>'
                for c in entry["palette"]
            )
            st.markdown(f"""
            <div class="hist-strip">{swatches}</div>
            <div class="hist-mood">"{entry['mood'][:22]}"</div>
            """, unsafe_allow_html=True)
            if st.button("Restore", key=f"hist_{idx}", use_container_width=True):
                st.session_state.palette = entry["palette"]
                st.session_state.mood = entry["mood"]
                st.session_state.locks = [False] * len(entry["palette"])
                st.rerun()

st.divider()
st.markdown('<p class="footer">Made with ❤️ by the SpectrumAI team</p>', unsafe_allow_html=True)