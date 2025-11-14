# Nutrient Detector (Dummy-ready)

This package includes a Streamlit app and a script to generate a **dummy TensorFlow model** (`vitamin_model.h5`) that allows the app to run for UI/demo purposes.

## Files
- `app.py` - Streamlit application (loads `model/vitamin_model.h5`).
- `create_dummy_model.py` - Run this locally or in Colab to generate `model/vitamin_model.h5`.
- `requirements.txt` - Python dependencies for Streamlit Cloud or local setup.
- `model/` - folder where the generated model will be saved after running the script.

## Quick steps
1. On your PC or Google Colab, run:
   ```bash
   pip install -r requirements.txt
   python create_dummy_model.py
   ```
2. Confirm `model/vitamin_model.h5` exists.
3. Upload the entire repo to GitHub (including `model/vitamin_model.h5`).
4. Deploy to Streamlit Cloud.

## Notes
- The dummy model provides no medically valid predictions — it's for UI/testing only.
- For real predictions you must train on labeled data and replace `model/vitamin_model.h5` with a trained model.
