from pydantic import BaseModel, Field
from typing import Literal

class DiabetesScreeningResponse(BaseModel):
    model_version: str = Field(..., description="Version of the ML model used")
    diabetes_risk_probability: float = Field(
        ..., ge=0.0, le=1.0, description="Predicted probability of diabetes (0 to 1)"
    )
    screening_result: Literal["High Risk", "Low Risk"] = Field(
        ..., description="Screening outcome based on threshold"
    )
    screening_threshold: float = Field(
        ..., ge=0.0, le=1.0, description="Probability threshold used for screening"
    )
