from __future__ import annotations

import os
import joblib
from dataclasses import dataclass, field
from typing import Optional, Sequence, Any

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, classification_report
from lightgbm import LGBMClassifier


@dataclass
class BinaryTrainingConfig:
    """
    Configuração de treino para classificação binária com LightGBM.
    """

    # divisão dos dados
    train_size: float = 0.70          # proporção usada para treino (ex: 70% do dataset)
    val_size: float = 0.15            # proporção usada para validação (ex: 15%)
    test_size: float = 0.15           # proporção usada para teste final (ex: 15%)
    random_state: int = 42            # semente aleatória para garantir reprodutibilidade
    stratify: bool = True             # mantém proporção das classes na divisão

    # colunas
    id_cols: Sequence[str] = field(default_factory=lambda: ("RA",))        # colunas de identificação que não entram no modelo (ex: RA)
    leak_cols: Sequence[str] = field(default_factory=lambda: ("Defasagem",)) # colunas que causariam data leakage

    # regra do target binário
    target_rule: str = "negative_is_1"  # regra para converter target em binário (ex: target < 0 -> classe 1)

    # tratamento de dados
    fill_numeric_with_median: bool = True        # preenche valores numéricos faltantes com mediana
    fill_categorical_with_missing: bool = True   # substitui NaN em categóricas por "missing"
    remove_constant_columns: bool = True         # remove colunas com apenas um valor

    # parâmetros do modelo
    n_estimators: int = 5000       # número máximo de árvores do modelo
    learning_rate: float = 0.03    # taxa de aprendizado do LightGBM
    num_leaves: int = 31           # número máximo de folhas por árvore
    min_data_in_leaf: int = 10     # mínimo de exemplos por folha
    subsample: float = 0.9         # fração de dados usada por árvore
    colsample_bytree: float = 0.9  # fração de features usada por árvore
    reg_lambda: float = 1.0        # regularização L2 do modelo
    force_col_wise: bool = True    # otimização para datasets tabulares
    verbosity: int = -1            # nível de log do LightGBM (-1 silencioso)

    # salvar modelo
    output_model_path: Optional[str] = None  # caminho onde o modelo treinado será salvo


class BinaryDefasagemTrainer:
    """
    Classe para treinar um modelo binário a partir de um DataFrame.
    Entrada:
      - dataset (pd.DataFrame)
      - target_col (str)
      - config (BinaryTrainingConfig)

    Exemplo de uso:

        trainer = BinaryDefasagemTrainer(
            dataset=df,
            target_col="Defasagem FC",
            config=BinaryTrainingConfig(
                output_model_path="/caminho/model.joblib"
            )
        )

        result = trainer.train()
        print(result["metrics"]["accuracy"])
        print(result["metrics"]["report"])
    """

    def __init__(
        self,
        dataset: pd.DataFrame,
        target_col: str,
        config: BinaryTrainingConfig,
    ) -> None:
        self.dataset = dataset.copy()
        self.target_col = target_col
        self.config = config

        self.model: Optional[LGBMClassifier] = None
        self.feature_cols_: list[str] = []
        self.const_cols_dropped_: list[str] = []

        self.X_train: Optional[pd.DataFrame] = None
        self.X_val: Optional[pd.DataFrame] = None
        self.X_test: Optional[pd.DataFrame] = None
        self.y_train: Optional[pd.Series] = None
        self.y_val: Optional[pd.Series] = None
        self.y_test: Optional[pd.Series] = None

    def _validate_sizes(self) -> None:
        total = self.config.train_size + self.config.val_size + self.config.test_size
        if abs(total - 1.0) > 1e-9:
            raise ValueError(
                f"train_size + val_size + test_size deve ser 1.0. Valor atual: {total}"
            )

    def _build_binary_target(self, y_raw: pd.Series) -> pd.Series:
        y_raw = y_raw.astype(float)

        if self.config.target_rule == "negative_is_1":
            return (y_raw < 0).astype(int)

        if self.config.target_rule == "positive_is_1":
            return (y_raw > 0).astype(int)

        if self.config.target_rule == "non_negative_is_1":
            return (y_raw >= 0).astype(int)

        raise ValueError(
            "target_rule inválido. Use: "
            "'negative_is_1', 'positive_is_1' ou 'non_negative_is_1'."
        )

    def _prepare_data(self) -> tuple[pd.DataFrame, pd.Series]:
        df = self.dataset.copy()

        if self.target_col not in df.columns:
            raise ValueError(
                f"Target '{self.target_col}' não encontrada. "
                f"Colunas disponíveis: {list(df.columns)}"
            )

        # remove colunas de ID
        for col in self.config.id_cols:
            df = df.drop(columns=[col], errors="ignore")

        # remove colunas que causam leakage
        for col in self.config.leak_cols:
            if col != self.target_col:
                df = df.drop(columns=[col], errors="ignore")

        # target
        y = self._build_binary_target(df[self.target_col])

        # features
        X = df.drop(columns=[self.target_col])

        # object -> category
        for col in X.select_dtypes(include=["object"]).columns:
            if self.config.fill_categorical_with_missing:
                X[col] = X[col].astype("string").fillna("missing").astype("category")
            else:
                X[col] = X[col].astype("category")

        # numéricas -> mediana
        if self.config.fill_numeric_with_median:
            for col in X.select_dtypes(include=["number"]).columns:
                if X[col].isna().any():
                    X[col] = X[col].fillna(X[col].median())

        # remove colunas constantes
        if self.config.remove_constant_columns:
            nunique = X.nunique(dropna=False)
            self.const_cols_dropped_ = nunique[nunique <= 1].index.tolist()
            if self.const_cols_dropped_:
                X = X.drop(columns=self.const_cols_dropped_)

        self.feature_cols_ = list(X.columns)
        return X, y

    def _split_data(self, X: pd.DataFrame, y: pd.Series) -> None:
        strat = y if self.config.stratify else None

        # primeiro: train e temp
        X_train, X_temp, y_train, y_temp = train_test_split(
            X,
            y,
            test_size=(1.0 - self.config.train_size),
            random_state=self.config.random_state,
            stratify=strat,
        )

        # agora divide temp em val e test proporcionalmente
        temp_total = self.config.val_size + self.config.test_size
        relative_test_size = self.config.test_size / temp_total

        strat_temp = y_temp if self.config.stratify else None

        X_val, X_test, y_val, y_test = train_test_split(
            X_temp,
            y_temp,
            test_size=relative_test_size,
            random_state=self.config.random_state,
            stratify=strat_temp,
        )

        self.X_train = X_train
        self.X_val = X_val
        self.X_test = X_test
        self.y_train = y_train
        self.y_val = y_val
        self.y_test = y_test

    def _build_model(self) -> LGBMClassifier:
        pos = int((self.y_train == 1).sum())
        neg = int((self.y_train == 0).sum())
        scale_pos_weight = neg / max(pos, 1)

        model = LGBMClassifier(
            n_estimators=self.config.n_estimators,
            learning_rate=self.config.learning_rate,
            num_leaves=self.config.num_leaves,
            min_data_in_leaf=self.config.min_data_in_leaf,
            subsample=self.config.subsample,
            colsample_bytree=self.config.colsample_bytree,
            reg_lambda=self.config.reg_lambda,
            scale_pos_weight=scale_pos_weight,
            random_state=self.config.random_state,
            force_col_wise=self.config.force_col_wise,
            verbosity=self.config.verbosity,
        )

        return model

    def train(self) -> dict[str, Any]:
        self._validate_sizes()

        X, y = self._prepare_data()
        self._split_data(X, y)

        self.model = self._build_model()

        self.model.fit(
            self.X_train,
            self.y_train,
            eval_set=[(self.X_val, self.y_val)],
            eval_metric="binary_logloss",
        )

        pred = self.model.predict(self.X_test)

        metrics = {
            "accuracy": float(accuracy_score(self.y_test, pred)),
            "f1": float(f1_score(self.y_test, pred)),
            "report": classification_report(self.y_test, pred, digits=4),
        }

        feature_importance = pd.DataFrame(
            {
                "feature": self.feature_cols_,
                "importance": self.model.feature_importances_,
            }
        ).sort_values("importance", ascending=False)

        result = {
            "metrics": metrics,
            "feature_importance": feature_importance,
            "shapes": {
                "dataset": self.dataset.shape,
                "train": self.X_train.shape,
                "val": self.X_val.shape,
                "test": self.X_test.shape,
            },
            "feature_cols": self.feature_cols_,
            "const_cols_dropped": self.const_cols_dropped_,
        }

        if self.config.output_model_path:
            self.save(self.config.output_model_path)

        return result

    def save(self, path: str) -> None:
        if self.model is None:
            raise RuntimeError("Treine o modelo antes de salvar.")

        os.makedirs(os.path.dirname(path), exist_ok=True)

        artifact = {
            "model": self.model,
            "feature_cols": self.feature_cols_,
            "target": self.target_col,
            "target_rule": self.config.target_rule,
            "const_cols_dropped": self.const_cols_dropped_,
            "id_cols": list(self.config.id_cols),
            "leak_cols": list(self.config.leak_cols),
        }

        joblib.dump(artifact, path)

    def predict(self, new_data: pd.DataFrame) -> pd.Series:
        if self.model is None:
            raise RuntimeError("Treine o modelo antes de prever.")

        X = new_data.copy()

        for col in self.config.id_cols:
            X = X.drop(columns=[col], errors="ignore")

        for col in self.config.leak_cols:
            X = X.drop(columns=[col], errors="ignore")

        if self.target_col in X.columns:
            X = X.drop(columns=[self.target_col], errors="ignore")

        for col in X.select_dtypes(include=["object"]).columns:
            if self.config.fill_categorical_with_missing:
                X[col] = X[col].astype("string").fillna("missing").astype("category")
            else:
                X[col] = X[col].astype("category")

        if self.config.fill_numeric_with_median:
            for col in X.select_dtypes(include=["number"]).columns:
                if X[col].isna().any():
                    X[col] = X[col].fillna(X[col].median())

        X = X.drop(columns=self.const_cols_dropped_, errors="ignore")
        X = X[self.feature_cols_]

        pred = self.model.predict(X)
        return pd.Series(pred, index=X.index, name="prediction")


# ============================================================
# EXEMPLO DE USO
# ============================================================
if __name__ == "__main__":
    DATASET_PATH = "/mnt/HDD2TB/projetos_igor/FIAP---Tech-Challenge-Fase-4/pipeline_ml/data/model/pede_dataset_model_all_years.csv"
    MODEL_PATH = "/mnt/HDD2TB/projetos_igor/FIAP---Tech-Challenge-Fase-4/pipeline_ml/data/model/model_defasagem_fc_binario_lgbm.joblib"

    df = pd.read_csv(DATASET_PATH)

    config = BinaryTrainingConfig(
        train_size=0.70,
        val_size=0.15,
        test_size=0.15,
        random_state=42,
        id_cols=("RA",),
        leak_cols=("Defasagem",),
        target_rule="negative_is_1",   # 1 = ruim se Defasagem FC < 0
        output_model_path=MODEL_PATH,
    )

    trainer = BinaryDefasagemTrainer(
        dataset=df,
        target_col="Defasagem FC",
        config=config,
    )

    result = trainer.train()

    print("==== SHAPES ====")
    print(result["shapes"])

    print("\n==== MÉTRICAS ====")
    print("Accuracy:", result["metrics"]["accuracy"])
    print("F1:", result["metrics"]["f1"])
    print(result["metrics"]["report"])

    print("\n==== FEATURE IMPORTANCE ====")
    print(result["feature_importance"].head(15))