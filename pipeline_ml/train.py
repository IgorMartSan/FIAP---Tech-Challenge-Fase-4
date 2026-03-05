import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, f1_score, accuracy_score
from lightgbm import LGBMClassifier

df = pd.read_csv("/mnt/HDD2TB/projetos_igor/FIAP---Tech-Challenge-Fase-4/pipeline_ml/data/model/pede_dataset_model_all_years.csv")

TARGET = "Defasagem FC"

# 1) y binário correto: negativo = ruim
y = (df[TARGET].astype(float) < 0).astype(int)

# 2) X
drop_cols = ["RA"]
if "Defasagem" in df.columns:
    drop_cols.append("Defasagem")

# object->category
for c in df.select_dtypes(include=["object"]).columns:
    if c not in drop_cols and c != TARGET:
        df[c] = df[c].astype("string").fillna("missing").astype("category")

X = df.drop(columns=drop_cols + [TARGET], errors="ignore")

# NaN numéricas
for col in X.select_dtypes(include=["number"]).columns:
    if X[col].isna().any():
        X[col] = X[col].fillna(X[col].median())

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

model = LGBMClassifier(
    n_estimators=1200,
    learning_rate=0.03,
    min_data_in_leaf=10,
    class_weight="balanced",
    random_state=42
    # verbosity=-1
)

model.fit(X_train, y_train)
pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, pred))
print("F1 (classe ruim=1):", f1_score(y_test, pred))
print(classification_report(y_test, pred, digits=4))