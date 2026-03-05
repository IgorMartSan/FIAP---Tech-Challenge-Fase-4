import re
import numpy as np
import pandas as pd
from dataclasses import dataclass
from typing import Any, Mapping, Sequence


# ---------------------------
# Config (passável por parâmetro)
# ---------------------------

@dataclass(frozen=True)
class PreprocessConfig:
    aliases_colunas: Mapping[str, str] = None
    colunas_numericas: Sequence[str] = ()
    colunas_categoricas: Sequence[str] = ()
    colunas_saida_ordenada: Sequence[str] = ()
    required_columns: Sequence[str] = ()
    na_like: Mapping[Any, Any] = None  # ex: {"": np.nan, "N/A": np.nan}
    drop_duplicate_columns_keep: str = "first"  # "first" ou "last"
    dedup_subset_rows: Sequence[str] = ()  # ex: ("RA","Ano") se quiser


# ---------------------------
# Helpers (pequenos e testáveis)
# ---------------------------

def remove_excel_suffix(col: str) -> str:
    """Remove sufixos .1/.2... do pandas e faz strip."""
    return re.sub(r"\.\d+$", "", str(col)).strip()


def standardize_columns(
    df: pd.DataFrame,
    *,
    remove_excel_suffixes: bool = True,
    drop_duplicated_columns: bool = True,
    keep: str = "first",
) -> pd.DataFrame:
    """
    Padroniza colunas:
    - remove sufixos .1/.2
    - strip
    - remove colunas duplicadas pelo nome
    """
    base = df.copy()
    cols = base.columns

    if remove_excel_suffixes:
        cols = [remove_excel_suffix(c) for c in cols]
    else:
        cols = [str(c).strip() for c in cols]

    base.columns = cols

    if drop_duplicated_columns:
        base = base.loc[:, ~base.columns.duplicated(keep=keep)]

    return base


def rename_merge_aliases(
    df: pd.DataFrame,
    *,
    aliases: Mapping[str, str],
) -> pd.DataFrame:
    """
    Renomeia/une colunas equivalentes.
    - Se origem existe e destino não: renomeia.
    - Se ambos existem: destino = destino.combine_first(origem), remove origem.
    """
    if not aliases:
        return df.copy()

    base = df.copy()
    for origem, destino in aliases.items():
        if origem not in base.columns:
            continue

        if destino in base.columns:
            base[destino] = base[destino].combine_first(base[origem])
            base = base.drop(columns=[origem])
        else:
            base = base.rename(columns={origem: destino})

    return base


def validate_alias_transfer(
    df_original: pd.DataFrame,
    df_after: pd.DataFrame,
    *,
    aliases: Mapping[str, str],
) -> list[str]:
    """
    Valida se, quando o destino estava NaN e a origem tinha valor,
    o destino após renome/merge ficou preenchido.
    Retorna lista de inconsistências. Se quiser, você dá raise fora.
    """
    inconsistencias: list[str] = []
    if not aliases:
        return inconsistencias

    for origem, destino in aliases.items():
        if origem not in df_original.columns:
            continue

        origem_notna = df_original[origem].notna()
        if not origem_notna.any():
            continue

        destino_antes = (
            df_original[destino]
            if destino in df_original.columns
            else pd.Series(np.nan, index=df_original.index)
        )

        precisa_transferir = origem_notna & destino_antes.isna()

        if destino not in df_after.columns:
            inconsistencias.append(
                f"Destino ausente após renomeação: '{destino}' (origem: '{origem}')"
            )
            continue

        destino_depois = df_after[destino]
        faltantes = int((precisa_transferir & destino_depois.isna()).sum())
        if faltantes > 0:
            inconsistencias.append(
                f"Falha na transferência {origem} -> {destino}: {faltantes} linhas não preenchidas."
            )

    return inconsistencias


def coerce_numeric_columns(
    df: pd.DataFrame,
    *,
    numeric_cols: Sequence[str],
) -> pd.DataFrame:
    """Converte colunas para numérico com errors='coerce'."""
    base = df.copy()
    for col in numeric_cols:
        if col in base.columns:
            base[col] = pd.to_numeric(base[col], errors="coerce")
    return base


def normalize_categorical_columns(
    df: pd.DataFrame,
    *,
    cat_cols: Sequence[str],
) -> pd.DataFrame:
    """
    Normaliza strings em colunas categóricas:
    - trim
    - preserva NaN
    """
    base = df.copy()
    for col in cat_cols:
        if col in base.columns:
            # Só aplica em valores não nulos
            base[col] = base[col].apply(lambda v: str(v).strip() if pd.notna(v) else np.nan)
    return base


def normalize_missing_values(
    df: pd.DataFrame,
    *,
    na_like: Mapping[Any, Any] | None = None,
) -> pd.DataFrame:
    """
    Normaliza ausentes:
    - troca pd.NA por np.nan
    - opcional: troca "", "N/A", "-", etc. por np.nan
    """
    base = df.replace({pd.NA: np.nan})
    if na_like:
        base = base.replace(na_like)
    return base


def validate_required_columns(
    df: pd.DataFrame,
    *,
    required: Sequence[str],
) -> None:
    """Falha se faltar coluna essencial."""
    if not required:
        return
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Colunas obrigatórias ausentes: {missing}")


def drop_duplicate_rows(
    df: pd.DataFrame,
    *,
    subset: Sequence[str],
    keep: str = "first",
) -> pd.DataFrame:
    """Remove linhas duplicadas por uma chave (ex: aluno_id + ano)."""
    if not subset:
        return df.copy()
    base = df.copy()
    return base.drop_duplicates(subset=list(subset), keep=keep)


def reorder_columns(
    df: pd.DataFrame,
    *,
    ordered_cols: Sequence[str],
) -> pd.DataFrame:
    """
    Reordena:
    - colunas conhecidas primeiro na ordem
    - resto no final
    """
    if not ordered_cols:
        return df.copy()

    base = df.copy()
    existing = [c for c in ordered_cols if c in base.columns]
    remaining = [c for c in base.columns if c not in existing]
    return base[existing + remaining].copy()


# ---------------------------
# Pipeline (reutilizável)
# ---------------------------

def preprocess(
    df: pd.DataFrame,
    *,
    config: PreprocessConfig,
    validate_aliases: bool = True,
) -> pd.DataFrame:
    """
    Pipeline de preprocessamento configurável por parâmetro.
    """
    original = df.copy()

    base = standardize_columns(
        df,
        remove_excel_suffixes=True,
        drop_duplicated_columns=True,
        keep=config.drop_duplicate_columns_keep,
    )

    # opcional: remover linhas duplicadas por chave
    base = drop_duplicate_rows(base, subset=config.dedup_subset_rows, keep="first")

    # normaliza ausentes cedo (evita "" virar categoria)
    base = normalize_missing_values(base, na_like=config.na_like)

    # aliases
    base_aliased = rename_merge_aliases(base, aliases=config.aliases_colunas or {})

    if validate_aliases:
        inconsist = validate_alias_transfer(original, base_aliased, aliases=config.aliases_colunas or {})
        if inconsist:
            raise ValueError(f"Inconsistências de transferência de aliases: {inconsist}")

    # tipos
    base_aliased = coerce_numeric_columns(base_aliased, numeric_cols=config.colunas_numericas)

    # categóricas
    base_aliased = normalize_categorical_columns(base_aliased, cat_cols=config.colunas_categoricas)

    # valida colunas essenciais
    validate_required_columns(base_aliased, required=config.required_columns)

    # ordena saída
    base_aliased = reorder_columns(base_aliased, ordered_cols=config.colunas_saida_ordenada)

    return base_aliased