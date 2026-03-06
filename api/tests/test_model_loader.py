import numpy as np
import pandas as pd
import pytest

import model_loader


class FakeModel:
    def predict(self, X):
        # retorna 1 para cada linha
        return [1 for _ in range(len(X))]

    def predict_proba(self, X):
        # probabilidade fixa
        return np.array([[0.2, 0.8] for _ in range(len(X))])


def _build_artifact():
    return {
        "model": FakeModel(),
        "feature_cols": ["Mat", "Por", "Pedra_0", "INDE"],
        "target": "Target",
        "target_rule": None,
        "const_cols_dropped": ["Const"],
        "id_cols": ["RA"],
        "leak_cols": ["Defasagem"],
    }


def test_prepare_features_drops_and_orders(monkeypatch):
    """Verifica drop de colunas irrelevantes e ordem correta das features."""
    monkeypatch.setattr(model_loader.joblib, "load", lambda _: _build_artifact())

    service = model_loader.ModelService("/tmp/fake.joblib")

    df = pd.DataFrame(
        [
            {
                "RA": "RA-1",
                "Mat": 7.5,
                "Por": 6.8,
                "Pedra_0": "ametista",
                "INDE": 7.12,
                "Target": 1,
                "Defasagem": -1,
                "Const": 1,
            }
        ]
    )

    X = service._prepare_features(df)

    assert list(X.columns) == ["Mat", "Por", "Pedra_0", "INDE"]
    assert len(X) == 1


def test_prepare_features_missing_cols_raises(monkeypatch):
    """Garante exceção quando faltam colunas obrigatórias de feature."""
    monkeypatch.setattr(model_loader.joblib, "load", lambda _: _build_artifact())

    service = model_loader.ModelService("/tmp/fake.joblib")

    df = pd.DataFrame([{"Mat": 7.5, "Por": 6.8, "INDE": 7.12}])

    with pytest.raises(ValueError) as exc:
        service._prepare_features(df)

    assert "Faltam colunas para predição" in str(exc.value)


def test_predict_returns_expected(monkeypatch):
    """Valida que predict retorna classe e probabilidade esperadas."""
    monkeypatch.setattr(model_loader.joblib, "load", lambda _: _build_artifact())

    service = model_loader.ModelService("/tmp/fake.joblib")

    df = pd.DataFrame(
        [
            {
                "Mat": 7.5,
                "Por": 6.8,
                "Pedra_0": "ametista",
                "INDE": 7.12,
            }
        ]
    )

    pred, prob = service.predict(df)

    assert pred == [1]
    assert prob == [0.8]
