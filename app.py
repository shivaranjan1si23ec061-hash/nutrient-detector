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
        ["Vitamin A", "Vitamin B12", "Vitamin C", "Vitamin D", "Iron", "Calcium"]
    )

st.sidebar.write("---")
st.sidebar.caption("Upload an image to begin the analysis.")

# ---------------------------------------------------------
# Recommendations Database
# ---------------------------------------------------------
VITAMIN_RECOMMENDATIONS = {
    "Vitamin A": [
        "Carrots", "Sweet Potatoes", "Spinach",
        "Egg Yolks", "Pumpkin", "Vitamin A Capsules"
    ],
    "Vitamin B12": [
        "Milk & Dairy", "Chicken", "Fish (Tuna/Salmon)",
        "Eggs", "B12 Tablets"
    ],
    "Vitamin C": [
        "Oranges", "Lemons", "Strawberries",
        "Broccoli", "Vitamin C Chewables"
    ],
    "Vitamin D": [
        "Sunlight Exposure", "Fortified Milk",
        "Egg Yolks", "Mushrooms", "Vitamin D3 Supplements"
    ],
    "Iron": [
        "Spinach", "Red Meat", "Beetroot",
        "Dates", "Iron Syrup/Tablets"
    ],
    "Calcium": [
        "Milk", "Curd", "Paneer",
        "Almonds", "Calcium + Vitamin D Tablets"
    ]
}

# ---------------------------------------------------------
# Foods to Avoid
# ---------------------------------------------------------
FOODS_TO_AVOID = {
    "Vitamin A": ["Alcohol", "Processed Foods"],
    "Vitamin B12": ["Sugary Drinks", "Overcooked Food"],
    "Vitamin C": ["Junk Food", "Deep-Fried Items"],
    "Vitamin D": ["Too Much Caffeine", "Carbonated Drinks"],
    "Iron": ["Tea After Meals", "Coffee After Meals"],
    "Calcium": ["Soft Drinks", "High Salt Intake"]
}

# ---------------------------------------------------------
# Symptom Patterns
# ---------------------------------------------------------
SYMPTOMS = {
    "Vitamin A": "Dry skin, pale eyes, poor night vision",
    "Vitamin B12": "Fatigue, pale lips, weakness",
    "Vitamin C": "Low immunity, dry skin, bleeding gums",
    "Vitamin D": "Bone pain, fatigue, low mood",
    "Iron": "Pale skin, low energy, weakness",
    "Calcium": "Weak nails, muscle cramps"
}

# ---------------------------------------------------------
# Risk Level Logic
# ---------------------------------------------------------
def get_risk(score):
    if score < 0.45:
        return "High Risk ❗"
    elif score < 0.70:
        return "Moderate Risk ⚠️"
    return "Low Risk ✅"

# ---------------------------------------------------------
# Dummy predictor (fake model)
# ---------------------------------------------------------
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
            "risk": get_risk(score),
        }
    return result

# ---------------------------------------------------------
# Simple fake heatmap generator
# ---------------------------------------------------------
def fake_heatmap(image):
    img = image.convert("RGB")
    heat = img.filter(ImageFilter.EMBOSS)
    heat = ImageOps.colorize(heat.convert("L"), black="blue", white="red")
    return heat

# ---------------------------------------------------------
# Upload Section
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

    with st.spinner("Analyzing your image..."):
        time.sleep(2)
        prediction = dummy_predict()

    st.subheader("🧪 Vitamin Analysis Report")

    # ---------------------------------------------------------
    # SINGLE REPORT
    # ---------------------------------------------------------
    if analysis_type == "Single Vitamin Analysis":
        vit = selected_vitamin
        data = prediction[vit]

        st.metric(
            label=f"{vit} Level ({data['status']})",
            value=data["percentage"]
        )

        # Health Status
        if data["status"] == "❌ Deficient":
            st.error(f"⚠️ Severe {vit} deficiency detected.")
        elif data["status"] == "⚠️ Borderline":
            st.warning(f"⚠️ {vit} level is borderline.")
        else:
            st.success(f"✔ {vit} level is normal.")

        # Risk
        st.info(f"📊 **Risk Level:** {data['risk']}")

        # Symptoms
        st.write("### 🧠 Possible Symptoms")
        st.write(f"• {SYMPTOMS[vit]}")

        # Foods to Eat
        st.write(f"### 🍎 Foods to Improve {vit}")
        for item in VITAMIN_RECOMMENDATIONS[vit]:
            st.write(f"✔ {item}")

        # Foods to Avoid
        st.write(f"### 🚫 Foods to Avoid")
        for bad in FOODS_TO_AVOID[vit]:
            st.write(f"❌ {bad}")

    # ---------------------------------------------------------
    # FULL REPORT
    # ---------------------------------------------------------
    else:
        for vit, data in prediction.items():
            st.write(f"## 🟦 {vit}")
            st.progress(data["confidence"])

            st.write(f"**Status:** {data['status']}")  
            st.write(f"**Level:** {data['percentage']}")  
            st.write(f"**Risk Level:** {data['risk']}")

            # Symptoms
            st.write("### 🧠 Possible Symptoms")
            st.write(f"- {SYMPTOMS[vit]}")

            # Recommendations
            st.write("### 🍎 Recommended Foods")
            for food in VITAMIN_RECOMMENDATIONS[vit]:
                st.write(f"- {food}")

            # Foods to Avoid
            st.write("### 🚫 Foods to Avoid")
            for bad in FOODS_TO_AVOID[vit]:
                st.write(f"- {bad}")

            st.write("---")

    st.warning("⚠️ This is an AI estimation. Consult a doctor for medical advice.")
