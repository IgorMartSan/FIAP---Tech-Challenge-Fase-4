import joblib
import pandas as pd


class ModelService:
    def __init__(self, model_path: str):
        artifact = joblib.load(model_path)

        self.model = artifact["model"]
        self.feature_cols = artifact["feature_cols"]
        self.target = artifact.get("target")
        self.target_rule = artifact.get("target_rule")
        self.const_cols_dropped = artifact.get("const_cols_dropped", [])
        self.id_cols = artifact.get("id_cols", ["RA"])
        self.leak_cols = artifact.get("leak_cols", ["Defasagem"])

    def _prepare_features(self, df: pd.DataFrame) -> pd.DataFrame:
        X = df.copy()

        if self.target and self.target in X.columns:
            X = X.drop(columns=[self.target], errors="ignore")

        X = X.drop(columns=self.id_cols, errors="ignore")
        X = X.drop(columns=self.leak_cols, errors="ignore")
        X = X.drop(columns=self.const_cols_dropped, errors="ignore")

        for col in X.select_dtypes(include=["object"]).columns:
            X[col] = X[col].astype("string").fillna("missing").astype("category")

        for col in X.select_dtypes(include=["number"]).columns:
            if X[col].isna().any():
                X[col] = X[col].fillna(X[col].median())

        missing_cols = [c for c in self.feature_cols if c not in X.columns]
        if missing_cols:
            raise ValueError(f"Faltam colunas para predição: {missing_cols}")

        return X[self.feature_cols]

    def predict(self, df: pd.DataFrame):
        X = self._prepare_features(df)

        pred = self.model.predict(X)
        prob = self.model.predict_proba(X)[:, 1]

        return pred, prob