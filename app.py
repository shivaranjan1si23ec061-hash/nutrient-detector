import streamlit as st
import numpy as np
from PIL import Image, ImageOps, ImageFilter
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
        ["Vitamin A", "Vitamin B12", "Vitamin C", "Vitamin D", "Vitamin E", "Iron", "Calcium"]
    )

st.sidebar.write("---")
st.sidebar.caption("Upload an image to begin the analysis.")

# ---------------------------------------------------------
# Recommendations Database (Vitamin E Added)
# ---------------------------------------------------------
VITAMIN_RECOMMENDATIONS = {
    "Vitamin A": [
        "Carrots", "Sweet Potatoes", "Spinach", "Egg Yolks", "Pumpkin", "Vitamin A Capsules"
    ],
    "Vitamin B12": [
        "Milk & Dairy", "Chicken", "Fish (Tuna / Salmon)", "Eggs", "B12 Tablets"
    ],
    "Vitamin C": [
        "Oranges", "Lemons", "Strawberries", "Broccoli", "Vitamin C Chewable Tablets"
    ],
    "Vitamin D": [
        "Sunlight Exposure", "Fortified Milk", "Egg Yolks", "Mushrooms", "Vitamin D3 Supplements"
    ],
    "Vitamin E": [
        "Almonds", "Sunflower Seeds", "Spinach", "Avocado", "Vitamin E Capsules"
    ],
    "Iron": [
        "Spinach", "Red Meat", "Beetroot", "Dates", "Iron Syrup / Tablets"
    ],
    "Calcium": [
        "Milk", "Curd", "Paneer", "Almonds", "Calcium + Vitamin D Tablets"
    ]
}

# ---------------------------------------------------------
# Dummy predictor (Vitamin E added)
# ---------------------------------------------------------
def dummy_predict():
    vitamins = {
        "Vitamin A": random.uniform(0.2, 0.95),
        "Vitamin B12": random.uniform(0.2, 0.95),
        "Vitamin C": random.uniform(0.2, 0.95),
        "Vitamin D": random.uniform(0.2, 0.95),
        "Vitamin E": random.uniform(0.2, 0.95),   # ADDED
        "Iron": random.uniform(0.2, 0.95),
        "Calcium": random.uniform(0.2, 0.95),
    }

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
# Fake heatmap generator
# ---------------------------------------------------------
def fake_heatmap(image):
    img = image.convert("RGB")
    heat = img.filter(ImageFilter.EMBOSS)
    heat = ImageOps.colorize(heat.convert("L"), black="blue", white="red")
    return heat

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

    with col2:
        st.subheader("🔥 Feature Heatmap")
        heat_img = fake_heatmap(img)
        st.image(heat_img)

    st.write("---")

    # ---------------------------------------------------------
    # Prediction
    # ---------------------------------------------------------
    with st.spinner("Analyzing your image..."):
        time.sleep(2)
        prediction = dummy_predict()

    st.subheader("🧪 Vitamin Analysis Report")

    # ---------------------------------------------------------
    # SINGLE MODE
    # ---------------------------------------------------------
    if analysis_type == "Single Vitamin Analysis":
        vit = selected_vitamin
        data = prediction[vit]

        st.metric(
            label=f"{vit} Level ({data['status']})",
            value=f"{data['confidence']*100:.1f}%"
        )

        if data["status"] == "❌ Deficient":
            st.error(f"⚠️ Low {vit} detected.")
        elif data["status"] == "⚠️ Borderline":
            st.warning(f"{vit} level is borderline.")
        else:
            st.success(f"{vit} is normal.")

        st.subheader(f"🍎 Foods & Products to Recover from {vit}")
        for item in VITAMIN_RECOMMENDATIONS[vit]:
            st.write(f"✔ {item}")

    # ---------------------------------------------------------
    # FULL REPORT
    # ---------------------------------------------------------
    else:
        for vit, data in prediction.items():
            st.write(f"### 🟦 {vit}")
            st.progress(data["confidence"])
            st.write(f"**Status:** {data['status']}")
            st.write(f"**Confidence:** {data['confidence']*100:.1f}%")

            if data["status"] != "✅ Normal":
                st.write("#### 🍎 Recommended Recovery Items:")
                for item in VITAMIN_RECOMMENDATIONS[vit]:
                    st.write(f"- {item}")

            st.write("---")

    st.warning("⚠️ This is an AI estimation. Consult a doctor for medical advice.")
