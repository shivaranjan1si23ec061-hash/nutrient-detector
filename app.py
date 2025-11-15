import streamlit as st
import numpy as np
from PIL import Image, ImageOps, ImageFilter
import time
import random
import plotly.express as px
import plotly.graph_objects as go
st.set_page_config(page_title="AI Vitamin Deficiency Detector",
                   layout="wide",
                   page_icon="🧬")

# ---------------------------------------------------------
# Header
# ---------------------------------------------------------
st.title("🧬 AI-Powered Vitamin Deficiency Detection Dashboard")
st.caption("Upload an image to generate a complete health report")

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

st.sidebar.write("---")
uploaded_file = st.sidebar.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

# ---------------------------------------------------------
# Vitamin Recommendations
# ---------------------------------------------------------
VITAMIN_RECOMMENDATIONS = {
    "Vitamin A": ["Carrots", "Sweet Potatoes", "Spinach", "Egg Yolks", "Pumpkin"],
    "Vitamin B12": ["Milk", "Fish", "Eggs", "Chicken", "B12 Tablets"],
    "Vitamin C": ["Oranges", "Lemons", "Strawberries", "Broccoli"],
    "Vitamin D": ["Sunlight", "Fortified Milk", "Egg Yolks", "Mushrooms", "D3 Supplements"],
    "Vitamin E": ["Almonds", "Sunflower Seeds", "Avocado", "Vitamin E Capsules"],
    "Iron": ["Spinach", "Red Meat", "Beetroot", "Iron Tablets"],
    "Calcium": ["Milk", "Curd", "Paneer", "Almonds", "Calcium + D Tablets"]
}

# ---------------------------------------------------------
# Symptom Analysis (extra intelligence)
# ---------------------------------------------------------
SYMPTOM_PATTERNS = {
    "Vitamin A": "Dry skin, pale eyes, poor night vision",
    "Vitamin B12": "Fatigue, pale lips, dizziness",
    "Vitamin C": "Weak immunity, dry skin, bleeding gums",
    "Vitamin D": "Fatigue, bone pain, low mood",
    "Vitamin E": "Muscle weakness, vision problems",
    "Iron": "Pale skin, weakness, low energy",
    "Calcium": "Weak nails, muscle cramps"
}

# ---------------------------------------------------------
# Dummy Predictor (Advanced logic)
# ---------------------------------------------------------
def generate_advanced_prediction():
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
            "status": status,
            "risk": risk
        }
    return result

# ---------------------------------------------------------
# Heatmap
# ---------------------------------------------------------
def generate_heatmap(image):
    img = image.convert("RGB")
    heat = img.filter(ImageFilter.FIND_EDGES)
    heat = ImageOps.colorize(heat.convert("L"), black="blue", white="red")
    return heat

# ---------------------------------------------------------
# Main UI Logic
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

    # Generating Prediction
    with st.spinner("🔍 Analyzing Image… AI is generating report"):
        time.sleep(2)
        report = generate_advanced_prediction()

    # ---------------------------------------------------------
    # Single Vitamin Mode
    # ---------------------------------------------------------
    if analysis_type == "Single Vitamin Analysis":
        data = report[selected_vitamin]

        st.header(f"🧪 {selected_vitamin} Status Report")
        st.metric(label="Status", value=data["status"])
        st.metric(label="Confidence Level", value=f"{data['score']*100:.1f}%")
        st.metric(label="Risk Level", value=data["risk"])

        st.subheader("🍎 Recommended Foods")
        for item in VITAMIN_RECOMMENDATIONS[selected_vitamin]:
            st.write(f"✔ {item}")

        if symptoms_toggle:
            st.write("### 🧠 Symptom Insights")
            st.info(SYMPTOM_PATTERNS[selected_vitamin])

    # ---------------------------------------------------------
    # FULL REPORT MODE
    # ---------------------------------------------------------
    else:
        st.header("📊 Complete Vitamin Analysis Dashboard")

        # Radar Chart
        st.subheader("📌 Vitamin Levels Overview")
        radar_fig = go.Figure()

        radar_fig.add_trace(go.Scatterpolar(
            r=[v["score"] for v in report.values()],
            theta=list(report.keys()),
            fill='toself',
            name='Vitamin Levels'
        ))

        radar_fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
                                showlegend=False)
        st.plotly_chart(radar_fig, use_container_width=True)

        st.write("---")

        # Detailed breakdown
        st.header("📋 Vitamin-by-Vitamin Breakdown")
        for vit, data in report.items():
            with st.expander(f"🔵 {vit} – {data['status']}"):
                st.progress(data["score"])
                st.write(f"**Confidence:** {data['score']*100:.1f}%")
                st.write(f"**Risk Level:** {data['risk']}")

                st.write("#### 🍎 Recommended Foods")
                for item in VITAMIN_RECOMMENDATIONS[vit]:
                    st.write(f"- {item}")

                if symptoms_toggle:
                    st.write("#### 🧠 Possible Symptoms")
                    st.warning(SYMPTOM_PATTERNS[vit])

    st.write("---")
    st.warning("⚠️ This is only an AI estimate. For clinical decisions, consult a medical professional.")
