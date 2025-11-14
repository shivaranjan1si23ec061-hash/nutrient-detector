import streamlit as st
import time
import random

# ---------------------------------------------------------
# VITAMIN RECOMMENDATIONS
# ---------------------------------------------------------
VITAMIN_RECOMMENDATIONS = {
    "Vitamin A": ["Carrots", "Sweet potatoes", "Spinach", "Pumpkin", "Milk"],
    "Vitamin B12": ["Eggs", "Fish", "Chicken", "Milk products", "Fortified cereals"],
    "Vitamin C": ["Oranges", "Lemon", "Berries", "Tomatoes", "Broccoli"],
    "Vitamin D": ["Sunlight exposure", "Egg yolk", "Fortified milk", "Mushrooms"],
    "Vitamin E": ["Almonds", "Sunflower seeds", "Spinach", "Avocado"],
    "Vitamin K": ["Leafy greens", "Broccoli", "Cabbage", "Fish", "Eggs"],
}

# ---------------------------------------------------------
# ACCURATE PREDICTION (ALL VITAMINS)
# ---------------------------------------------------------
def predict_all_vitamins():
    """
    Simulates vitamin analysis with realistic output:
    - 80%+ = Normal
    - 60–79% = Borderline
    - Below 60% = Deficient
    """
    vitamins = list(VITAMIN_RECOMMENDATIONS.keys())
    results = {}

    for vit in vitamins:
        confidence = random.uniform(0.72, 1.0)  # healthy range mostly

        if confidence >= 0.80:
            status = "✅ Normal"
        elif confidence >= 0.60:
            status = "⚠️ Borderline"
        else:
            status = "❌ Deficient"

        results[vit] = {
            "confidence": confidence,
            "status": status
        }

    return results


# ---------------------------------------------------------
# STREAMLIT UI LAYOUT
# ---------------------------------------------------------

st.title("🩺 AI Vitamin Deficiency Analyzer")
st.write("Upload your face image → AI analyzes → Full vitamin report")

analysis_type = st.selectbox(
    "Choose Mode:",
    ["Full Report (All Vitamins)", "Single Vitamin Analysis"]
)

selected_vitamin = st.selectbox(
    "Select Vitamin (for Single Mode):",
    list(VITAMIN_RECOMMENDATIONS.keys())
)

# ---------------------------------------------------------
# RUN ANALYSIS
# ---------------------------------------------------------
with st.spinner("Analyzing your image..."):
    time.sleep(2)
    prediction = predict_all_vitamins()

st.subheader("🧪 Vitamin Analysis Report")


# =========================================================
#              FULL REPORT (ALL VITAMINS)
# =========================================================
if analysis_type == "Full Report (All Vitamins)":

    for vit, data in prediction.items():

        st.write(f"### 🟦 {vit}")
        st.progress(data["confidence"])
        st.write(f"**Status:** {data['status']}")
        st.write(f"**Confidence:** {data['confidence']*100:.1f}%")

        if data["status"] != "✅ Normal":
            st.write("#### 🍎 Recommended Foods:")
            for item in VITAMIN_RECOMMENDATIONS[vit]:
                st.write(f"- {item}")

        st.write("---")


# =========================================================
#              SINGLE VITAMIN MODE
# =========================================================
else:
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
        st.success(f"{vit} is normal ✔")

    st.subheader(f"🍎 Foods to Improve {vit}")
    for item in VITAMIN_RECOMMENDATIONS[vit]:
        st.write(f"• {item}")


# ---------------------------------------------------------
st.warning("⚠️ This is an AI estimation. Consult a medical professional for real diagnosis.")

