import streamlit as st
from PIL import Image, ImageOps, ImageFilter
import time
import random

st.set_page_config(page_title="Vitamin Deficiency Detector", layout="wide")

# ------------------------------------------
# Session State
# ------------------------------------------
if "show_dashboard" not in st.session_state:
    st.session_state.show_dashboard = False
if "prediction" not in st.session_state:
    st.session_state.prediction = None
if "uploaded_img" not in st.session_state:
    st.session_state.uploaded_img = None

# ------------------------------------------
# Sidebar
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

uploaded_file = st.sidebar.file_uploader("Upload Image", type=["jpg","jpeg","png"])
st.sidebar.write("---")

# ------------------------------------------
# Database
# ------------------------------------------
RECOMMEND = {
    "Vitamin A": ["Carrots","Spinach","Sweet Potatoes","Egg Yolks"],
    "Vitamin B12": ["Eggs","Milk","Chicken","Fish"],
    "Vitamin C": ["Oranges","Lemon","Strawberries","Broccoli"],
    "Vitamin D": ["Sunlight","Fortified Milk","Mushrooms"],
    "Iron": ["Spinach","Beetroot","Dates","Red Meat"],
    "Calcium": ["Milk","Curd","Almonds","Paneer"]
}

AVOID = {
    "Vitamin A": ["Alcohol","Processed Foods"],
    "Vitamin B12": ["Sugary Drinks"],
    "Vitamin C": ["Junk Food"],
    "Vitamin D": ["Soft Drinks"],
    "Iron": ["Tea After Meals"],
    "Calcium": ["High Salt Foods"]
}

SYMPTOMS = {
    "Vitamin A": "Dry skin, night blindness",
    "Vitamin B12": "Fatigue, pale lips",
    "Vitamin C": "Weak immunity, dry skin",
    "Vitamin D": "Bone pain, weakness",
    "Iron": "Pale skin, dizziness",
    "Calcium": "Weak nails, cramps"
}

# ------------------------------------------
# Helpers
# ------------------------------------------
def risk(score):
    if score < 0.45: return "High Risk ❗"
    if score < 0.70: return "Borderline ⚠️"
    return "Normal ✅"

def fake_predict():
    output = {}
    for v in RECOMMEND:
        s = random.uniform(0.2, 0.95)
        output[v] = {
            "score": round(s,2),
            "percent": f"{s*100:.1f}%",
            "status": "❌ Deficient" if s<0.45 else ("⚠️ Borderline" if s<0.70 else "✅ Normal"),
            "risk": risk(s)
        }
    return output

def fake_heatmap(img):
    img = img.convert("RGB")
    heat = img.filter(ImageFilter.EMBOSS)
    return ImageOps.colorize(heat.convert("L"), black="blue", white="red")

# ------------------------------------------
# Upload Image
# ------------------------------------------
if uploaded_file:
    st.session_state.uploaded_img = Image.open(uploaded_file)
    st.session_state.prediction = None  # reset

# ------------------------------------------
# MAIN VIEW
# ------------------------------------------
st.title("🧬 Vitamin Deficiency Detector")

if st.session_state.uploaded_img:
    col1,col2 = st.columns(2)
    with col1:
        st.subheader("Uploaded Image")
        st.image(st.session_state.uploaded_img)

    with col2:
        st.subheader("Feature Heatmap")
        st.image(fake_heatmap(st.session_state.uploaded_img))

    if st.button("Analyze Image"):
        with st.spinner("Analyzing..."):
            time.sleep(1)
            st.session_state.prediction = fake_predict()

st.write("---")

# ------------------------------------------
# Show Report
# ------------------------------------------
if st.session_state.prediction:

    pred = st.session_state.prediction

    if analysis_type == "Single Vitamin Analysis":
        vit = selected_vitamin
        data = pred[vit]

        st.subheader(f"{vit} Report")
        st.metric(f"{vit} Level ({data['status']})", data["percent"])
        st.info(f"Risk: {data['risk']}")

        st.write("### Symptoms")
        st.write(f"- {SYMPTOMS[vit]}")

        st.write("### Foods to Improve")
        for x in RECOMMEND[vit]: st.write("✔ "+x)

        st.write("### Foods to Avoid")
        for x in AVOID[vit]: st.write("❌ "+x)

    else:
        st.subheader("Full Vitamin Report")
        for vit,data in pred.items():
            st.write(f"## {vit}")
            st.progress(data["score"])
            st.write(f"**Level:** {data['percent']}")
            st.write(f"**Status:** {data['status']}")
            st.write(f"**Risk:** {data['risk']}")
            st.write("Symptoms: "+SYMPTOMS[vit])
            st.write("Foods to Improve:")
            for x in RECOMMEND[vit]: st.write("- "+x)
            st.write("Foods to Avoid:")
            for x in AVOID[vit]: st.write("- "+x)
            st.write("---")

    # --------------------------------------
    # DASHBOARD BUTTON (fully working)
    # --------------------------------------
    if st.button("📊 Open Advanced Dashboard"):
        st.session_state.show_dashboard = True


# ------------------------------------------
# ADVANCED DASHBOARD (WORKING GUARANTEED)
# ------------------------------------------
if st.session_state.show_dashboard and st.session_state.prediction:

    with st.expander("📊 ADVANCED DASHBOARD (Click to Collapse)", expanded=True):

        st.write("### 🧬 Cross-Vitamin Comparison Dashboard")

        pred = st.session_state.prediction

        for vit,data in pred.items():
            st.write(f"## {vit}")
            st.progress(data["score"])
            st.write(f"**Level:** {data['percent']}")
            st.write(f"**Risk:** {data['risk']}")
            st.write(f"Symptoms: {SYMPTOMS[vit]}")
            st.write("Foods to Improve:")
            for x in RECOMMEND[vit]: st.write("✔ "+x)
            st.write("Foods to Avoid:")
            for x in AVOID[vit]: st.write("❌ "+x)
            st.write("---")

        if st.button("Close Dashboard"):
            st.session_state.show_dashboard = False
