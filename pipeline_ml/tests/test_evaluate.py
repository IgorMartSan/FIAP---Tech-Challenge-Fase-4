import numpy as np
import pandas as pd
import pytest

import da_evaluate.evaluate as eval_mod


class FakeModel:
    def predict(self, X):
        return np.zeros(len(X), dtype=int)


def test_evaluate_and_report(monkeypatch):
    """Objetivo: avaliar modelo fake e gerar relatório textual.

    Exemplo de uso: `BinaryModelEvaluator` retorna métricas para val/test.
    """
    artifact = {
        "model": FakeModel(),
        "feature_cols": ["Mat", "Por"],
        "target": "Defasagem FC",
        "const_cols_dropped": [],
    }

    monkeypatch.setattr(eval_mod.joblib, "load", lambda _: artifact)

    evaluator = eval_mod.BinaryModelEvaluator("/tmp/fake.joblib")

    val_df = pd.DataFrame(
        {
            "RA": ["RA-1", "RA-2"],
            "Mat": [7.5, 8.0],
            "Por": [6.8, 7.1],
            "Defasagem FC": [-1, 1],
        }
    )
    test_df = val_df.copy()

    val_target = pd.Series([1, 0])
    test_target = pd.Series([1, 0])

    results = evaluator.evaluate(val_df, val_target, test_df, test_target)

    assert "validation" in results
    assert "test" in results

    report = evaluator.build_text_report(results)
    assert "VALIDATION" in report
    assert "TEST" in report
