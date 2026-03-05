from pydantic import BaseModel, Field, computed_field
from typing import Literal, Annotated

# pydantic model to validate incoming data
class DiabetesScreeningInput(BaseModel):
    age: Annotated[float, Field(..., gt=0, lt=120, description="Age of the patient in years", examples=[45])]
    gender: Annotated[Literal["Male", "Female", "Other"], Field(..., description="Biological sex of the patient")]
    height: Annotated[float, Field(..., gt=0.5, lt=2.5, description="Height in meters", examples=[1.72])]
    weight: Annotated[float, Field(..., gt=20, lt=300, description="Weight in kilograms", examples=[75])]
    smoking_history: Annotated[Literal["never", "former", "current", "ever", "not current"], Field(..., description="Smoking history of the patient")]
    hypertension: Annotated[Literal["Yes", "No"], Field(..., description="Does the patient have hypertension?")]
    heart_disease: Annotated[Literal["Yes", "No"], Field(..., description="Does the patient have heart disease?")]


    # Computed BMI
    
    @computed_field
    @property
    def bmi(self) -> float:
        """
        Body Mass Index calculated as weight / height^2
        """
        return round(self.weight / (self.height ** 2), 2)
    
    
    @computed_field
    @property
    def hypertension_bin(self) -> int:
        return 1 if self.hypertension == "Yes" else 0

    @computed_field
    @property
    def heart_disease_bin(self) -> int:
        return 1 if self.heart_disease == "Yes" else 0