import streamlit as st
import numpy as np
from PIL import Image, ImageOps, ImageFilter
import time
import random

# -------------------------------
# PAGE CONFIG & GLOBAL CSS
# -------------------------------
st.set_page_config(page_title="Vitamin Deficiency Detector", layout="wide")

# 🔥 Modern UI Styling
st.markdown("""
<style>
/* Smooth cards */
div.stButton > button {
    border-radius: 12px;
    padding: 10px 25px;
    background: linear-gradient(90deg, #3A7BD5, #00D2FF);
    color: white;
    border: none;
}
div.stButton > button:hover {
    transform: scale(1.03);
}

/* Glass-card popup look */
.report-card {
    background: rgba(255,255,255,0.18);
    backdrop-filter: blur(12px);
    padding: 25px;
    border-radius: 18px;
    border: 1px solid rgba(255,255,255,0.3);
    margin-bottom: 25px;
}

/* Gradient titles */
h1, h2, h3 {
    background: -webkit-linear-gradient(#0072ff, #00c6ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Center image */
.center-img {
    display: block;
    margin-left: auto;
    margin-right: auto;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Sidebar Settings
# ---------------------------------------------------------
st.sidebar.title("⚙️ Analysis Settings")
analysis_type = st.sidebar.selectbox(
    "Analysis Type",
    ["Full Vitamin Report", "Single Vitamin Analysis"]
)

selected_vitamin = None
if analysis_type == "Single Vitamin Analysis":
    selected_vitamin = st.sidebar.selectbox(
        "Choose Vitamin",
        ["Vitamin A", "Vitamin B12", "Vitamin C", "Vitamin D", "Vitamin E", "Iron", "Calcium"]
    )

st.sidebar.write("---")
st.sidebar.caption("📤 Upload an image to begin the analysis.")

# ---------------------------------------------------------
# Recommendations
# ---------------------------------------------------------
VITAMIN_RECOMMENDATIONS = {
    "Vitamin A": ["Carrots", "Sweet Potatoes", "Spinach", "Egg Yolks", "Pumpkin", "Vitamin A Capsules"],
    "Vitamin B12": ["Milk & Dairy", "Chicken", "Fish", "Eggs", "B12 Tablets"],
    "Vitamin C": ["Oranges", "Lemons", "Strawberries", "Broccoli", "Vitamin C Tablets"],
    "Vitamin D": ["Sunlight", "Fortified Milk", "Egg Yolks", "Mushrooms", "Vitamin D3 Supplements"],
    "Vitamin E": ["Almonds", "Sunflower Seeds", "Spinach", "Avocado", "Vitamin E Capsules"],
    "Iron": ["Spinach", "Red Meat", "Beetroot", "Dates", "Iron Tablets"],
    "Calcium": ["Milk", "Curd", "Paneer", "Almonds", "Calcium Tablets"]
}

# ---------------------------------------------------------
# Predictor (improved)
# ---------------------------------------------------------
def dummy_predict():
    vitamins = {
        "Vitamin A": random.uniform(0.75, 1.0),
        "Vitamin B12": random.uniform(0.75, 1.0),
        "Vitamin C": random.uniform(0.75, 1.0),
        "Vitamin D": random.uniform(0.75, 1.0),
        "Vitamin E": random.uniform(0.75, 1.0),
        "Iron": random.uniform(0.75, 1.0),
        "Calcium": random.uniform(0.75, 1.0),
    }
    result = {}
    for vit, score in vitamins.items():
        if score >= 0.80:
            status = "✅ Normal"
        elif score >= 0.60:
            status = "⚠️ Borderline"
        else:
            status = "❌ Deficient"
        result[vit] = {"confidence": round(score, 2), "status": status}
    return result

# ---------------------------------------------------------
# Heatmap Effect
# ---------------------------------------------------------
def fake_heatmap(image):
    img = image.convert("RGB")
    heat = img.filter(ImageFilter.EMBOSS)
    heat = ImageOps.colorize(heat.convert("L"), black="blue", white="red")
    return heat

# ---------------------------------------------------------
# Main UI
# ---------------------------------------------------------
st.title("🩺 Vitamin Deficiency Detector Dashboard")

uploaded_file = st.file_uploader("📸 Upload Face Image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Uploaded Image")
        img = Image.open(uploaded_file)
        st.image(img, use_column_width=True, output_format='PNG')

    with col2:
        st.subheader("AI Heatmap Visualization")
        heat_img = fake_heatmap(img)
        st.image(heat_img, use_column_width=True)

    st.write("---")

    # Run prediction
    with st.spinner("🔍 Analyzing your face..."):
        time.sleep(1.8)
        prediction = dummy_predict()

    st.subheader("🧪 Vitamin Analysis Report")

    # ---------------------------------------------------------
    # Single Vitamin Mode
    # ---------------------------------------------------------
    if analysis_type == "Single Vitamin Analysis":
        vit = selected_vitamin
        data = prediction[vit]

        st.markdown("<div class='report-card'>", unsafe_allow_html=True)

        st.metric(
            label=f"{vit} Level ({data['status']})",
            value=f"{data['confidence']*100:.1f}%"
        )

        if data["status"] == "❌ Deficient":
            st.error(f"⚠️ Low {vit} detected.")
        elif data["status"] == "⚠️ Borderline":
            st.warning(f"{vit} level is borderline.")
        else:
            st.success(f"{vit} is normal ✨")

        st.subheader(f"🍎 Recommended Foods for {vit}")
        for item in VITAMIN_RECOMMENDATIONS[vit]:
            st.write(f"✔ {item}")

        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # Full Report Mode
    # ---------------------------------------------------------
    else:
        for vit, data in prediction.items():
            st.markdown("<div class='report-card'>", unsafe_allow_html=True)

            st.write(f"### 🟦 {vit}")
            st.progress(data["confidence"])
            st.write(f"**Status:** {data['status']}  |  **Confidence:** {data['confidence']*100:.1f}%")

            if data["status"] != "✅ Normal":
                st.write("#### 🍎 Recommended Items:")
                for item in VITAMIN_RECOMMENDATIONS[vit]:
                    st.write(f"- {item}")

            st.markdown("</div>", unsafe_allow_html=True)

    st.info("This is an AI estimation. For real diagnosis, consult a doctor.")
else:
    st.warning("📤 Please upload your image to begin analysis.")
