import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import io

# ページ設定：iPadで最大化して表示
st.set_page_config(page_title="むすこくんのおえかきアプリ", layout="wide")

st.title("🎨 どでか！おえかきボード")

# --- サイドバーの設定 ---
st.sidebar.header("どうぐ箱")

tool_type = st.sidebar.selectbox(
    "なにで かく？",
    ("ペン", "しかく", "まる", "けしごむ")
)

mode_map = {
    "ペン": "freedraw",
    "しかく": "rect",
    "まる": "circle",
    "けしごむ": "freedraw"
}
drawing_mode = mode_map[tool_type]

# 初期値を鮮やかな色（#FF00FF）に設定
if tool_type == "けしごむ":
    stroke_color = "#FFFFFF"
else:
    stroke_color = st.sidebar.color_picker("なにいろに する？", "#FF00FF")

stroke_width = st.sidebar.slider("ふとさ", 1, 100, 20) # 3歳児向けに最大値を100、初期値を20に

# --- キャンバスの設置 ---
# 背景を白に、サイズを大きく設定
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color="#FFFFFF",
    height=800, # 縦幅を大きく
    use_container_width=True, # 横幅をiPadの画面幅いっぱいに
    drawing_mode=drawing_mode,
    key="canvas",
)

# --- 保存機能 ---
if canvas_result.image_data is not None:
    img_data = canvas_result.image_data
    img_pil = Image.fromarray(img_data.astype('uint8'), 'RGBA')
    
    # 画像をダウンロード可能なバッファに変換
    buf = io.BytesIO()
    img_pil.save(buf, format="PNG")
    byte_im = buf.getvalue()

    st.sidebar.download_button(
        label="できた絵をほぞんする",
        data=byte_im,
        file_name="musuko_no_e.png",
        mime="image/png"
    )