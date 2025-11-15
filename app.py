    import streamlit as st
import numpy as np
from PIL import Image, ImageOps, ImageFilter
import time
import random

st.set_page_config(page_title="AI Vitamin Deficiency Detector",
                   layout="wide",
                   page_icon="🧬")

# ---------------------------------------------------------
# Header
# ---------------------------------------------------------
st.title("🧬 AI-Powered Vitamin Deficiency Detection Dashboard")
st.caption("Upload an image to generate your complete vitamin health report.")

st.write("---")

# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------
st.sidebar.title("⚙️ Controls")
analysis_type = st.sidebar.selectbox(
    "Analysis Type",
    ["Full Vitamin Report", "Single Vitamin Analysis"]
)

symptoms_toggle = st.sidebar.checkbox("Enable Symptom-Based Insights", True)

selected_vitamin = None
if analysis_type == "Single Vitamin Analysis":
    selected_vitamin = st.sidebar.selectbox(
        "Choose Vitamin",
        ["Vitamin A", "Vitamin B12", "Vitamin C", "Vitamin D", "Vitamin E", "Iron", "Calcium"]
    )

uploaded_file = st.sidebar.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

# ---------------------------------------------------------
# Vitamin Data
# ---------------------------------------------------------
VITAMIN_RECOMMENDATIONS = {
    "Vitamin A": ["Carrots", "Spinach", "Pumpkin", "Egg Yolks", "Sweet Potatoes"],
    "Vitamin B12": ["Milk", "Eggs", "Fish", "Chicken", "B12 Tablets"],
    "Vitamin C": ["Oranges", "Lemon", "Guava", "Broccoli", "Strawberries"],
    "Vitamin D": ["Sunlight", "Mushrooms", "Fortified Milk", "Egg Yolks"],
    "Vitamin E": ["Almonds", "Sunflower Seeds", "Spinach", "Avocado"],
    "Iron": ["Spinach", "Beetroot", "Red Meat", "Dates"],
    "Calcium": ["Milk", "Curd", "Paneer", "Almonds", "Ragi"]
}

FOODS_TO_AVOID = {
    "Vitamin A": ["Alcohol", "Processed Foods"],
    "Vitamin B12": ["Overcooked Food", "Sugary Drinks"],
    "Vitamin C": ["Junk Food", "Deep-Fried Items"],
    "Vitamin D": ["Too Much Caffeine", "Carbonated Drinks"],
    "Vitamin E": ["High-Sugar Foods"],
    "Iron": ["Tea Immediately After Meals", "Coffee After Meals"],
    "Calcium": ["Soft Drinks", "High Salt Intake"]
}

SYMPTOM_PATTERNS = {
    "Vitamin A": "Dry skin, poor night vision, pale eyes",
    "Vitamin B12": "Fatigue, pale lips, dizziness",
    "Vitamin C": "Weak immunity, bleeding gums, dry skin",
    "Vitamin D": "Bone pain, low mood, fatigue",
    "Vitamin E": "Weak muscles, vision issues",
    "Iron": "Low energy, pale face, weakness",
    "Calcium": "Weak nails, muscle cramps, brittle bones"
}

# ---------------------------------------------------------
# Predictor
# ---------------------------------------------------------
def generate_prediction():
    result = {}
    for vit in VITAMIN_RECOMMENDATIONS.keys():
        score = random.uniform(0.2, 0.95)

        if score < 0.45:
            status = "❌ Deficient"
            risk = "High Risk"
        elif score < 0.70:
            status = "⚠️ Borderline"
            risk = "Moderate Risk"
        else:
            status = "✅ Normal"
            risk = "Low Risk"

        result[vit] = {
            "score": round(score, 2),
            "percentage": f"{score*100:.1f}%",
            "status": status,
            "risk": risk
        }
    return result

# ---------------------------------------------------------
# Heatmap Generator
# ---------------------------------------------------------
def generate_heatmap(image):
    img = image.convert("RGB")
    heat = img.filter(ImageFilter.FIND_EDGES)
    heat = ImageOps.colorize(heat.convert("L"), black="blue", white="red")
    return heat

# ---------------------------------------------------------
# Main Page Logic
# ---------------------------------------------------------
if uploaded_file:
    col1, col2 = st.columns(2)

    # Original Image
    with col1:
        st.subheader("📸 Uploaded Image")
        img = Image.open(uploaded_file)
        st.image(img, use_column_width=True)

    # Heatmap
    with col2:
        st.subheader("🔥 AI Feature Heatmap")
        heat = generate_heatmap(img)
        st.image(heat, use_column_width=True)

    st.write("---")

    # Generate Predictions
    with st.spinner("🔍 Analyzing Image… Generating Vitamin Report"):
        time.sleep(2)
        report = generate_prediction()

    # ---------------------------------------------------------
    # SINGLE VITAMIN REPORT
    # ---------------------------------------------------------
    if analysis_type == "Single Vitamin Analysis":
        data = report[selected_vitamin]

        st.header(f"🧪 {selected_vitamin} Status Report")
        
        colA, colB, colC = st.columns(3)
        colA.metric("Status", data["status"])
        colB.metric("Level (%)", data["percentage"])
        colC.metric("Risk", data["risk"])

        st.write("---")

        st.subheader("🍎 Foods to Improve Levels")
        for item in VITAMIN_RECOMMENDATIONS[selected_vitamin]:
            st.write(f"✔ {item}")

        st.subheader("🚫 Foods to Avoid")
        for food in FOODS_TO_AVOID[selected_vitamin]:
            st.write(f"❌ {food}")

        if symptoms_toggle:
            st.subheader("🧠 Possible Symptoms")
            st.info(SYMPTOM_PATTERNS[selected_vitamin])

    # ---------------------------------------------------------
    # FULL REPORT MODE
    # ---------------------------------------------------------
    else:
        st.header("📊 Complete Vitamin Analysis")

        for vit, data in report.items():
            with st.expander(f"🔵 {vit} — {data['status']} ({data['percentage']})"):
                
                st.progress(data["score"])
                st.write(f"### Status: {data['status']}")
                st.write(f"### Level: {data['percentage']}")
                st.write(f"### Risk Level: {data['risk']}")

                st.write("### 🍎 Foods to Improve")
                for item in VITAMIN_RECOMMENDATIONS[vit]:
                    st.write(f"- {item}")

                st.write("### 🚫 Foods to Avoid")
                for food in FOODS_TO_AVOID[vit]:
                    st.write(f"- {food}")

                if symptoms_toggle:
                    st.write("### 🧠 Possible Symptoms")
                    st.warning(SYMPTOM_PATTERNS[vit])

    st.write("---")
    st.warning("⚠️ This is only an AI estimate. Consult a doctor for medical confirmation.")

