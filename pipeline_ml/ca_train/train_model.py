import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, classification_report
from lightgbm import LGBMClassifier

# ============================================================
# CONFIG (caminho fixo que você pediu)
# ============================================================
DATASET_PATH = "/mnt/HDD2TB/projetos_igor/FIAP---Tech-Challenge-Fase-4/pipeline_ml/data/model/pede_dataset_model_all_years.csv"
OUT_DIR = "/mnt/HDD2TB/projetos_igor/FIAP---Tech-Challenge-Fase-4/pipeline_ml/data/model"
OUT_MODEL_PATH = os.path.join(OUT_DIR, "model_defasagem_fc_binario_lgbm.joblib")

TARGET_COL = "Defasagem FC"   # alvo
ID_COL = "RA"                 # remover
DROP_LEAK_COL = "Defasagem"   # remover para evitar leakage (se existir)

RANDOM_STATE = 42

# ============================================================
# 1) LOAD
# ============================================================
df = pd.read_csv(DATASET_PATH)
print("Dataset:", df.shape)

# ============================================================
# 2) LIMPEZA
# ============================================================
df = df.drop(columns=[ID_COL], errors="ignore")
df = df.drop(columns=[DROP_LEAK_COL], errors="ignore")

# Target binário:
# 1 = ruim (negativo)
# 0 = bom (>= 0)
y = (df[TARGET_COL].astype(float) < 0).astype(int)

X = df.drop(columns=[TARGET_COL])

# object -> category + missing
for c in X.select_dtypes(include=["object"]).columns:
    X[c] = X[c].astype("string").fillna("missing").astype("category")

# NaN numéricas -> mediana
for c in X.select_dtypes(include=["number"]).columns:
    if X[c].isna().any():
        X[c] = X[c].fillna(X[c].median())

# remover colunas constantes
nunique = X.nunique(dropna=False)
const_cols = nunique[nunique <= 1].index.tolist()
if const_cols:
    X = X.drop(columns=const_cols)
    print("Constantes removidas:", const_cols)

print("Features:", X.shape[1])

# ============================================================
# 3) SPLIT: train / val / test (70/15/15)
# ============================================================
# primeiro separa (train) e (temp = val+test)
X_train, X_temp, y_train, y_temp = train_test_split(
    X, y,
    test_size=0.30,
    random_state=RANDOM_STATE,
    stratify=y
)

# agora separa val e test (metade/metade do temp)
X_val, X_test, y_val, y_test = train_test_split(
    X_temp, y_temp,
    test_size=0.50,
    random_state=RANDOM_STATE,
    stratify=y_temp
)

print(f"Train: {len(X_train)} | Val: {len(X_val)} | Test: {len(X_test)}")

# ============================================================
# 4) MODELO (com desbalanceamento)
# ============================================================
pos = int((y_train == 1).sum())
neg = int((y_train == 0).sum())
scale_pos_weight = neg / max(pos, 1)

model = LGBMClassifier(
    n_estimators=5000,          # alto pq usamos early stopping
    learning_rate=0.03,
    num_leaves=31,
    min_data_in_leaf=10,
    subsample=0.9,
    colsample_bytree=0.9,
    reg_lambda=1.0,
    scale_pos_weight=scale_pos_weight,
    random_state=RANDOM_STATE,
    force_col_wise=True,
    verbosity=-1
)

# ============================================================
# 5) TREINO com validação (early stopping)
# ============================================================
model.fit(
    X_train, y_train,
    eval_set=[(X_val, y_val)],
    eval_metric="binary_logloss",
    callbacks=[],
)

# ============================================================
# 6) AVALIAÇÃO no TESTE (final)
# ============================================================
pred = model.predict(X_test)

print("\n==== RESULTADOS (TESTE) ====")
print("Accuracy:", accuracy_score(y_test, pred))
print("F1 (classe ruim=1):", f1_score(y_test, pred))
print(classification_report(y_test, pred, digits=4))

# ============================================================
# 7) SALVAR MODELO + METADATA
# ============================================================
os.makedirs(OUT_DIR, exist_ok=True)

artifact = {
    "model": model,
    "feature_cols": list(X.columns),
    "target": TARGET_COL,
    "binary_rule": "1 if Defasagem FC < 0 else 0",
    "scale_pos_weight": scale_pos_weight,
    "const_cols_dropped": const_cols,
}

joblib.dump(artifact, OUT_MODEL_PATH)
print(f"[OK] modelo salvo em: {OUT_MODEL_PATH}")


import pandas as pd

fi = pd.DataFrame({
    "feature": X.columns,
    "importance": model.feature_importances_
}).sort_values("importance", ascending=False)

print(fi.head(15))