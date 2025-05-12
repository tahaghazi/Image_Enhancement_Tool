# app.py
import streamlit as st
from io import BytesIO
from PIL import Image
import MainCode as mc  # Import your image processing functions


def main():
    # Page config
    st.set_page_config(page_title="Image Enhancer", layout="wide")
    st.title("🖼️ Image Enhancement Dashboard")

    # Sidebar settings
    st.sidebar.header("Enhancement Controls")
    gamma = st.sidebar.slider("Gamma", 0.1, 5.0, 1.0, 0.1)
    hist_eq = st.sidebar.checkbox("Histogram Equalization")
    brightness = st.sidebar.slider("Brightness", 0.5, 2.0, 1.0, 0.1)
    contrast = st.sidebar.slider("Contrast", 0.5, 2.0, 1.0, 0.1)
    sharpness = st.sidebar.slider("Sharpness", 0.0, 2.0, 1.0, 0.1)
    saturation = st.sidebar.slider("Saturation", 0.0, 2.0, 1.0, 0.1)
    exposure_gain = st.sidebar.slider("Exposure", 0.5, 2.0, 1.0, 0.1)

    # File uploader
    uploaded_file = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])
    if not uploaded_file:
        st.info("Please upload an image to start enhancing.")
        return

    # Load image using MainCode API
    original = mc.load_image(uploaded_file)

    # Apply enhancements via MainCode functions
    enhanced = mc.apply_gamma(original, gamma)
    if hist_eq:
        enhanced = mc.apply_hist_eq(enhanced)
    enhanced = mc.adjust_brightness(enhanced, brightness)
    enhanced = mc.adjust_contrast(enhanced, contrast)
    enhanced = mc.adjust_sharpness(enhanced, sharpness)
    enhanced = mc.adjust_saturation(enhanced, saturation)
    enhanced = mc.adjust_exposure(enhanced, exposure_gain)

    # Display side by side
    col1, col2 = st.columns(2)
    with col1:
        st.header("Original")
        st.image(original, use_column_width=True)
    with col2:
        st.header("Enhanced")
        st.image(enhanced, use_column_width=True)

    # Download enhanced image
    buf = BytesIO()
    enhanced.save(buf, format="PNG")
    st.download_button(
        label="Download Enhanced Image",
        data=buf.getvalue(),
        file_name="enhanced.png",
        mime="image/png"
    )

if __name__ == '__main__':
    main()
