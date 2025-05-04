import streamlit as st
import cv2
import numpy as np
from PIL import Image

st.markdown('<p style="color:white; font-size:50px;">AI มองเหรียญยังไง?</p>', unsafe_allow_html=True)
st.markdown('<p style="color:white; font-size:30px;">อัปโหลดภาพเหรียญ แล้วดูว่า AI ตรวจเจอทั้งหมดกี่เหรียญ</p>', unsafe_allow_html=True)

st.markdown('<p style="color:white; font-size:20px;">📸 อัปโหลดภาพ</p>', unsafe_allow_html=True)
uploaded_file = st.file_uploader("",type=["jpg", "jpeg", "png","webp"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    img_np = np.array(image)
    output = img_np.copy()
    gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
    gray = cv2.medianBlur(gray, 5)

    # ตรวจจับวงกลมด้วย HoughCircles
    circles = cv2.HoughCircles(
        gray,
        cv2.HOUGH_GRADIENT,
        dp=1.2,
        minDist=30,
        param1=50,
        param2=30,
        minRadius=10,
        maxRadius=80
    )

    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        for (x, y, r) in circles:
            cv2.circle(output, (x, y), r, (0, 255, 0), 3)
        st.image(output, caption=f"ตรวจเจอ {len(circles)} เหรียญ", use_container_width=True)
        st.success(f"✅ ตรวจพบ {len(circles)} วงกลม (อาจเป็นเหรียญ)")
    else:
        st.image(img_np, caption="ไม่พบเหรียญใด ๆ", use_container_width=True)
        st.warning("🚫 ไม่พบวงกลมในภาพ กรุณาลองภาพใหม่")

bg="""
<style>
.stApp {
    background-image: url("https://play-lh.googleusercontent.com/bTf6otSgyG8RzTZ1Vkum7pFeOHwhFpgwE9M7gUv9KT-ta9mxuwqeH-zDSFtAbeQTXTQ=w648-h364-rw");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}
</style>
"""
st.html(bg)



st.info("พัฒนาโดย ไทเกอร์")
