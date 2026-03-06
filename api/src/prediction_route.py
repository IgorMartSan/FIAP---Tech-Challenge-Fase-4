import logging
import os
import time
from pathlib import Path

import pandas as pd
from fastapi import APIRouter

from schemas import PredictionInput, PredictionOutput
from model_loader import ModelService

MODEL_FILENAME = os.getenv("MODEL_FILENAME", "model_defasagem_fc_binario_lgbm.joblib")
MODEL_PATH = Path(__file__).resolve().parent / "model" / MODEL_FILENAME

router = APIRouter(tags=["Prediction"])

model_service = ModelService(str(MODEL_PATH))
logger = logging.getLogger("prediction")


@router.post(
    "/predict",
    response_model=PredictionOutput,
    summary="Predizer risco de apoio pedagógico",
    description="""
                    Esta rota recebe os indicadores educacionais e históricos de um aluno e utiliza
                    um modelo de Machine Learning para estimar o risco de ele precisar de apoio pedagógico.

                    ### Como interpretar a saída
                    
                    - **risk_class = 1**: aluno com risco, provavelmente precisando de acompanhamento.
                    - **risk_class = 0**: aluno com baixo risco no cenário atual.
                    - **risk_probability**: probabilidade estimada de risco.
                    - **needs_help**: interpretação direta para uso operacional.
                    - **help_level**:
                    - **baixa**: probabilidade menor que 0.40
                    - **moderada**: probabilidade entre 0.40 e 0.69
                    - **alta**: probabilidade maior ou igual a 0.70

                    ### Observação

                    A API apoia a decisão pedagógica, mas não substitui a avaliação humana.
                """,
    response_description="Resultado da predição de risco e recomendação de necessidade de apoio.",
)
def predict(payload: PredictionInput):
    start = time.perf_counter()
    df = pd.DataFrame([payload.model_dump()])

    pred, prob = model_service.predict(df)
    latency_ms = (time.perf_counter() - start) * 1000.0

    logger.info(
        "prediction",
        extra={
            "event": "prediction",
            "model_version": os.getenv("MODEL_VERSION", "v1"),
            "latency_ms": round(latency_ms, 2),
            "risk_class": int(pred[0]),
            "risk_probability": float(prob[0]),
            "features": payload.model_dump(),
        },
    )

    return PredictionOutput(
        risk_class=int(pred[0]),
        risk_probability=float(prob[0]),
    )
