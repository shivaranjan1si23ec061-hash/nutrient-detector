import streamlit as st
from utils.face_extractor import extract_regions
from utils.preprocess import enhance_image
from utils.grad_cam import generate_gradcam
import tensorflow as tf
import numpy as np
import json
from PIL import Image

# Load model
model = tf.keras.models.load_model("model/vitamin_model.h5")

# Load labels
with open("model/label_map.json","r") as f:
    label_map = json.load(f)

st.title("AI-Based Vitamin Deficiency Detector")

uploaded = st.file_uploader("Upload Face Image", type=["jpg","png","jpeg"])

if uploaded:
    img = Image.open(uploaded)
    st.image(img, caption="Uploaded Image")

    # Extract face regions
    regions = extract_regions(np.array(img))

    # Preprocess
    processed = enhance_image(regions["full_face"])
    processed = np.expand_dims(processed, axis=0)

    # Prediction
    pred = model.predict(processed)[0]

    # Display output
    results = {label_map[str(i)]: float(pred[i]) for i in range(len(pred))}
    st.json(results)

    # Grad-CAM
    heatmap = generate_gradcam(model, processed, layer_name="top_conv")
    st.image(heatmap, caption="Model Focus Heatmap")
