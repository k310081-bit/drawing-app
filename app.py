import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import io

# ページ設定
st.set_page_config(page_title="むすこくんのおえかきアプリ", layout="wide")

# --- 🌈 虹色とキラキラの魔法 (CSSエフェクト) ---
st.markdown("""
    <style>
    /* キャンバス内の線（にじいろペン）を虹色に変化させるアニメーション */
    @keyframes rainbow-glow {
        0% { filter: hue-rotate(0deg) drop-shadow(0 0 5px #FF00FF); }
        50% { filter: hue-rotate(180deg) drop-shadow(0 0 15px #00FFFF); }
        100% { filter: hue-rotate(360deg) drop-shadow(0 0 5px #FF00FF); }
    }

    /* 「にじいろ」が選ばれている時だけ、キャンバス全体を魔法の空間にする */
    .rainbow-mode iframe {
        animation: rainbow-glow 3s linear infinite;
        border: 10px solid;
        border-image: linear-gradient(45deg, red, orange, yellow, green, blue, indigo, violet) 1;
    }

    /* キラキラした背景の装飾 */
    .stApp {
        background-color: #f0faff;
        background-image: radial-gradient(#ffffff 1px, transparent 1px);
        background-size: 20px 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("✨ どでか！にじいろ・おえかきボード ✨")

# --- サイドバーの設定 ---
st.sidebar.header("🎨 どうぐ箱")

tool_type = st.sidebar.selectbox(
    "なにで かく？",
    ("にじいろペン", "ふつうのペン", "しかく", "まる", "けしごむ")
)

mode_map = {
    "にじいろペン": "freedraw",
    "ふつうのペン": "freedraw",
    "しかく": "rect",
    "まる": "circle",
    "けしごむ": "freedraw"
}
drawing_mode = mode_map[tool_type]

# --- 色の決定 ---
if tool_type == "にじいろペン":
    # 虹色のベースカラー（CSSで回転させるので、鮮やかな色ならOK）
    stroke_color = "#FF00FF" 
    st.sidebar.success("🌟 いまは「まほうの にじいろ」だよ！")
    # キャンバスを虹色モードにするためのコンテナ
    canvas_container_class = "rainbow-mode"
elif tool_type == "けしごむ":
    stroke_color = "#FFFFFF"
    canvas_container_class = ""
else:
    stroke_color = st.sidebar.color_picker("なにいろに する？", "#FF00FF")
    canvas_container_class = ""

stroke_width = st.sidebar.slider("ふとさ", 1, 100, 30)

# --- キャンバスの設置 ---
# HTMLのdivで包んで、CSSアニメーションを適用できるようにする
st.markdown(f'<div class="{canvas_container_class}">', unsafe_allow_html=True)

canvas_result = st_canvas(
    fill_color="rgba(255, 255, 255, 0)",
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color="#FFFFFF",
    height=700,
    width=1000,
    drawing_mode=drawing_mode,
    key="canvas",
)

st.markdown('</div>', unsafe_allow_html=True)

# --- 保存機能 ---
if canvas_result.image_data is not None:
    img_data = canvas_result.image_data
    img_pil = Image.fromarray(img_data.astype('uint8'), 'RGBA')
    
    buf = io.BytesIO()
    img_pil.save(buf, format="PNG")
    byte_im = buf.getvalue()

    st.sidebar.markdown("---")
    st.sidebar.download_button(
        label="🌈 できた絵をほぞんする",
        data=byte_im,
        file_name="musuko_no_e.png",
        mime="image/png"
    )