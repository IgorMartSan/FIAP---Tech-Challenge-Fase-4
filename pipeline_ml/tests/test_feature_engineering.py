import pandas as pd
import pytest

from ba_feature_engineering.feature_engineering import (
    SingleYearToNextYearConfig,
    SingleYearToNextYearBuilder,
)


def test_single_year_builder_happy_path():
    """Objetivo: gerar dataset final com schema definido no config.

    Exemplo de uso: mapear `Mat/Por` -> `mat/por` e `Defasagem FC` -> `target`.
    """
    df_feat = pd.DataFrame(
        {
            "RA": ["RA-1", "RA-2"],
            "Mat": [7.5, 8.0],
            "Por": [6.8, 7.1],
        }
    )
    df_tgt = pd.DataFrame(
        {
            "RA": ["RA-1", "RA-2"],
            "Defasagem FC": [-1, 1],
        }
    )

    cfg = SingleYearToNextYearConfig(
        id_col="RA",
        output_schema=("RA", "mat", "por", "target"),
        feature_map={"mat": "Mat", "por": "Por"},
        target_map={"target": "Defasagem FC"},
        strict_schema=True,
        join_how="inner",
    )

    builder = SingleYearToNextYearBuilder(cfg)
    out = builder.build(df_feat, df_tgt)

    assert list(out.columns) == ["RA", "mat", "por", "target"]
    assert out["target"].tolist() == [-1, 1]


def test_single_year_builder_missing_source_col_raises():
    """Objetivo: falhar quando falta coluna de origem no mapping.

    Exemplo de uso: `por` mapeado para coluna inexistente dispara ValueError.
    """
    df_feat = pd.DataFrame({"RA": ["RA-1"], "Mat": [7.5]})
    df_tgt = pd.DataFrame({"RA": ["RA-1"], "Defasagem FC": [-1]})

    cfg = SingleYearToNextYearConfig(
        id_col="RA",
        output_schema=("RA", "mat", "por", "target"),
        feature_map={"mat": "Mat", "por": "Por"},
        target_map={"target": "Defasagem FC"},
        strict_schema=True,
    )

    builder = SingleYearToNextYearBuilder(cfg)

    with pytest.raises(ValueError):
        builder.build(df_feat, df_tgt)
