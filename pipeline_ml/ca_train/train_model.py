import json
import pickle
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import classification_report, f1_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import GroupShuffleSplit, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = PROJECT_ROOT / "pipeline_ml" / "outputs" / "dados_feature_engineering_consolidado.csv"
OUTPUT_DIR = PROJECT_ROOT / "pipeline_ml" / "outputs"
MODEL_PATH = OUTPUT_DIR / "modelo_risco_defasagem.pkl"
METRICS_PATH = OUTPUT_DIR / "metricas_risco_defasagem.json"
LEAKAGE_FEATURES_BY_TARGET = {
    "RISCO_DEFASAGEM": ["Fase", "Fase Ideal", "DERIV_FASE_NUMERICA", "Defasagem"],
}


def load_training_data(path: Path) -> pd.DataFrame:
    """
    Carrega o dataset consolidado para treino.
    """
    if not path.exists():
        raise FileNotFoundError(
            f"Arquivo nao encontrado: {path}. Rode pipeline_ml/dev_pipeline.py antes do treino."
        )
    return pd.read_csv(path)


def build_target(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cria alvo binario de risco de defasagem escolar.

    Regra:
    - 1: aluno em risco (Defasagem < 0)
    - 0: sem risco (Defasagem >= 0)
    """
    prepared = df.copy()
    if "Defasagem" not in prepared.columns:
        raise ValueError("A coluna 'Defasagem' nao existe no dataset consolidado.")

    prepared["Defasagem"] = pd.to_numeric(prepared["Defasagem"], errors="coerce")
    prepared = prepared.dropna(subset=["Defasagem"])
    prepared["RISCO_DEFASAGEM"] = (prepared["Defasagem"] < 0).astype(int)
    return prepared


def select_features(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series, pd.Series]:
    """
    Seleciona conjunto de features de alta disponibilidade e sem vazamento de alvo.
    """
    numeric_features = [
        "DERIV_ANO_REFERENCIA",
        "DERIV_ANOS_NO_PROGRAMA",
        "DERIV_FASE_NUMERICA",
        "DERIV_MEDIA_NOTAS",
        "DERIV_DESVIO_NOTAS",
        "DERIV_MEDIA_INDICADORES",
        "DERIV_QTD_AVALIADORES_PREENCHIDOS",
        "DERIV_QTD_RECOMENDACOES_PREENCHIDAS",
        "IAA",
        "IEG",
        "IPS",
        "IPP",
        "IDA",
        "IPV",
        "IAN",
        "Nº Av",
        "Mat",
        "Por",
    ]
    categorical_features = [
        "Fase",
        "Turma",
        "Gênero",
        "Instituição de ensino",
        "Fase Ideal",
    ]

    usable_numeric = [c for c in numeric_features if c in df.columns]
    usable_categorical = [c for c in categorical_features if c in df.columns]
    feature_columns = usable_numeric + usable_categorical
    if not feature_columns:
        raise ValueError("Nenhuma feature disponivel para treino.")

    if "RA" not in df.columns:
        raise ValueError("A coluna 'RA' e obrigatoria para split por aluno.")

    X = df[feature_columns]
    y = df["RISCO_DEFASAGEM"]
    groups = df["RA"]
    return X, y, groups


def build_training_pipeline(numeric_features: list[str], categorical_features: list[str]) -> Pipeline:
    """
    Monta pipeline de preprocessamento + modelo (scikit-learn).
    """
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", SimpleImputer(strategy="median"), numeric_features),
            (
                "cat",
                Pipeline(
                    steps=[
                        ("imputer", SimpleImputer(strategy="most_frequent")),
                        ("onehot", OneHotEncoder(handle_unknown="ignore")),
                    ]
                ),
                categorical_features,
            ),
        ]
    )

    model = RandomForestClassifier(
        n_estimators=300,
        max_depth=None,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1,
        class_weight="balanced",
    )

    return Pipeline(steps=[("preprocessor", preprocessor), ("model", model)])


def evaluate_model(model: Pipeline, X_test: pd.DataFrame, y_test: pd.Series) -> dict:
    """
    Avalia modelo de classificacao com metricas principais.
    """
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    metrics = {
        "f1": float(f1_score(y_test, y_pred, zero_division=0)),
        "precision": float(precision_score(y_test, y_pred, zero_division=0)),
        "recall": float(recall_score(y_test, y_pred, zero_division=0)),
        "roc_auc": float(roc_auc_score(y_test, y_prob)),
        "classification_report": classification_report(y_test, y_pred, zero_division=0),
    }
    return metrics


def save_training_artifacts(model: Pipeline, metrics: dict[str, Any]) -> None:
    """
    Persiste modelo e metricas em disco.
    """
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with MODEL_PATH.open("wb") as model_file:
        pickle.dump(model, model_file)
    METRICS_PATH.write_text(json.dumps(metrics, indent=2, ensure_ascii=False), encoding="utf-8")


def train_model_from_config(df: pd.DataFrame, config: dict[str, Any]) -> dict[str, Any]:
    """
    Treina modelo a partir de uma configuracao declarativa.

    Args:
        df: DataFrame com os dados de treino.
        config: Configuracao do treino contendo:
            - target_column (str): nome da coluna alvo.
            - feature_columns (list[str]): colunas usadas como entrada do modelo.
            - group_column (str, opcional): coluna para split por grupo (evita vazamento).
            - test_size (float, opcional): proporcao do conjunto de teste. Padrao: 0.2.
            - validation_size (float, opcional): proporcao do conjunto de validacao. Padrao: 0.2.
            - random_state (int, opcional): semente aleatoria. Padrao: 42.
            - model_params (dict, opcional): parametros do RandomForestClassifier.

    Returns:
        dict com pipeline treinado, metricas e metadados.
    """
    target_column = config.get("target_column")
    feature_columns = config.get("feature_columns", [])
    group_column = config.get("group_column")
    test_size = float(config.get("test_size", 0.2))
    validation_size = float(config.get("validation_size", 0.2))
    random_state = int(config.get("random_state", 42))
    model_params = config.get("model_params", {})
    leakage_features = config.get("leakage_features", LEAKAGE_FEATURES_BY_TARGET.get(target_column, []))
    verbose = bool(config.get("verbose", True))

    if verbose:
        print("\n[TRAIN] Iniciando treinamento com configuracao declarativa...")

    if not target_column:
        raise ValueError("config['target_column'] e obrigatorio.")
    if not feature_columns:
        raise ValueError("config['feature_columns'] precisa ter ao menos uma coluna.")
    if leakage_features:
        feature_columns = [col for col in feature_columns if col not in leakage_features]
        if verbose:
            print(f"[TRAIN] Features removidas por vazamento: {leakage_features}")
    if not feature_columns:
        raise ValueError("Nenhuma feature disponivel apos remover colunas com vazamento.")

    required_columns = feature_columns + [target_column]
    if group_column:
        required_columns.append(group_column)

    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Colunas ausentes no DataFrame: {missing_columns}")
    if test_size <= 0 or test_size >= 1:
        raise ValueError("config['test_size'] deve estar entre 0 e 1.")
    if validation_size <= 0 or validation_size >= 1:
        raise ValueError("config['validation_size'] deve estar entre 0 e 1.")
    if test_size + validation_size >= 1:
        raise ValueError("A soma de test_size e validation_size deve ser menor que 1.")

    prepared = df.dropna(subset=[target_column]).copy()
    prepared = prepared.replace({pd.NA: np.nan})
    X = prepared[feature_columns]
    y = prepared[target_column]
    val_ratio_within_train = validation_size / (1 - test_size)
    if verbose:
        print(f"[TRAIN] Dataset preparado: {len(prepared)} linhas | {len(feature_columns)} features")

    if group_column:
        groups = prepared[group_column]
        if verbose:
            print(f"[TRAIN] Split com grupos por coluna: {group_column}")
        test_splitter = GroupShuffleSplit(n_splits=1, test_size=test_size, random_state=random_state)
        train_val_idx, test_idx = next(test_splitter.split(X, y, groups=groups))

        X_train_val = X.iloc[train_val_idx]
        y_train_val = y.iloc[train_val_idx]
        groups_train_val = groups.iloc[train_val_idx]
        X_test = X.iloc[test_idx]
        y_test = y.iloc[test_idx]

        val_splitter = GroupShuffleSplit(n_splits=1, test_size=val_ratio_within_train, random_state=random_state)
        train_idx_rel, val_idx_rel = next(val_splitter.split(X_train_val, y_train_val, groups=groups_train_val))
        X_train = X_train_val.iloc[train_idx_rel]
        y_train = y_train_val.iloc[train_idx_rel]
        X_val = X_train_val.iloc[val_idx_rel]
        y_val = y_train_val.iloc[val_idx_rel]
    else:
        if verbose:
            print("[TRAIN] Split estratificado sem grupos")
        X_train_val, X_test, y_train_val, y_test = train_test_split(
            X,
            y,
            test_size=test_size,
            random_state=random_state,
            stratify=y,
        )
    if verbose:
        print(
            f"[TRAIN] Tamanhos -> treino: {len(X_train)} | "
            f"validacao: {len(X_val)} | teste: {len(X_test)}"
        )
        X_train, X_val, y_train, y_val = train_test_split(
            X_train_val,
            y_train_val,
            test_size=val_ratio_within_train,
            random_state=random_state,
            stratify=y_train_val,
        )

    numeric_features = X_train.select_dtypes(include=["number"]).columns.tolist()
    categorical_features = [col for col in feature_columns if col not in numeric_features]

    effective_model_params = {
        "n_estimators": 300,
        "max_depth": None,
        "min_samples_leaf": 2,
        "random_state": random_state,
        "n_jobs": -1,
        "class_weight": "balanced",
    }
    effective_model_params.update(model_params)

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", SimpleImputer(strategy="median"), numeric_features),
            (
                "cat",
                Pipeline(
                    steps=[
                        ("imputer", SimpleImputer(strategy="most_frequent")),
                        ("onehot", OneHotEncoder(handle_unknown="ignore")),
                    ]
                ),
                categorical_features,
            ),
        ]
    )
    model = RandomForestClassifier(**effective_model_params)
    pipeline = Pipeline(steps=[("preprocessor", preprocessor), ("model", model)])
    if verbose:
        print("[TRAIN] Treinando modelo...")
    pipeline.fit(X_train, y_train)

    if verbose:
        print("[TRAIN] Avaliando em validacao e teste...")
    validation_metrics = evaluate_model(pipeline, X_val, y_val)
    test_metrics = evaluate_model(pipeline, X_test, y_test)
    if verbose:
        print(
            f"[TRAIN] Validacao F1={validation_metrics['f1']:.4f} | "
            f"Teste F1={test_metrics['f1']:.4f}"
        )
    return {
        "pipeline": pipeline,
        "metrics": test_metrics,
        "validation_metrics": validation_metrics,
        "test_metrics": test_metrics,
        "X_train_shape": X_train.shape,
        "X_validation_shape": X_val.shape,
        "X_test_shape": X_test.shape,
        "feature_columns": feature_columns,
        "removed_leakage_features": leakage_features,
        "target_column": target_column,
    }


def main() -> None:
    # 1) Leitura e alvo
    df = load_training_data(DATA_PATH)
    df = build_target(df)
    X, _, _ = select_features(df)

    train_config = {
        "target_column": "RISCO_DEFASAGEM",
        "feature_columns": X.columns.tolist(),
        "group_column": "RA",
        "test_size": 0.2,
        "validation_size": 0.2,
        "random_state": 42,
        "model_params": {
            "n_estimators": 300,
            "min_samples_leaf": 2,
            "class_weight": "balanced",
        },
    }
    training_result = train_model_from_config(df=df, config=train_config)
    pipeline = training_result["pipeline"]
    validation_metrics = training_result["validation_metrics"]
    test_metrics = training_result["test_metrics"]

    # 4) Persistencia
    save_training_artifacts(
        pipeline,
        {
            "validation": validation_metrics,
            "test": test_metrics,
        },
    )

    print("Treino concluido.")
    print(
        f"Amostras de treino: {training_result['X_train_shape'][0]} | "
        f"validacao: {training_result['X_validation_shape'][0]} | "
        f"teste: {training_result['X_test_shape'][0]}"
    )
    print(f"Target: {training_result['target_column']}")
    print(f"Features usadas ({len(training_result['feature_columns'])}): {training_result['feature_columns']}")
    if training_result["removed_leakage_features"]:
        print(f"Features removidas por vazamento: {training_result['removed_leakage_features']}")
    print(f"Modelo salvo em: {MODEL_PATH}")
    print(f"Métricas salvas em: {METRICS_PATH}")
    print(
        f"Validacao - F1: {validation_metrics['f1']:.4f} | "
        f"Precision: {validation_metrics['precision']:.4f} | "
        f"Recall: {validation_metrics['recall']:.4f}"
    )
    print(
        f"Teste - F1: {test_metrics['f1']:.4f} | "
        f"Precision: {test_metrics['precision']:.4f} | "
        f"Recall: {test_metrics['recall']:.4f}"
    )


if __name__ == "__main__":
    main()
