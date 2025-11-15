import streamlit as st
from PIL import Image, ImageOps, ImageFilter
import time
import random

# --------------------------
# Page + session init
# --------------------------
st.set_page_config(page_title="Vitamin Deficiency Detector", layout="wide")

if "show_popup" not in st.session_state:
    st.session_state.show_popup = False
if "prediction" not in st.session_state:
    st.session_state.prediction = None
if "last_image_uploaded" not in st.session_state:
    st.session_state.last_image_uploaded = None

# --------------------------
# Sidebar
# --------------------------
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
uploaded_file = st.sidebar.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

# --------------------------
# Data dictionaries
# --------------------------
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

# --------------------------
# Helpers
# --------------------------
def calculate_risk(value):
    if value < 0.45:
        return "High Risk ❗"
    elif value < 0.70:
        return "Moderate Risk ⚠️"
    return "Low Risk ✅"

def dummy_predict():
    """Generate and return a deterministic-ish set of predictions.
       Stored in session_state so popup and main page use same values."""
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
            "risk": calculate_risk(score)
        }
    return result

def fake_heatmap(image: Image.Image) -> Image.Image:
    img = image.convert("RGB")
    heat = img.filter(ImageFilter.EMBOSS)
    heat = ImageOps.colorize(heat.convert("L"), black="blue", white="red")
    return heat

# --------------------------
# Process upload and prediction (persist to session_state)
# --------------------------
if uploaded_file is not None:
    try:
        img = Image.open(uploaded_file).convert("RGB")
        st.session_state.last_image_uploaded = uploaded_file.name
        # run dummy predict and save
        with st.spinner("Analyzing image and generating report..."):
            time.sleep(1.0)
            st.session_state.prediction = dummy_predict()
    except Exception as e:
        st.error(f"Could not read the uploaded image: {e}")
        st.session_state.prediction = None

# --------------------------
# Render main UI
# --------------------------
st.title("🧬 Vitamin Deficiency Detector")

if st.session_state.last_image_uploaded:
    st.caption(f"Last uploaded file: {st.session_state.last_image_uploaded}")

# Show image + heatmap if available
if uploaded_file is not None:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📸 Uploaded Image")
        st.image(img, use_column_width=True)
    with col2:
        st.subheader("🔥 Feature Heatmap")
        st.image(fake_heatmap(img), use_column_width=True)

st.write("---")

# If prediction exists, show report; otherwise prompt to upload
if st.session_state.prediction is None:
    st.info("Upload an image (left sidebar) to generate the vitamin report.")
else:
    prediction = st.session_state.prediction  # alias

    st.subheader("🧪 Vitamin Analysis Report")

    if analysis_type == "Single Vitamin Analysis" and selected_vitamin is not None:
        vit = selected_vitamin
        data = prediction.get(vit)
        if data:
            st.metric(label=f"{vit} Level ({data['status']})", value=data["percentage"])
            st.info(f"📊 Risk: {data['risk']}")
            st.write("### Symptoms")
            st.write(f"- {SYMPTOMS[vit]}")
            st.write("### Foods to Improve")
            for x in VITAMIN_RECOMMENDATIONS[vit]:
                st.write("✔ " + x)
            st.write("### Foods to Avoid")
            for x in FOODS_TO_AVOID[vit]:
                st.write("❌ " + x)
        else:
            st.error("Prediction for selected vitamin not found.")
    else:
        # Full report
        for vit, data in prediction.items():
            st.write(f"## 🟦 {vit}")
            st.progress(data["confidence"])
            st.write(f"**Status:** {data['status']}")
            st.write(f"**Level:** {data['percentage']}")
            st.write(f"**Risk:** {data['risk']}")
            st.write("### Symptoms")
            st.write(f"- {SYMPTOMS[vit]}")
            st.write("### Foods to Improve")
            for x in VITAMIN_RECOMMENDATIONS[vit]:
                st.write("✔ " + x)
            st.write("### Foods to Avoid")
            for x in FOODS_TO_AVOID[vit]:
                st.write("❌ " + x)
            st.write("---")

    # Open popup button — sets state (no rerun)
    if st.button("🧬 Open Advanced Dashboard"):
        st.session_state.show_popup = True

    st.warning("⚠️ This is an AI estimation. Consult a doctor for professional advice.")

# --------------------------
# Popup modal that re-uses session_state.prediction
# --------------------------
if st.session_state.show_popup:
    # safety: ensure prediction exists
    if st.session_state.prediction is None:
        st.error("No report available to show in popup. Upload an image first.")
        if st.button("Close"):
            st.session_state.show_popup = False
    else:
        st.markdown("""
            <style>
                .overlay {
                    position: fixed;
                    top: 0; left: 0;
                    width: 100%; height: 100%;
                    background: rgba(0,0,0,0.55);
                    z-index: 9999;
                }
                .popup-card {
                    position: fixed;
                    top: 50%; left: 50%;
                    transform: translate(-50%, -50%);
                    background: white;
                    padding: 20px;
                    width: 75%;
                    height: 75%;
                    overflow: auto;
                    border-radius: 12px;
                    z-index: 10000;
                    box-shadow: 0 8px 24px rgba(0,0,0,0.3);
                }
            </style>
        """, unsafe_allow_html=True)

        st.markdown('<div class="overlay"></div>', unsafe_allow_html=True)
        st.markdown('<div class="popup-card">', unsafe_allow_html=True)

        st.markdown("## 🧬 Advanced Vitamin Dashboard (Pop-Up)")
        st.write("This is the same detailed report shown in the main page:")

        for vit, data in st.session_state.prediction.items():
            st.write(f"### 🟦 {vit}")
            st.progress(data["confidence"])
            st.write(f"**Status:** {data['status']}")
            st.write(f"**Level:** {data['percentage']}")
            st.write(f"**Risk:** {data['risk']}")
            st.write("**Symptoms:**")
            st.write(f"- {SYMPTOMS[vit]}")
            st.write("**Foods to Improve:**")
            for x in VITAMIN_RECOMMENDATIONS[vit]:
                st.write("✔ " + x)
            st.write("**Foods to Avoid:**")
            for x in FOODS_TO_AVOID[vit]:
                st.write("❌ " + x)
            st.write("---")

        if st.button("❌ Close"):
            st.session_state.show_popup = False

        st.markdown("</div>", unsafe_allow_html=True)
