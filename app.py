import streamlit as st
import numpy as np
from PIL import Image, ImageOps, ImageFilter
import time
import random

# ---------------------- PAGE CONFIG -----------------------
st.set_page_config(
    page_title="AI Vitamin Deficiency Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------- CUSTOM CSS -------------------------
st.markdown("""
<style>

body {
    background-color: #0f0f0f;
}

/* HEADER */
.header {
    background: linear-gradient(120deg, #4c00ff, #0099ff);
    padding: 35px;
    border-radius: 14px;
    color: white;
    text-align: center;
    margin-bottom: 25px;
    box-shadow: 0 0 25px rgba(0,0,0,0.4);
}

/* DASHBOARD CARDS */
.metric-card {
    padding: 25px;
    border-radius: 16px;
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(12px);
    color: white;
    box-shadow: 0 0 25px rgba(0,0,0,0.3);
    text-align: center;
    transition: 0.3s ease;
}
.metric-card:hover {
    transform: scale(1.04);
    box-shadow: 0 0 40px rgba(0,0,0,0.5);
}

/* RECOMMENDATION CHIPS */
.chip {
    display: inline-block;
    padding: 10px 16px;
    margin: 6px;
    border-radius: 20px;
    background: #1e1e1e;
    color: #f5f5f5;
    font-size: 14px;
    border: 1px solid #444;
}

/* IMAGE BOX */
.image-box {
    padding: 15px;
    background: rgba(255,255,255,0.06);
    border-radius: 15px;
    box-shadow: 0 0 20px rgba(0,0,0,0.4);
}

</style>
""", unsafe_allow_html=True)

# ---------------------- HEADER -------------------------
st.markdown("""
<div class="header">
    <h1>🧬 AI Vitamin Deficiency Analysis Dashboard</h1>
    <h3>Smart Health Monitoring • Nutrition Insights • Recovery Guide</h3>
</div>
""", unsafe_allow_html=True)

# ---------------------- SIDEBAR -------------------------
st.sidebar.title("🌐 Dashboard Controls")
analysis_type = st.sidebar.selectbox(
    "Analysis Type",
    ["Full Vitamin Report", "Single Vitamin Analysis"]
)

if analysis_type == "Single Vitamin Analysis":
    selected_vitamin = st.sidebar.selectbox(
        "Select Vitamin",
        ["Vitamin A", "Vitamin B12", "Vitamin C", "Vitamin D", "Iron", "Calcium"]
    )

st.sidebar.write("---")
uploaded_file = st.sidebar.file_uploader("📸 Upload Image", type=["jpg", "jpeg", "png"])

# ---------------------- DATA -------------------------
VITAMIN_RECOMMENDATIONS = {
    "Vitamin A": ["Carrots", "Spinach", "Egg yolks", "Pumpkin", "Vitamin A Capsules"],
    "Vitamin B12": ["Milk", "Eggs", "Fish", "Chicken", "B12 Tablets"],
    "Vitamin C": ["Oranges", "Lemons", "Strawberries", "Vitamin C Tablets"],
    "Vitamin D": ["Sunlight", "Mushrooms", "Milk", "Vitamin D3"],
    "Iron": ["Spinach", "Beetroot", "Dates", "Iron Syrup/Tablets"],
    "Calcium": ["Milk", "Curd", "Paneer", "Almonds", "Calcium Tablets"]
}

def dummy_predict():
    result = {}
    for vit in VITAMIN_RECOMMENDATIONS.keys():
        score = random.uniform(0.2, 0.95)
        status = ("❌ Deficient" if score < 0.45 
                  else "⚠️ Borderline" if score < 0.7 
                  else "✅ Normal")
        result[vit] = {"score": round(score, 2), "status": status}
    return result

def fake_heatmap(img):
    heat = img.filter(ImageFilter.EMBOSS)
    return ImageOps.colorize(heat.convert("L"), black="blue", white="red")

# ---------------------- MAIN DASHBOARD -------------------------
if uploaded_file:
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("📷 Uploaded Image")
        img = Image.open(uploaded_file)
        st.markdown('<div class="image-box">', unsafe_allow_html=True)
        st.image(img, use_column_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.subheader("🔥 Heatmap (AI Feature Highlight)")
        heatmap = fake_heatmap(img)
        st.markdown('<div class="image-box">', unsafe_allow_html=True)
        st.image(heatmap, use_column_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.write("---")
    st.subheader("🧪 Analysis Results")

    with st.spinner("AI analyzing the facial nutritional markers..."):
        time.sleep(1.5)
        results = dummy_predict()

    # ---------------- SINGLE VITAMIN PANEL ----------------
    if analysis_type == "Single Vitamin Analysis":
        vit = selected_vitamin
        data = results[vit]

        card = f"""
        <div class="metric-card">
            <h2>{vit}</h2>
            <h1>{data['score']*100:.1f}%</h1>
            <p>{data['status']}</p>
        </div>
        """
        st.markdown(card, unsafe_allow_html=True)

        st.subheader("🍎 Recovery Recommendations")
        for food in VITAMIN_RECOMMENDATIONS[vit]:
            st.markdown(f"<span class='chip'>{food}</span>", unsafe_allow_html=True)

    # ---------------- FULL DASHBOARD PANEL ----------------
    else:
        colA, colB, colC = st.columns(3)
        vitamins = list(results.keys())
        cols = [colA, colB, colC]

        # Cards for all vitamins
        for i, vit in enumerate(vitamins):
            with cols[i % 3]:
                data = results[vit]
                card = f"""
                <div class="metric-card">
                    <h3>{vit}</h3>
                    <h2>{data['score']*100:.1f}%</h2>
                    <p>{data['status']}</p>
                </div>
                """
                st.markdown(card, unsafe_allow_html=True)

        st.write("---")
        st.subheader("🥗 Recommended Foods & Supplements")

        for vit, data in results.items():
            if data["status"] != "✅ Normal":
                st.markdown(f"### {vit} – {data['status']}")
                for item in VITAMIN_RECOMMENDATIONS[vit]:
                    st.markdown(f"<span class='chip'>{item}</span>", unsafe_allow_html=True)
                st.write("")

# ---------------------- FOOTER -------------------------
st.write("---")
st.caption("⚠️ This dashboard provides AI-simulated estimates. Not for medical use.")
