import os
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split

from utils.io import read_pede_excel

from aa_preprocessing.preprocessing import PreprocessConfig, preprocess
from aa_preprocessing.preprocessing_config import (
    ALIASES_COLUNAS,
    COLUNAS_NUMERICAS,
    COLUNAS_CATEGORICAS,
    COLUNAS_SAIDA_ORDENADA,
    CATEGORICAL_VALUE_MAP,
    CATEGORICAL_ALLOWED_VALUES,
)

from ba_feature_engineering.feature_engineering import (
    SingleYearToNextYearConfig,
    SingleYearToNextYearBuilder,
)

from ba_feature_engineering.feature_engineering_config import (
    ID_COL,
    OUTPUT_SCHEMA,
    FEATURE_MAP_2022,
    FEATURE_MAP_2023,
    FEATURE_MAP_2024,
    TARGET_MAP,
    JOIN_TYPE,
    STRICT_SCHEMA,
)

from ca_train.train_model import BinaryTrainingConfig, BinaryDefasagemTrainer
from da_evaluate.evaluate import BinaryModelEvaluator


PATH = "/home/igor/Projetos/FIAP---Tech-Challenge-Fase-4/arquivos_do_projeto/BASE DE DADOS PEDE 2024 - DATATHON.xlsx"


def get_sheet_by_year(datasets: dict, year: int) -> pd.DataFrame:
    year_str = str(year)

    if year_str in datasets:
        return datasets[year_str]

    for sheet_name, df in datasets.items():
        if year_str in str(sheet_name):
            return df

    available = ", ".join(map(str, datasets.keys()))
    raise KeyError(
        f"Nao foi encontrada aba para o ano {year_str}. "
        f"Abas disponiveis: {available}"
    )


if __name__ == "__main__":

    # ---------------------------------------------------------
    # 1) carregar datasets brutos
    # ---------------------------------------------------------
    datasets = read_pede_excel(PATH)

    df_2022 = get_sheet_by_year(datasets, 2022)
    df_2023 = get_sheet_by_year(datasets, 2023)
    df_2024 = get_sheet_by_year(datasets, 2024)

    # cria coluna Ano para deduplicação
    df_2022["Ano"] = 2022
    df_2023["Ano"] = 2023
    df_2024["Ano"] = 2024

    os.makedirs("data/bruto", exist_ok=True)
    df_2022.to_csv("data/bruto/pede_2022.csv", index=False)
    df_2023.to_csv("data/bruto/pede_2023.csv", index=False)
    df_2024.to_csv("data/bruto/pede_2024.csv", index=False)

    # ---------------------------------------------------------
    # 2) configurar preprocessamento
    # ---------------------------------------------------------
    preprocess_config = PreprocessConfig(
        aliases_colunas=ALIASES_COLUNAS,
        colunas_numericas=COLUNAS_NUMERICAS,
        colunas_categoricas=COLUNAS_CATEGORICAS,
        colunas_saida_ordenada=COLUNAS_SAIDA_ORDENADA,
        required_columns=["RA", "Nome"],
        na_like={
            "": np.nan,
            " ": np.nan,
            "N/A": np.nan,
            "NA": np.nan,
            "-": np.nan,
        },
        dedup_subset_rows=("RA", "Ano"),
        categorical_lower=True,
        categorical_remove_accents=True,
        categorical_collapse_whitespace=True,
        categorical_value_map=CATEGORICAL_VALUE_MAP,
        categorical_allowed_values=CATEGORICAL_ALLOWED_VALUES,
        categorical_validate_strict=True,
    )

    # ---------------------------------------------------------
    # 3) preprocessar datasets
    # ---------------------------------------------------------
    df_2022 = preprocess(df_2022, config=preprocess_config)
    df_2023 = preprocess(df_2023, config=preprocess_config)
    df_2024 = preprocess(df_2024, config=preprocess_config)

    os.makedirs("data/processed", exist_ok=True)
    df_2022.to_csv("data/processed/pede_2022.csv", index=False)
    df_2023.to_csv("data/processed/pede_2023.csv", index=False)
    df_2024.to_csv("data/processed/pede_2024.csv", index=False)

    # ---------------------------------------------------------
    # 4) feature engineering (ano A -> ano A+1)
    # ---------------------------------------------------------
    os.makedirs("data/model", exist_ok=True)

    year_pairs = [
        (2022, 2023),
        (2023, 2024),
    ]

    dfs_by_year = {
        2022: df_2022,
        2023: df_2023,
        2024: df_2024,
    }

    feature_map_by_year = {
        2022: FEATURE_MAP_2022,
        2023: FEATURE_MAP_2023,
        2024: FEATURE_MAP_2024,
    }

    datasets_model = []

    for feat_year, tgt_year in year_pairs:
        df_features = dfs_by_year[feat_year]
        df_target = dfs_by_year[tgt_year]

        fe_config = SingleYearToNextYearConfig(
            id_col=ID_COL,
            output_schema=OUTPUT_SCHEMA,
            feature_map=feature_map_by_year[feat_year],
            target_map=TARGET_MAP,
            join_how=JOIN_TYPE,
            strict_schema=STRICT_SCHEMA,
        )

        builder = SingleYearToNextYearBuilder(fe_config)

        ds_model = builder.build(
            df_features=df_features,
            df_target=df_target,
        )

        ds_model = ds_model.dropna()

        print(f"\n[INFO] Dataset {feat_year} -> {tgt_year}")
        print(ds_model.dtypes)

        out_path = f"data/model/pede_dataset_model_{feat_year}_to_{tgt_year}.csv"
        ds_model.to_csv(out_path, index=False, encoding="utf-8")

        print(f"[OK] salvo: {out_path} | shape={ds_model.shape}")

        datasets_model.append(ds_model)

    # ---------------------------------------------------------
    # 5) juntar datasets de modelagem
    # ---------------------------------------------------------
    dataset_final = pd.concat(datasets_model, ignore_index=True)

    dataset_final_path = "data/model/pede_dataset_model_all_years.csv"
    dataset_final.to_csv(dataset_final_path, index=False)

    print(f"\n[OK] Dataset final salvo: {dataset_final_path}")
    print(f"[INFO] Shape final: {dataset_final.shape}")

    # ---------------------------------------------------------
    # 6) configurar treino
    # ---------------------------------------------------------
    model_output_path = "data/model/model_defasagem_fc_binario_lgbm.joblib"

    train_config = BinaryTrainingConfig(
        train_size=0.70,
        val_size=0.15,
        test_size=0.15,
        random_state=42,
        stratify=True,
        id_cols=("RA",),
        leak_cols=("Defasagem",),
        target_rule="negative_is_1",
        fill_numeric_with_median=True,
        fill_categorical_with_missing=True,
        remove_constant_columns=True,
        n_estimators=5000,
        learning_rate=0.03,
        num_leaves=31,
        min_data_in_leaf=10,
        subsample=0.9,
        colsample_bytree=0.9,
        reg_lambda=1.0,
        force_col_wise=True,
        verbosity=-1,
        output_model_path=model_output_path,
    )

    # ---------------------------------------------------------
    # 7) treinar modelo
    # ---------------------------------------------------------
    trainer = BinaryDefasagemTrainer(
        dataset=dataset_final,
        target_col="Defasagem futura",
        config=train_config,
    )

    result = trainer.train()

    # ---------------------------------------------------------
    # 8) exibir resultados de treino
    # ---------------------------------------------------------
    print("\n==== SHAPES ====")
    print(result["shapes"])

    print("\n==== MÉTRICAS ====")
    print("Accuracy:", result["metrics"]["accuracy"])
    print("F1:", result["metrics"]["f1"])
    print(result["metrics"]["report"])

    print("\n==== FEATURE IMPORTANCE ====")
    print(result["feature_importance"].head(15))

    fi_path = "data/model/feature_importance.csv"
    result["feature_importance"].to_csv(fi_path, index=False)
    print(f"\n[OK] feature importance salva em: {fi_path}")

    # ---------------------------------------------------------
    # 9) configurar avaliação
    # ---------------------------------------------------------
    evaluate_dataset_path = "/home/igor/Projetos/FIAP---Tech-Challenge-Fase-4/pipeline_ml/data/model/pede_dataset_model_all_years.csv"
    evaluate_model_path = "/home/igor/Projetos/FIAP---Tech-Challenge-Fase-4/pipeline_ml/data/model/model_defasagem_fc_binario_lgbm.joblib"

    # ---------------------------------------------------------
    # 10) preparar dados para avaliação
    # ---------------------------------------------------------
    df_eval = pd.read_csv(evaluate_dataset_path)

    y_eval = (df_eval["Defasagem futura"].astype(float) < 0).astype(int)
    X_eval = df_eval.copy()

    X_train_eval, X_temp_eval, y_train_eval, y_temp_eval = train_test_split(
        X_eval,
        y_eval,
        test_size=0.30,
        random_state=42,
        stratify=y_eval,
    )

    X_val_eval, X_test_eval, y_val_eval, y_test_eval = train_test_split(
        X_temp_eval,
        y_temp_eval,
        test_size=0.50,
        random_state=42,
        stratify=y_temp_eval,
    )

    # ---------------------------------------------------------
    # 11) avaliar modelo carregado
    # ---------------------------------------------------------
    evaluator = BinaryModelEvaluator(model_path=evaluate_model_path)

    evaluation_results = evaluator.evaluate(
        val_df=X_val_eval,
        val_target=y_val_eval,
        test_df=X_test_eval,
        test_target=y_test_eval,
    )

    evaluation_report_text = evaluator.build_text_report(evaluation_results)

    # ---------------------------------------------------------
    # 12) exibir e salvar relatório de avaliação
    # ---------------------------------------------------------
    print("\n==== EVALUATION REPORT ====")
    print(evaluation_report_text)

    evaluation_report_path = "data/model/evaluation_report.txt"
    with open(evaluation_report_path, "w", encoding="utf-8") as f:
        f.write(evaluation_report_text)

    print(f"[OK] relatório de avaliação salvo em: {evaluation_report_path}")