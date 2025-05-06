import streamlit as st
import joblib
import numpy as np
import os

# Set page config
st.set_page_config(page_title="Water Potability Predictor", layout="centered")

# Title and description
st.title("💧 Water Potability Prediction App")
st.markdown("This app uses a trained machine learning model to predict whether water is safe to drink (potable) based on various chemical properties.")

# Load model and scaler
model_path = os.path.join("models", "svc.save")
scaler_path = os.path.join("models", "scaler.save")

try:
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
except Exception as e:
    st.error(f"Error loading model files: {e}")
    st.stop()

# Input fields
st.header("🔬 Enter Water Quality Parameters")

ph = st.number_input("pH value", min_value=0.0, max_value=14.0, value=7.0)
hardness = st.number_input("Hardness (mg/L)", min_value=0.0, value=100.0)
solids = st.number_input("Solids (ppm)", min_value=0.0, value=10000.0)
chloramines = st.number_input("Chloramines (ppm)", min_value=0.0, value=5.0)
sulfate = st.number_input("Sulfate (mg/L)", min_value=0.0, value=250.0)
conductivity = st.number_input("Conductivity (μS/cm)", min_value=0.0, value=400.0)
organic_carbon = st.number_input("Organic Carbon (ppm)", min_value=0.0, value=10.0)
trihalomethanes = st.number_input("Trihalomethanes (μg/L)", min_value=0.0, value=60.0)
turbidity = st.number_input("Turbidity (NTU)", min_value=0.0, value=4.0)

if st.button("Predict Potability"):
    input_features = [ph, hardness, solids, chloramines, sulfate,
                      conductivity, organic_carbon, trihalomethanes, turbidity]

    if all(val == 0 for val in input_features):
        st.warning("⚠️ Please enter valid (non-zero) values.")
    else:
        input_scaled = scaler.transform([input_features])
        prediction = model.predict(input_scaled)

        if prediction[0] == 1:
            st.success("✅ The water is POTABLE (safe to drink).")
        else:
            st.error("❌ The water is NOT POTABLE (unsafe to drink).")
