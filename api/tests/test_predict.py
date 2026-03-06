from fastapi.testclient import TestClient

import prediction_route
from main import app


class DummyModelService:
    def predict(self, df):
        # retorna class=1 e prob=0.77 para qualquer entrada
        return [1], [0.77]


def test_predict_ok(monkeypatch):
    """Garante sucesso na rota /predict com modelo mockado e saída determinística."""
    monkeypatch.setattr(prediction_route, "model_service", DummyModelService())

    client = TestClient(app)

    payload = {
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
        "Defasagem": -1,
    }

    resp = client.post("/predict", json=payload)
    assert resp.status_code == 200

    body = resp.json()
    assert body["risk_class"] == 1
    assert abs(body["risk_probability"] - 0.77) < 1e-9


def test_predict_validation_error():
    """Garante erro 422 quando campos obrigatórios não são enviados."""
    client = TestClient(app)

    payload = {
        # "Mat" faltando de propósito
        "RA": "RA-999",
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
        "Defasagem": -1,
    }

    resp = client.post("/predict", json=payload)
    assert resp.status_code == 422
