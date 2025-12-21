import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import numpy as np

# ページ設定：iPadで見やすいようにワイドモードに
st.set_page_config(page_title="むすこくんのおえかきアプリ", layout="wide")

st.title("🎨 おえかきボード")

# --- サイドバーの設定 ---
st.sidebar.header("どうぐ箱")

# 1. 描画モードの選択（スタンプ機能も含む）
tool_type = st.sidebar.selectbox(
    "なにで かく？",
    ("ペン", "しかく", "まる", "けしごむ")
)

# ツール名から内部的なモードに変換
mode_map = {
    "ペン": "freedraw",
    "しかく": "rect",
    "まる": "circle",
    "けしごむ": "freedraw"
}
drawing_mode = mode_map[tool_type]

# 2. 色の選択
if tool_type == "けしごむ":
    stroke_color = "#FFFFFF" # 消しゴムは白
else:
    stroke_color = st.sidebar.color_picker("なにいろに する？", "#000000")

# 3. ペンの太さ
stroke_width = st.sidebar.slider("ふとさ", 1, 50, 10)

# --- キャンバスの設置 ---
st.subheader("しろいところに かいてね！")

canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",  # 図形の中身の色
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color="#FFFFFF",
    height=500,
    width=700,
    drawing_mode=drawing_mode,
    key="canvas",
)

# --- 保存機能 ---
if canvas_result.image_data is not None:
    # 画像データを取り出し
    img_data = canvas_result.image_data
    
    # プレビュー表示
    # st.image(img_data) # 必要なら表示
    
    # ダウンロードボタン
    img_pil = Image.fromarray(img_data.astype('uint8'), 'RGBA')
    st.sidebar.download_button(
        label="できた絵をほぞんする",
        data=img_pil.tobytes(), # 簡易的な例です。本来はBytesIOを使います
        file_name="my_drawing.png",
        mime="image/png"
    )

st.write("※ iPadでは、画面の端をスワイプしてスクロールしないように気をつけてね！")