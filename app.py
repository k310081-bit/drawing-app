import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import io
import random
import base64

# =========================
# ページ設定
# =========================
st.set_page_config(
    page_title="むすこくんのおえかきアプリ",
    layout="wide"
)

# =========================
# CSS
# =========================
st.markdown("""
<style>
.stApp {
    background-color: #fffaf0;
    background-image: radial-gradient(#ffd700 1px, transparent 1px);
    background-size: 30px 30px;
}

.big-button button {
    font-size: 28px !important;
    padding: 20px !important;
}
</style>
""", unsafe_allow_html=True)

st.title("✨ どでか！にじいろ・おえかきボード ✨")

# =========================
# セッション初期化
# =========================
if "draw_count" not in st.session_state:
    st.session_state.draw_count = 0

if "canvas_key" not in st.session_state:
    st.session_state.canvas_key = "canvas_0"

# =========================
# サイドバー
# =========================
st.sidebar.header("🎨 どうぐ箱")

tool_type = st.sidebar.selectbox(
    "なにで かく？",
    ("にじいろペン", "ふつうのペン", "しかく", "まる", "スタンプ", "けしごむ")
)

mode_map = {
    "にじいろペン": "freedraw",
    "ふつうのペン": "freedraw",
    "しかく": "rect",
    "まる": "circle",
    "スタンプ": "point",
    "けしごむ": "freedraw",
}

drawing_mode = mode_map[tool_type]

# =========================
# にじいろ
# =========================
def random_rainbow_color():
    return random.choice([
        "#FF0000", "#FF7F00", "#FFFF00",
        "#00FF00", "#00FFFF", "#0000FF", "#8B00FF"
    ])

if tool_type == "にじいろペン":
    if "rainbow_color" not in st.session_state:
        st.session_state.rainbow_color = random_rainbow_color()

    stroke_color = st.session_state.rainbow_color

    if st.sidebar.button("🌈 いろをかえる"):
        st.session_state.rainbow_color = random_rainbow_color()

elif tool_type == "けしごむ":
    stroke_color = "#FFFFFF"
else:
    stroke_color = st.sidebar.color_picker("いろ", "#FF00FF")

stroke_width = st.sidebar.slider("ふとさ", 1, 100, 30)

# =========================
# スタンプ設定
# =========================
stamp_map = {
    "🌈": "rainbow",
    "🦕": "dino",
    "⭐": "star",
    "🚗": "car",
}

selected_stamp = None
if tool_type == "スタンプ":
    selected_stamp = st.sidebar.radio(
        "どのスタンプ？",
        list(stamp_map.keys())
    )

# =========================
# Canvas
# =========================
canvas_result = st_canvas(
    fill_color="rgba(255,255,255,0)",
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color="#FFFFFF",
    height=650,
    width=1000,
    drawing_mode=drawing_mode,
    key=st.session_state.canvas_key,
)

# =========================
# 効果音（描いたらポン！）
# =========================
if canvas_result.json_data and len(canvas_result.json_data["objects"]) > st.session_state.draw_count:
    st.session_state.draw_count += 1

    audio_html = """
    <audio autoplay>
        <source src="https://www.soundjay.com/buttons/sounds/button-16.mp3">
    </audio>
    """
    st.markdown(audio_html, unsafe_allow_html=True)

# =========================
# 🎆 花火演出
# =========================
if st.session_state.draw_count > 0 and st.session_state.draw_count % 10 == 0:
    st.balloons()
    st.success("🎆 すごい！たくさん かいたね！")

# =========================
# 🧹 全部消す
# =========================
st.markdown("<div class='big-button'>", unsafe_allow_html=True)
if st.button("🧹 ぜんぶ けす！"):
    st.session_state.canvas_key = f"canvas_{random.randint(0,99999)}"
    st.session_state.draw_count = 0
st.markdown("</div>", unsafe_allow_html=True)

# =========================
# 保存
# =========================
if canvas_result.image_data is not None:
    img = Image.fromarray(
        canvas_result.image_data.astype("uint8"),
        "RGBA"
    )

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    byte_img = buf.getvalue()

    st.sidebar.markdown("---")
    st.sidebar.download_button(
        "💾 できたえを ほぞん",
        data=byte_img,
        file_name="musuko_no_e.png",
        mime="image/png",
    )
