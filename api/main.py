from fastapi import FastAPI
from pydantic import BaseModel, Field


app = FastAPI(title="Predict API", version="1.0.0")


class PredictRequest(BaseModel):
    feature_1: float = Field(..., description="Primeira feature numérica")
    feature_2: float = Field(..., description="Segunda feature numérica")


class PredictResponse(BaseModel):
    prediction: float


@app.post("/predict", response_model=PredictResponse)
def predict(payload: PredictRequest) -> PredictResponse:
    # Placeholder: substitua pela chamada do seu modelo treinado.
    result = (payload.feature_1 + payload.feature_2) / 2
    return PredictResponse(prediction=result)
