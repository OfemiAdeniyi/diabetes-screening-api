import joblib
import pickle
import pandas as pd

# Load model with joblib
model = joblib.load("Model/rf_screening_model.pkl")

# Load threshold with pickle
with open("Model/screening_threshold.pkl", "rb") as f:
    threshold = pickle.load(f)

MODEL_VERSION = "1.0.0"

def predict_output(DiabetesScreeningInput: dict):
    input_df = pd.DataFrame([DiabetesScreeningInput])
    prob = model.predict_proba(input_df)[:, 1][0]
    return prob