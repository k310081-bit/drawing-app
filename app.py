import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import io

# ページ設定
st.set_page_config(page_title="むすこくんのおえかきアプリ", layout="wide")

# --- 🌈 虹色とキラキラの魔法 (CSSエフェクト) ---
# ここで、線がキラキラ光って色がかわる「まほう」をかけているよ！
st.markdown("""
    <style>
    /* 線のまわりを、虹色に光らせながら色を変化させるアニメーション */
    @keyframes rainbow-neon {
        0% { filter: hue-rotate(0deg) drop-shadow(0 0 5px rgba(255,0,0,0.8)) drop-shadow(0 0 15px rgba(255,0,0,0.4)); }
        25% { filter: hue-rotate(90deg) drop-shadow(0 0 5px rgba(255,255,0,0.8)) drop-shadow(0 0 15px rgba(255,255,0,0.4)); }
        50% { filter: hue-rotate(180deg) drop-shadow(0 0 5px rgba(0,255,0,0.8)) drop-shadow(0 0 15px rgba(0,255,0,0.4)); }
        75% { filter: hue-rotate(270deg) drop-shadow(0 0 5px rgba(0,255,255,0.8)) drop-shadow(0 0 15px rgba(0,255,255,0.4)); }
        100% { filter: hue-rotate(360deg) drop-shadow(0 0 5px rgba(255,0,255,0.8)) drop-shadow(0 0 15px rgba(255,0,255,0.4)); }
    }

    /* 「にじいろペン」の時だけ、この魔法をキャンバスにかける */
    .rainbow-mode canvas {
        animation: rainbow-neon 4s linear infinite;
    }

    /* アプリ全体の背景を少し可愛く */
    .stApp {
        background-color: #fffaf0; /* やさしいクリーム色 */
        background-image: radial-gradient(#ffd700 1px, transparent 1px); /* 金色のドット */
        background-size: 30px 30px;
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

# --- 色と魔法の設定 ---
canvas_container_class = "" # 初期化

if tool_type == "にじいろペン":
    # 虹色のベースになる明るい色
    stroke_color = "#FF00FF" 
    st.sidebar.markdown("---")
    st.sidebar.success("🌟 いまは「まほうの にじいろ」だよ！\n\nせんが キラキラ ひかるよ！")
    # キャンバスに魔法をかけるための目印
    canvas_container_class = "rainbow-mode"
elif tool_type == "けしごむ":
    stroke_color = "#FFFFFF"
else:
    stroke_color = st.sidebar.color_picker("なにいろに する？", "#FF00FF")

# 3歳児でも描きやすいように、少し太めを初期値に
stroke_width = st.sidebar.slider("ふとさ", 1, 100, 30)

# --- キャンバスの設置 ---
# 魔法をかけるためのクラスをdivに設定
st.markdown(f'<div class="{canvas_container_class}">', unsafe_allow_html=True)

canvas_result = st_canvas(
    fill_color="rgba(255, 255, 255, 0)", # 塗りつぶしは透明に
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color="#FFFFFF", # キャンバスの背景は白
    height=700,
    width=1000,
    drawing_mode=drawing_mode,
    key="canvas",
)

st.markdown('</div>', unsafe_allow_html=True)

# --- 保存機能 ---
if canvas_result.image_data is not None:
    # 注: 保存される画像には、CSSのキラキラエフェクトは反映されません
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