import os
import numpy as np
import pandas as pd

from utils.io import read_pede_excel

from aa_preprocessing.preprocessing import PreprocessConfig, preprocess
from aa_preprocessing.preprocessing_config import (
    ALIASES_COLUNAS,
    COLUNAS_NUMERICAS,
    COLUNAS_CATEGORICAS,
    COLUNAS_SAIDA_ORDENADA,
    CATEGORICAL_VALUE_MAP,          # ✅ novo
    CATEGORICAL_ALLOWED_VALUES,     # ✅ novo
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

from ca_train.train_model import TrainConfig, DefasagemTrainer

PATH = "/mnt/HDD2TB/projetos_igor/FIAP---Tech-Challenge-Fase-4/arquivos_do_projeto/BASE DE DADOS PEDE 2024 - DATATHON.xlsx"


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

    # -------------------------------
    # 1) carregar datasets (brutos)
    # -------------------------------
    datasets = read_pede_excel(PATH)

    df_2022 = get_sheet_by_year(datasets, 2022)
    df_2023 = get_sheet_by_year(datasets, 2023)
    df_2024 = get_sheet_by_year(datasets, 2024)

    # cria a coluna Ano para o preprocess conseguir deduplicar por ("RA","Ano")
    df_2022["Ano"] = 2022
    df_2023["Ano"] = 2023
    df_2024["Ano"] = 2024

    os.makedirs("data/bruto", exist_ok=True)
    df_2022.to_csv("data/bruto/pede_2022.csv", index=False)
    df_2023.to_csv("data/bruto/pede_2023.csv", index=False)
    df_2024.to_csv("data/bruto/pede_2024.csv", index=False)

    # -------------------------------
    # 2) configurar preprocessamento
    # -------------------------------
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

        # normalização de texto
        categorical_lower=True,
        categorical_remove_accents=True,
        categorical_collapse_whitespace=True,

        # ✅ novo: canonização + validação de categorias (contrato)
        categorical_value_map=CATEGORICAL_VALUE_MAP,
        categorical_allowed_values=CATEGORICAL_ALLOWED_VALUES,
        categorical_validate_strict=True,   # True = se achar valor fora do contrato, dá erro
    )

    # -------------------------------
    # 3) preprocessar datasets
    # -------------------------------
    df_2022 = preprocess(df_2022, config=preprocess_config)
    df_2023 = preprocess(df_2023, config=preprocess_config)
    df_2024 = preprocess(df_2024, config=preprocess_config)

    os.makedirs("data/processed", exist_ok=True)
    df_2022.to_csv("data/processed/pede_2022.csv", index=False)
    df_2023.to_csv("data/processed/pede_2023.csv", index=False)
    df_2024.to_csv("data/processed/pede_2024.csv", index=False)




    # -------------------------------
    # 4) feature engineering (single-year -> next-year) via loop
    # -------------------------------
    os.makedirs("data/model", exist_ok=True)

    # lista de pares (features_year -> target_year)
    year_pairs = [
        (2022, 2023),
        (2023, 2024),
        # (2024, 2025),  # quando tiver 2025, só descomentar/gerar dinamicamente
    ]

    # seus dataframes já preprocessados
    dfs_by_year = {
        2022: df_2022,
        2023: df_2023,
        2024: df_2024,
    }

    # feature_map por ano (cada ano pode apontar para colunas diferentes tipo "Pedra 2022", "Pedra 2023"...)
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
            feature_map=feature_map_by_year[feat_year],   # usa o map do ano das features
            target_map=TARGET_MAP,                        # seu target map aponta pro INDE do ano target
            join_how=JOIN_TYPE,
            strict_schema=STRICT_SCHEMA,
        )

        builder = SingleYearToNextYearBuilder(fe_config)

        ds_model = builder.build(
            df_features=df_features,
            df_target=df_target,
        )

        ds_model = ds_model.dropna()

        print(ds_model.dtypes)

        out_path = f"data/model/pede_dataset_model_{feat_year}_to_{tgt_year}.csv"
        ds_model.to_csv(out_path, index=False, encoding="utf-8")

        print(f"[OK] salvo: {out_path} | shape={ds_model.shape}")

        datasets_model.append(ds_model)

    dataset_final = pd.concat(datasets_model, ignore_index=True)

    dataset_final.to_csv(
    "data/model/pede_dataset_model_all_years.csv",
    index=False
)

    print(dataset_final.shape)



    

    # -------------------------------
    # 5) salvar dataset de modelagem
    # -------------------------------
