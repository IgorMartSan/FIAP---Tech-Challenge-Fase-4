import pandas as pd
import numpy as np
import pytest

from ca_train.train_model import BinaryDefasagemTrainer, BinaryTrainingConfig


class FakeModel:
    def __init__(self):
        self.feature_importances_ = []

    def fit(self, X, y, eval_set=None, eval_metric=None):
        self.feature_importances_ = [1 for _ in range(X.shape[1])]
        return self

    def predict(self, X):
        return np.zeros(len(X), dtype=int)


class FakePredictModel:
    def __init__(self):
        self.seen_columns = None

    def predict(self, X):
        self.seen_columns = list(X.columns)
        return np.zeros(len(X), dtype=int)


def _make_dataset():
    return pd.DataFrame(
        {
            "RA": ["RA-1", "RA-2", "RA-3", "RA-4"],
            "Mat": [7.5, 8.0, 6.0, 5.5],
            "Por": [6.8, 7.1, 5.5, 5.0],
            "Pedra": ["a", "b", "a", "c"],
            "Defasagem FC": [-1, 1, -1, 1],
        }
    )


def test_validate_sizes_raises():
    """Objetivo: garantir validação das proporções de split.

    Exemplo de uso: train=0.6, val=0.2, test=0.3 deve falhar.
    """
    cfg = BinaryTrainingConfig(train_size=0.6, val_size=0.2, test_size=0.3)
    trainer = BinaryDefasagemTrainer(_make_dataset(), "Defasagem FC", cfg)

    with pytest.raises(ValueError):
        trainer._validate_sizes()


def test_build_binary_target_rules():
    """Objetivo: converter target conforme as regras suportadas.

    Exemplo de uso: `negative_is_1` transforma -1 em 1 e 0/1 em 0/1.
    """
    cfg = BinaryTrainingConfig()
    trainer = BinaryDefasagemTrainer(_make_dataset(), "Defasagem FC", cfg)

    y_raw = pd.Series([-1, 0, 1])

    trainer.config.target_rule = "negative_is_1"
    assert trainer._build_binary_target(y_raw).tolist() == [1, 0, 0]

    trainer.config.target_rule = "positive_is_1"
    assert trainer._build_binary_target(y_raw).tolist() == [0, 0, 1]

    trainer.config.target_rule = "non_negative_is_1"
    assert trainer._build_binary_target(y_raw).tolist() == [0, 1, 1]

    trainer.config.target_rule = "invalid"
    with pytest.raises(ValueError):
        trainer._build_binary_target(y_raw)


def test_train_with_fake_model(monkeypatch):
    """Objetivo: treinar com modelo fake e validar estrutura do retorno.

    Exemplo de uso: mock de `_build_model` evita treino real do LightGBM.
    """
    cfg = BinaryTrainingConfig(train_size=0.5, val_size=0.25, test_size=0.25)
    trainer = BinaryDefasagemTrainer(_make_dataset(), "Defasagem FC", cfg)

    monkeypatch.setattr(trainer, "_build_model", lambda: FakeModel())

    result = trainer.train()

    assert "metrics" in result
    assert "feature_importance" in result
    assert "shapes" in result
    assert len(result["feature_cols"]) > 0


def test_predict_requires_trained_model():
    """Objetivo: impedir predição antes do treino.

    Exemplo de uso: chamar `predict` sem `train` deve lançar RuntimeError.
    """
    cfg = BinaryTrainingConfig()
    trainer = BinaryDefasagemTrainer(_make_dataset(), "Defasagem FC", cfg)

    with pytest.raises(RuntimeError):
        trainer.predict(_make_dataset())


def test_save_requires_trained_model():
    """Objetivo: impedir salvar antes do treino."""
    cfg = BinaryTrainingConfig()
    trainer = BinaryDefasagemTrainer(_make_dataset(), "Defasagem FC", cfg)

    with pytest.raises(RuntimeError):
        trainer.save("/tmp/fake.joblib")


def test_train_saves_artifact(monkeypatch):
    """Objetivo: salvar artefato com metadados após treino."""
    cfg = BinaryTrainingConfig(train_size=0.5, val_size=0.25, test_size=0.25, output_model_path="/tmp/fake.joblib")
    trainer = BinaryDefasagemTrainer(_make_dataset(), "Defasagem FC", cfg)

    monkeypatch.setattr(trainer, "_build_model", lambda: FakeModel())

    captured = {}

    def _fake_dump(obj, path):
        captured["artifact"] = obj
        captured["path"] = path

    monkeypatch.setattr("ca_train.train_model.joblib.dump", _fake_dump)

    trainer.train()

    assert captured["path"] == "/tmp/fake.joblib"
    assert captured["artifact"]["target"] == "Defasagem FC"
    assert captured["artifact"]["target_rule"] == "negative_is_1"
    assert "feature_cols" in captured["artifact"]


def test_predict_drops_id_leak_target_and_const_cols():
    """Objetivo: garantir que predict usa apenas feature_cols_."""
    cfg = BinaryTrainingConfig()
    trainer = BinaryDefasagemTrainer(_make_dataset(), "Defasagem FC", cfg)

    model = FakePredictModel()
    trainer.model = model
    trainer.feature_cols_ = ["Mat", "Por", "Pedra"]
    trainer.const_cols_dropped_ = ["ConstCol"]

    new_data = pd.DataFrame(
        {
            "RA": ["RA-10"],
            "Mat": [7.5],
            "Por": [6.8],
            "Pedra": ["a"],
            "Defasagem FC": [-1],
            "ConstCol": [1],
        }
    )

    pred = trainer.predict(new_data)

    assert model.seen_columns == ["Mat", "Por", "Pedra"]
    assert pred.name == "prediction"
