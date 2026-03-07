import streamlit as st
import requests

# -------------------------------
# Replace with your EC2 public IP
# -------------------------------
API_BASE_URL = "http://35.179.154.100:8000"

# -------------------------------
# Page Setup
# -------------------------------
st.set_page_config(page_title="Diabetes Risk Screening", layout="centered")

st.markdown("## 🩺 Diabetes Risk Screening Tool")
st.markdown(
    """
**Purpose:** Early identification of individuals who may be at risk of diabetes.  
This tool is designed for **community health centers and medical outreaches**.

⚠️ *This is a screening tool, not a diagnostic test.*
"""
)

st.divider()

# -------------------------------
# Initialize session state
# -------------------------------
defaults = {
    "age": 0,
    "gender": "Male",
    "height": 0.0,
    "weight": 0.0,
    "smoking_history": "never",
    "hypertension": "No",
    "heart_disease": "No",
    "screening_result": None
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# -------------------------------
# Reset Form Button
# -------------------------------
if st.button("🔄 Reset Form"):
    for key in defaults:
        st.session_state[key] = defaults[key]
    st.rerun()

# -------------------------------
# Input Form
# -------------------------------
age = st.number_input("Age (years)", min_value=0, max_value=120, value=st.session_state.age, key="age")
gender = st.selectbox(
    "Gender", ["Male", "Female", "Other"],
    index=["Male", "Female", "Other"].index(st.session_state.gender),
    key="gender"
)
height = st.number_input("Height (meters)", min_value=0.0, max_value=3.0, step=0.01, value=st.session_state.height, key="height")
weight = st.number_input("Weight (kg)", min_value=0.0, max_value=300.0, step=0.5, value=st.session_state.weight, key="weight")
smoking_history = st.selectbox(
    "Smoking History", ["never","former","current","ever","not current"],
    index=["never","former","current","ever","not current"].index(st.session_state.smoking_history),
    key="smoking_history"
)
hypertension = st.radio("Hypertension?", ["No","Yes"], index=["No","Yes"].index(st.session_state.hypertension), key="hypertension")
heart_disease = st.radio("Heart Disease?", ["No","Yes"], index=["No","Yes"].index(st.session_state.heart_disease), key="heart_disease")

# -------------------------------
# BMI Calculation
# -------------------------------
bmi = round(weight / (height ** 2), 2) if height > 0 else 0
st.info(f"📊 Calculated BMI: **{bmi} kg/m²**")
st.divider()

# -------------------------------
# Screening Button
# -------------------------------
if st.button("🔍 Screen for Diabetes Risk"):

    if age == 0 or height == 0 or weight == 0:
        st.warning("⚠️ Please fill Age, Height and Weight before screening.")

    else:
        payload = {
            "age": age,
            "gender": gender,
            "height": height,
            "weight": weight,
            "smoking_history": smoking_history,
            "hypertension": hypertension,
            "heart_disease": heart_disease
        }

        try:
            # POST to the EC2-hosted FastAPI endpoint
            response = requests.post(f"{API_BASE_URL}/screen-diabetes", json=payload, timeout=10)

            if response.status_code == 200:
                result = response.json()
                risk_percent = result["diabetes_risk_probability"] * 100

                st.subheader("📊 Screening Result")
                st.write(f"**Diabetes Risk Probability:** {risk_percent:.2f}%")
                st.write(f"**Screening Result:** {result['screening_result']}")
                st.write(f"**Threshold Used:** {result['screening_threshold']}")

                if risk_percent >= 50:
                    st.error("⚠️ High risk detected. Recommend further medical testing.")
                else:
                    st.success("✅ Low risk detected.")

            else:
                st.error(f"API Error: {response.status_code}")

        except requests.exceptions.ConnectionError:
            st.error("❌ Could not connect to the screening API server.")

        except requests.exceptions.Timeout:
            st.error("⏳ Request timed out. The server may be busy.")
