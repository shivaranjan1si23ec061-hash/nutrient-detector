import streamlit as st
from PIL import Image
import numpy as np

st.title("Vitamin Deficiency Detector")

# Dummy predictor
def predict(image_array):
    return {
        "Vitamin A": "Normal",
        "Vitamin B12": "Low",
        "Vitamin D": "Normal"
    }

uploaded = st.file_uploader("Upload an image", type=["jpg", "png"])

if uploaded:
    img = Image.open(uploaded)
    st.image(img, caption="Uploaded Image")

    img_array = np.array(img)

    result = predict(img_array)

    st.subheader("Prediction Result")
    st.json(result)

