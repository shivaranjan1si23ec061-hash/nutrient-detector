import streamlit as st
import numpy as np
import cv2
from PIL import Image, ImageOps
import time
import random

st.set_page_config(page_title="Vitamin Deficiency Detector", layout="wide")

# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------
st.sidebar.title("⚙️ Settings")
analysis_type = st.sidebar.selectbox(
    "Analysis Type", 
    ["Full Vitamin Report", "Single Vitamin Analysis"]
)

selected_vitamin = None
if analysis_type == "Single Vitamin Analysis":
    selected_vitamin = st.sidebar.selectbox(
        "Choose Vitamin",
        ["Vitamin A", "Vitamin B12", "Vitamin C", "Vitamin D", "Iron", "Calcium"]
    )

st.sidebar.write("---")
st.sidebar.caption("Upload an image to begin the analysis.")

# ---------------------------------------------------------
# Title
# ---------------------------------------------------------
st.title("🧬 AI-Powered Vitamin Deficiency Detector")
st.write("Upload your face or hand image for AI-based nutritional analysis.")

# ---------------------------------------------------------
# Dummy advanced predictor
# (You can later replace this with a real ML model)
# ---------------------------------------------------------
def advanced_dummy_predict(img_array):
    vitamins = {
        "Vitamin A": random.uniform(0.2, 0.95),
        "Vitamin B12": random.uniform(0.2, 0.95),
        "Vitamin C": random.uniform(0.2, 0.95),
        "Vitamin D": random.uniform(0.2, 0.95),
        "Iron": random.uniform(0.2, 0.95),
        "Calcium": random.uniform(0.2, 0.95),
    }

    # Deficiency based on score
    result = {}
    for vit, score in vitamins.items():
        if score < 0.45:
            status = "❌ Deficient"
        elif score < 0.70:
            status = "⚠️ Borderline"
        else:
            status = "✅ Normal"

        result[vit] = {"confidence": round(score, 2), "status": status}

    return result

# ---------------------------------------------------------
# Heatmap generator
# ---------------------------------------------------------
def generate_heatmap(image):
    try:
        img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        heatmap = cv2.applyColorMap(img_gray, cv2.COLORMAP_JET)
        return heatmap
    except:
        return None

# ---------------------------------------------------------
# Upload
# ---------------------------------------------------------
uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📸 Uploaded Image")
        img = Image.open(uploaded_file)
        st.image(img)

    # Convert to OpenCV image
    img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    # Generate heatmap
    heatmap_img = generate_heatmap(img_cv)

    if heatmap_img is not None:
        with col2:
            st.subheader("🔥 Feature Heatmap")
            st.image(heatmap_img, channels="BGR")

    st.write("---")

    # ---------------------------------------------------------
    # Prediction
    # ---------------------------------------------------------
    with st.spinner("Analyzing image with AI..."):
        time.sleep(2)
        prediction = advanced_dummy_predict(img_cv)

    st.subheader("🧪 Vitamin Analysis Report")

    if analysis_type == "Single Vitamin Analysis":
        vit = selected_vitamin
        st.metric(
            label=f"{vit} Level ({prediction[vit]['status']})", 
            value=f"{prediction[vit]['confidence']*100:.1f}%"
        )

        if prediction[vit]["status"] == "❌ Deficient":
            st.error(f"⚠️ Low {vit} detected. Consider dietary improvements.")
        elif prediction[vit]["status"] == "⚠️ Borderline":
            st.warning(f"{vit} level is borderline. Monitor closely.")
        else:
            st.success(f"{vit} is at a healthy level!")
    else:
        # Full vitamin report
        for vit, data in prediction.items():
            st.write(f"### 🟦 {vit}")
            st.progress(data["confidence"])
            st.write(f"**Status:** {data['status']}")
            st.write(f"**Confidence:** {data['confidence']*100:.1f}%")
            st.write("---")

    # ---------------------------------------------------------
    # Recommendations
    # ---------------------------------------------------------
    st.subheader("🥗 Personalized Health Recommendations")

    for vit, data in prediction.items():
        if data["status"] == "❌ Deficient":
            st.error(f"**{vit}: Deficient** → Increase intake immediately.")
        elif data["status"] == "⚠️ Borderline":
            st.warning(f"**{vit}: Borderline** → Maintain diet carefully.")
        else:
            st.success(f"**{vit}: Normal** → Keep it up!")

    st.write("---")
    st.caption("⚠️ This tool is for educational purposes only. Not medical advice.")
