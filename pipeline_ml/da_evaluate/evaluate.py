from __future__ import annotations

import joblib
from dataclasses import dataclass
from typing import Any, Dict, Optional

import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    classification_report,
    confusion_matrix,
)


@dataclass
class EvaluationOutput:
    dataset_name: str
    accuracy: float
    f1: float
    precision: float
    recall: float
    confusion_matrix: list[list[int]]
    classification_report_text: str


class BinaryModelEvaluator:
    """
    Classe responsável por:
    - carregar um modelo treinado salvo em .joblib
    - avaliar em validation e test
    - gerar relatório com métricas
    """

    def __init__(self, model_path: str):
        self.model_path = model_path
        self.artifact: Optional[Dict[str, Any]] = None
        self.model = None
        self.feature_cols: list[str] = []
        self.target: Optional[str] = None
        self.const_cols_dropped: list[str] = []

    def load_model(self) -> None:
        """
        Carrega o artefato salvo do modelo.
        """
        self.artifact = joblib.load(self.model_path)
        self.model = self.artifact["model"]
        self.feature_cols = self.artifact.get("feature_cols", [])
        self.target = self.artifact.get("target")
        self.const_cols_dropped = self.artifact.get("const_cols_dropped", [])

    def _prepare_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Prepara o dataframe para inferência:
        - remove target se vier junto
        - remove colunas constantes antigas
        - converte object para category
        - reordena colunas conforme treino
        """
        X = df.copy()

        if self.target and self.target in X.columns:
            X = X.drop(columns=[self.target], errors="ignore")

        if "RA" in X.columns:
            X = X.drop(columns=["RA"], errors="ignore")

        if "Defasagem" in X.columns:
            X = X.drop(columns=["Defasagem"], errors="ignore")

        X = X.drop(columns=self.const_cols_dropped, errors="ignore")

        for col in X.select_dtypes(include=["object"]).columns:
            X[col] = X[col].astype("string").fillna("missing").astype("category")

        for col in X.select_dtypes(include=["number"]).columns:
            if X[col].isna().any():
                X[col] = X[col].fillna(X[col].median())

        missing_cols = [c for c in self.feature_cols if c not in X.columns]
        if missing_cols:
            raise ValueError(
                f"Faltam colunas necessárias para predição: {missing_cols}"
            )

        X = X[self.feature_cols]
        return X

    def _evaluate_dataset(
        self,
        X: pd.DataFrame,
        y: pd.Series,
        dataset_name: str,
    ) -> EvaluationOutput:
        """
        Avalia o modelo em um dataset específico.
        """
        pred = self.model.predict(X)

        return EvaluationOutput(
            dataset_name=dataset_name,
            accuracy=float(accuracy_score(y, pred)),
            f1=float(f1_score(y, pred)),
            precision=float(precision_score(y, pred)),
            recall=float(recall_score(y, pred)),
            confusion_matrix=confusion_matrix(y, pred).tolist(),
            classification_report_text=classification_report(y, pred, digits=4),
        )

    def evaluate(
        self,
        val_df: pd.DataFrame,
        val_target: pd.Series,
        test_df: pd.DataFrame,
        test_target: pd.Series,
    ) -> Dict[str, EvaluationOutput]:
        """
        Avalia o modelo nos datasets de validação e teste.
        """
        if self.model is None:
            self.load_model()

        X_val = self._prepare_features(val_df)
        X_test = self._prepare_features(test_df)

        val_result = self._evaluate_dataset(X_val, val_target, "validation")
        test_result = self._evaluate_dataset(X_test, test_target, "test")

        return {
            "validation": val_result,
            "test": test_result,
        }

    def build_text_report(
        self,
        results: Dict[str, EvaluationOutput],
    ) -> str:
        """
        Gera um relatório textual consolidado.
        """
        lines = []

        for dataset_name, result in results.items():
            lines.append(f"==== {dataset_name.upper()} ====")
            lines.append(f"Accuracy : {result.accuracy:.4f}")
            lines.append(f"F1       : {result.f1:.4f}")
            lines.append(f"Precision: {result.precision:.4f}")
            lines.append(f"Recall   : {result.recall:.4f}")
            lines.append(f"Confusion Matrix: {result.confusion_matrix}")
            lines.append("")
            lines.append(result.classification_report_text)
            lines.append("\n")

        return "\n".join(lines)