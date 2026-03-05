from fastapi import FastAPI
from fastapi.responses import JSONResponse
from schema.DiabetesScreeningInput import DiabetesScreeningInput
from schema.prediction_response import DiabetesScreeningResponse
from Model.predict import predict_output, model, MODEL_VERSION, threshold


app = FastAPI()

    

# Human Readable
@app.get('/')
def home():
    return{'message':'Diabetes Screening API'}

# Machine readable
@app.get('/health')
def health_check():
    return{
        'status':'OK',
        'Version': MODEL_VERSION,
        'model_loaded': model is not None
    }


@app.post("/screen-diabetes", response_model= DiabetesScreeningResponse)
def Screen_Patient_for_Diabetes(data: DiabetesScreeningInput):
    try:
        user_input = {
            "age": data.age,
            "gender": data.gender,
            "smoking_history": data.smoking_history,
            "bmi": data.bmi,
            "hypertension": data.hypertension_bin,
            "heart_disease": data.heart_disease_bin
        }

        prob = predict_output(user_input)

        screening_result = "High Risk" if prob >= threshold else "Low Risk"

        return JSONResponse(
    status_code=200,
    content={
        "model_version": MODEL_VERSION,
        "diabetes_risk_probability": round(float(prob), 3),
        "screening_result": screening_result,
        "screening_threshold": round(float(threshold), 3)
    }
)

    except Exception as e:
        return JSONResponse(status_code=500,content={"error": str(e)})