import pandas as pd
import numpy as np
from utils.io import read_pede_excel
from aa_preprocessing.preprocessing import PreprocessConfig, preprocess
from aa_preprocessing.preprocessing_config import (
    ALIASES_COLUNAS,
    COLUNAS_NUMERICAS,
    COLUNAS_CATEGORICAS,
    COLUNAS_SAIDA_ORDENADA,
)
import os


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

    # -------------------------------
    # 1 carregar datasets
    # -------------------------------

    datasets = read_pede_excel(PATH)

    df_2022 = get_sheet_by_year(datasets, 2022)
    df_2023 = get_sheet_by_year(datasets, 2023)
    df_2024 = get_sheet_by_year(datasets, 2024)


    # -------------------------------
    # 2 configurar preprocessamento
    # -------------------------------

    config = PreprocessConfig(
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
            "-": np.nan
        },
        dedup_subset_rows=("RA", "Ano"),
    )


    # -------------------------------
    # 3 preprocessar datasets
    # -------------------------------

    df_2022 = preprocess(df_2022, config=config)
    df_2023 = preprocess(df_2023, config=config)
    df_2024 = preprocess(df_2024, config=config)


    # -------------------------------
    # 4 salvar datasets separados
    # -------------------------------

    os.makedirs("data/processed", exist_ok=True)

    df_2022.to_csv("data/processed/bruto_pede_2022.csv", index=False)
    df_2023.to_csv("data/processed/pede_2023.csv", index=False)
    df_2024.to_csv("data/processed/pede_2024.csv", index=False)


    print("Datasets preprocessados salvos com sucesso!")
    print("2022:", df_2022.shape)
    print("2023:", df_2023.shape)
    print("2024:", df_2024.shape)