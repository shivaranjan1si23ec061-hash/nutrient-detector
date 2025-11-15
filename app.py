import streamlit as st
import numpy as np
from PIL import Image, ImageOps, ImageFilter
import time
import random

# ------------------------------------------
# INITIAL POP-UP STATE
# ------------------------------------------
if "show_popup" not in st.session_state:
    st.session_state.show_popup = False

st.set_page_config(page_title="Vitamin Deficiency Detector", layout="wide")

# ------------------------------------------
# SIDEBAR
# ------------------------------------------
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

# ------------------------------------------
# RECOMMENDATIONS DATABASE
# ------------------------------------------
VITAMIN_RECOMMENDATIONS = {
    "Vitamin A": ["Carrots", "Sweet Potatoes", "Spinach", "Egg Yolks", "Pumpkin"],
    "Vitamin B12": ["Milk", "Chicken", "Fish", "Eggs", "B12 Tablets"],
    "Vitamin C": ["Oranges", "Lemon", "Strawberries", "Broccoli"],
    "Vitamin D": ["Sunlight", "Fortified Milk", "Egg Yolks", "Mushrooms"],
    "Iron": ["Spinach", "Red Meat", "Beetroot", "Dates"],
    "Calcium": ["Milk", "Curd", "Paneer", "Almonds"]
}

FOODS_TO_AVOID = {
    "Vitamin A": ["Alcohol", "Processed Foods"],
    "Vitamin B12": ["Sugary Drinks", "Overcooked Foods"],
    "Vitamin C": ["Junk Food", "Deep-Fried Items"],
    "Vitamin D": ["Too Much Caffeine", "Soft Drinks"],
    "Iron": ["Tea After Meals", "Coffee After Meals"],
    "Calcium": ["Soft Drinks", "High Salt Foods"]
}

SYMPTOMS = {
    "Vitamin A": "Dry skin, pale eyes, poor night vision",
    "Vitamin B12": "Weakness, pale lips, fatigue",
    "Vitamin C": "Bleeding gums, low immunity, dry skin",
    "Vitamin D": "Weak bones, low mood, tiredness",
    "Iron": "Low energy, pale skin, dizziness",
    "Calcium": "Weak nails, muscle cramps"
}

# ------------------------------------------
# RISK CALCULATION
# ------------------------------------------
def calculate_risk(value):
    if value < 0.45:
        return "High Risk ❗"
    elif value < 0.70:
        return "Moderate Risk ⚠️"
    return "Low Risk ✅"

# ------------------------------------------
# PREDICTION MODEL
# ------------------------------------------
def dummy_predict():
    vitamins = {
        "Vitamin A": random.uniform(0.2, 0.95),
        "Vitamin B12": random.uniform(0.2, 0.95),
        "Vitamin C": random.uniform(0.2, 0.95),
        "Vitamin D": random.uniform(0.2, 0.95),
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

        result[vit] = {
            "confidence": round(score, 2),
            "percentage": f"{score*100:.1f}%",
            "status": status,
            "risk": calculate_risk(score),
        }
    return result

# ------------------------------------------
# HEATMAP
# ------------------------------------------
def fake_heatmap(image):
    img = image.convert("RGB")
    heat = img.filter(ImageFilter.EMBOSS)
    heat = ImageOps.colorize(heat.convert("L"), black="blue", white="red")
    return heat

# ------------------------------------------
# UPLOAD SECTION
# ------------------------------------------
uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

if uploaded_file:

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📸 Uploaded Image")
        img = Image.open(uploaded_file)
        st.image(img)

    with col2:
        st.subheader("🔥 Feature Heatmap")
        st.image(fake_heatmap(img))

    st.write("---")

    # ------------------------------------------
    # PREDICTION PROCESS
    # ------------------------------------------
    with st.spinner("Analyzing your image..."):
        time.sleep(2)
        prediction = dummy_predict()

    st.subheader("🧪 Vitamin Analysis Report")

    # ------------------------------------------
    # SINGLE REPORT
    # ------------------------------------------
    if analysis_type == "Single Vitamin Analysis":

        vit = selected_vitamin
        data = prediction[vit]

        st.metric(f"{vit} Level ({data['status']})", data["percentage"])
        st.info(f"📊 Risk Level: **{data['risk']}**")

        st.write("### 🧠 Possible Symptoms")
        st.write(f"- {SYMPTOMS[vit]}")

        st.write(f"### 🍎 Foods to Improve {vit}")
        for item in VITAMIN_RECOMMENDATIONS[vit]:
            st.write("✔ " + item)

        st.write("### 🚫 Foods to Avoid")
        for item in FOODS_TO_AVOID[vit]:
            st.write("❌ " + item)

    # ------------------------------------------
    # FULL REPORT
    # ------------------------------------------
    else:
        for vit, data in prediction.items():
            st.write(f"## 🟦 {vit}")
            st.progress(data["confidence"])
            st.write(f"**Status:** {data['status']}")
            st.write(f"**Level:** {data['percentage']}")
            st.write(f"**Risk:** {data['risk']}")

            st.write("### 🧠 Symptoms")
            st.write(f"- {SYMPTOMS[vit]}")

            st.write("### 🍎 Foods to Improve")
            for food in VITAMIN_RECOMMENDATIONS[vit]:
                st.write("- " + food)

            st.write("### 🚫 Foods to Avoid")
            for avoid in FOODS_TO_AVOID[vit]:
                st.write("- " + avoid)

            st.write("---")

    # BUTTON TO OPEN POP-UP
    st.write("---")
    if st.button("🧬 Open Advanced Dashboard"):
        st.session_state.show_popup = True
        st.experimental_rerun()

    st.warning("⚠️ This is an AI estimation. Consult a doctor for professional advice.")

# ------------------------------------------
# POP-UP ADVANCED DASHBOARD
# ------------------------------------------
if st.session_state.show_popup:

    st.markdown("""
        <style>
            .overlay {
                position: fixed;
                top: 0; left: 0;
                width: 100%; height: 100%;
                background: rgba(0,0,0,0.6);
                z-index: 9999;
            }
            .popup {
                position: fixed;
                top: 50%; left: 50%;
                transform: translate(-50%, -50%);
                background: white;
                width: 70%;
                padding: 25px;
                border-radius: 15px;
                z-index: 10000;
                box-shadow: 0px 0px 25px rgba(0,0,0,0.4);
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="overlay"></div>', unsafe_allow_html=True)
    st.markdown('<div class="popup">', unsafe_allow_html=True)

    st.markdown("## 🧬 Advanced Analytics Dashboard")
    st.markdown("### 📊 Your Health Summary")

    colA, colB, colC = st.columns(3)
    colA.metric("Highest Deficiency", "Vitamin D")
    colB.metric("Well Balanced", "Vitamin C")
    colC.metric("Overall Health Score", "78 / 100")

    st.write("### 🌟 Recommendations Summary")
    st.success("""
    - Increase sunlight exposure  
    - Add spinach and beetroot weekly  
    - Reduce caffeine intake  
    - Maintain hydration  
    """)

    if st.button("❌ Close"):
        st.session_state.show_popup = False
        st.experimental_rerun()

    st.markdown("</div>", unsafe_allow_html=True)
