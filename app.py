import streamlit as st
from PIL import Image
import numpy as np
import time

# ------------------------------------------------------------
# BEAUTIFUL DASHBOARD THEME
# ------------------------------------------------------------
st.set_page_config(
    page_title="Vitamin Deficiency Detector",
    layout="wide",
    page_icon="🥗",
)

# Custom CSS for Styling
st.markdown("""
<style>
    .big-title {
        font-size: 42px;
        font-weight: 900;
        text-align: center;
    }
    .sub-title {
        font-size: 22px;
        text-align: center;
        margin-top: -10px;
    }
    .card {
        background: #ffffff;
        padding: 20px;
        border-radius: 18px;
        box-shadow: 0 4px 14px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .result-card {
        background: #e7f5ff;
        padding: 20px;
        border-radius: 18px;
        border-left: 6px solid #1c7ed6;
    }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# TITLE
# ------------------------------------------------------------
st.markdown("<div class='big-title'>🥗 Vitamin Deficiency Detector</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Upload an image and get health insights instantly</div>", unsafe_allow_html=True)
st.write("")

# ------------------------------------------------------------
# SIDEBAR
# ------------------------------------------------------------
st.sidebar.header("📥 Upload Image")
uploaded_file = st.sidebar.file_uploader("Choose an image", type=["jpg", "png", "jpeg"])

st.sidebar.write("---")
st.sidebar.header("ℹ About")
st.sidebar.info(
    "This tool analyzes face/skin patterns to estimate possible vitamin deficiencies "
    "and recommends foods/products to recover quickly."
)

# ------------------------------------------------------------
# Dummy Detection Function
# ------------------------------------------------------------
def predict_deficiency(img_array):
    """
    Fake ML Model Logic for Demo Purposes.
    Replace with your real trained model later.
    """
    labels = ["Vitamin D", "Vitamin B12", "Iron", "Calcium", "Vitamin C"]
    probs = np.random.rand(len(labels))
    probs = probs / probs.sum()
    deficiency = labels[np.argmax(probs)]
    return deficiency, probs


# ------------------------------------------------------------
# Foods & Products Recommendations
# ------------------------------------------------------------
recommendations = {
    "Vitamin D": [
        "🔸 Sunlight (15–20 mins)",
        "🔸 Salmon, tuna",
        "🔸 Vitamin D fortified milk",
        "🔸 Supplement: **D3 1000 IU**",
    ],
    "Vitamin B12": [
        "🔸 Eggs, dairy",
        "🔸 Fortified cereals",
        "🔸 Lean meat & fish",
        "🔸 Supplement: **Methylcobalamin**",
    ],
    "Iron": [
        "🔸 Spinach & leafy vegetables",
        "🔸 Beans & lentils",
        "🔸 Red meat",
        "🔸 Supplement: **Iron + Vitamin C**",
    ],
    "Calcium": [
        "🔸 Milk, curd, paneer",
        "🔸 Almonds, sesame seeds",
        "🔸 Ragi",
        "🔸 Supplement: **Calcium + D3**",
    ],
    "Vitamin C": [
        "🔸 Oranges, lemons",
        "🔸 Tomatoes",
        "🔸 Strawberries",
        "🔸 Supplement: **Ascorbic Acid**",
    ]
}

# ------------------------------------------------------------
# MAIN APP WORKFLOW
# ------------------------------------------------------------
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### 📤 Uploaded Image")

    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, width=350, caption="Uploaded Image")

with col2:
    st.markdown("### 🩺 Detection Results")
    if uploaded_file:

        # Convert image to array
        img_array = np.array(img)

        with st.spinner("Analyzing image... Please wait ⏳"):
            time.sleep(2)
            deficiency, probs = predict_deficiency(img_array)

        # Display Result
        st.markdown(f"""
        <div class='result-card'>
            <h2>🧬 Detected Deficiency: <b>{deficiency}</b></h2>
        </div>
        """, unsafe_allow_html=True)

        # Probabilities Chart
        st.markdown("#### 📊 Probability Distribution")
        st.bar_chart({ 
            "Vitamin": ["Vitamin D", "Vitamin B12", "Iron", "Calcium", "Vitamin C"],
            "Probability": probs
        })

        # Recommendations Section
        st.markdown("### 🥦 Recommended Foods & Recovery Items")
        st.markdown("<div class='card'>", unsafe_allow_html=True)

        for item in recommendations[deficiency]:
            st.write(item)

        st.markdown("</div>", unsafe_allow_html=True)

    else:
        st.info("⬅ Upload an image from the left sidebar to get results.")


# ------------------------------------------------------------
# FOOTER
# ------------------------------------------------------------
st.write("---")
st.markdown("<center>⚕ Made with ❤️ for Health Detection Demo</center>", unsafe_allow_html=True)
