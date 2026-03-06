from pydantic import BaseModel, Field, ConfigDict


class PredictionInput(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "RA": "RA-999",
                "Mat": 7.5,
                "Por": 6.8,
                "Pedra_0": "ametista",
                "Pedra_1": "agata",
                "Pedra_2": "quartzo",
                "INDE": 7.12,
                "IAA": 8.10,
                "IEG": 7.40,
                "IPS": 6.90,
                "IDA": 7.20,
                "IPV": 8.05,
                "IAN": 5.00,
                "Defasagem": -1
            }
        }
    )

    RA: str | None = Field(default=None, description="Identificador do aluno.")
    Mat: float = Field(..., description="Nota de Matemática.")
    Por: float = Field(..., description="Nota de Português.")
    Pedra_0: str = Field(..., description="Pedra histórica 0.")
    Pedra_1: str = Field(..., description="Pedra histórica 1.")
    Pedra_2: str = Field(..., description="Pedra histórica 2.")
    INDE: float = Field(..., description="Índice de Desenvolvimento Educacional.")
    IAA: float = Field(..., description="Indicador de Autoavaliação.")
    IEG: float = Field(..., description="Indicador de Engajamento.")
    IPS: float = Field(..., description="Indicador Psicossocial.")
    IDA: float = Field(..., description="Indicador de Aprendizagem.")
    IPV: float = Field(..., description="Indicador de Ponto de Virada.")
    IAN: float = Field(..., description="Indicador de Adequação ao Nível.")
    Defasagem: float | None = Field(default=None, description="Defasagem histórica.")

class PredictionOutput(BaseModel):
    risk_class: int = Field(..., description="1 = ruim, 0 = bom.")
    risk_probability: float = Field(..., description="Probabilidade prevista da classe ruim.")