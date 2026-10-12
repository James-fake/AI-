import streamlit as st
import requests
import os
import zipfile
import uuid
from pathlib import Path

st.set_page_config(page_title="🐾 AI 动物表情包", layout="wide", page_icon="🐾")
st.title("🐾 AI 动物表情包生成器")
st.markdown("**上传任意动物照片，自动生成9张专业表情包**")

col1, col2 = st.columns([1, 1])
with col1:
    uploaded_file = st.file_uploader("上传动物照片 (jpg/png)", type=["jpg", "png", "jpeg"], help="推荐正面高清照片")
    style = st.selectbox("风格选择", ["可爱卡通", "写实", "3D", "油画"])
    emoji_type = st.selectbox("表情类型", ["开心", "愤怒", "害羞", "惊讶", "微笑", "酷炫", "吐舌", "可爱", "生气"])

with col2:
    if st.button("🚀 生成9张表情包", type="primary", use_container_width=True):
        if not uploaded_file:
            st.error("请先上传照片！")
        else:
            with st.spinner("正在调用 AI 生成中... (6-8秒)"):
                files = {"animal_photo": (uploaded_file.name, uploaded_file.getvalue())}
                params = {"style": style.lower(), "emoji_type": emoji_type}
                
                resp = requests.post("http://localhost:8000/generate", files=files, params=params)
                
                if resp.status_code == 200:
                    st.success("✅ 生成完成！")
                    
                    output_dir = Path("uploads") / "generated"
                    output_dir.mkdir(parents=True, exist_ok=True)
                    
                    for i in range(9):
                        img_path = output_dir / f"sticker_{i+1}.webp"
                        if img_path.exists():
                            st.image(str(img_path), caption=f"表情{i+1}", use_column_width=True)
                    
                    zip_path = Path("exports") / f"{uuid.uuid4()}.zip"
                    zip_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    with zipfile.ZipFile(zip_path, 'w') as z:
                        for i in range(9):
                            img_path = output_dir / f"sticker_{i+1}.webp"
                            if img_path.exists():
                                z.write(img_path, f"sticker_{i+1}.webp")
                    
                    with open(zip_path, "rb") as f:
                        st.download_button("📥 下载ZIP (9张)", f, file_name=zip_path.name, mime="application/zip")
                    
                    st.success("分享到微信/QQ 超方便！")
                else:
                    st.error(f"生成失败：{resp.text}")

st.caption("隐私安全 · 完全本地运行 · 原始照片永不上传")
