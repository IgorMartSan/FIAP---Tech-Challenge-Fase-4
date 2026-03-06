import pandas as pd
import numpy as np
import pytest

from aa_preprocessing.preprocessing import (
    PreprocessConfig,
    standardize_columns,
    rename_merge_aliases,
    validate_alias_transfer,
    preprocess,
)


def test_standardize_columns_remove_suffix_and_duplicates():
    """Objetivo: padronizar colunas removendo sufixos e duplicadas.

    Exemplo de uso: DataFrame com colunas `Col` e `Col.1` vira apenas `Col`.
    """
    df = pd.DataFrame([[1, 2]], columns=["Col", "Col.1"])
    out = standardize_columns(df, remove_excel_suffixes=True, drop_duplicated_columns=True)
    assert list(out.columns) == ["Col"]
    assert out.iloc[0, 0] == 1


def test_alias_merge_and_validate_transfer():
    """Objetivo: unir aliases sem perder informação.

    Exemplo de uso: mover valores de `A` para `B` quando `B` está vazio.
    """
    df = pd.DataFrame({"A": [1, np.nan], "B": [np.nan, 2]})
    out = rename_merge_aliases(df, aliases={"A": "B"})

    inconsist = validate_alias_transfer(df, out, aliases={"A": "B"})
    assert inconsist == []
    assert "A" not in out.columns
    assert out["B"].tolist() == [1, 2]


def test_preprocess_end_to_end():
    """Objetivo: executar o pipeline completo e validar efeitos principais.

    Exemplo de uso: dedup por `RA/Ano`, normalizar `Pedra 0` e converter numéricas.
    """
    df = pd.DataFrame(
        [
            {
                "RA": "RA-1",
                "Mat": "7.5",
                "Por": "6.8",
                "Pedra 0": "  Ágata ",
                "INDE": 7.12,
                "Ano": 2023,
            },
            {
                "RA": "RA-1",
                "Mat": "7.5",
                "Por": "6.8",
                "Pedra 0": "  Ágata ",
                "INDE": 7.12,
                "Ano": 2023,
            },
        ]
    )

    config = PreprocessConfig(
        aliases_colunas={"Pedra 0": "Pedra_0"},
        colunas_numericas=("Mat", "Por"),
        colunas_categoricas=("Pedra_0",),
        required_columns=("RA", "Mat", "Por", "Pedra_0", "INDE"),
        dedup_subset_rows=("RA", "Ano"),
        colunas_saida_ordenada=("RA", "Mat", "Por", "Pedra_0", "INDE"),
        na_like={"": np.nan},
    )

    out = preprocess(df, config=config)

    assert list(out.columns) == ["RA", "Mat", "Por", "Pedra_0", "INDE", "Ano"]
    assert len(out) == 1
    assert out.loc[0, "Pedra_0"] == "agata"
    assert out["Mat"].dtype.kind in "fi"
