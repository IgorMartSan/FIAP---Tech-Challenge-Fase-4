import re
import unicodedata
from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd


# =============================================================================
# Config
# =============================================================================

@dataclass(frozen=True)
class PreprocessConfig:
    """
    Configuração do pipeline de preprocessamento.

    Principais responsabilidades:
    - Padronizar nomes de colunas (remover sufixos .1/.2 e duplicadas)
    - Normalizar valores ausentes (na_like)
    - Unificar colunas equivalentes (aliases_colunas)
    - Converter colunas numéricas (pd.to_numeric(errors="coerce"))
    - Normalizar colunas categóricas (strip/lower/sem acento/colapsar espaços)
    - (Opcional) Canonizar valores categóricos por coluna via mapeamento
    - (Opcional) Validar que valores categóricos finais pertencem a um conjunto permitido
    - Deduplicar linhas por chave (dedup_subset_rows)
    - Validar colunas obrigatórias e reordenar colunas de saída
    """
    # Normalização de nomes
    aliases_colunas: Mapping[str, str] = field(default_factory=dict)
    drop_duplicate_columns_keep: str = "first"  # "first" ou "last"

    # Tipos/colunas
    colunas_numericas: Sequence[str] = ()
    colunas_categoricas: Sequence[str] = ()
    colunas_saida_ordenada: Sequence[str] = ()
    required_columns: Sequence[str] = ()

    # Ausentes e dedup
    na_like: Mapping[Any, Any] = field(default_factory=dict)
    dedup_subset_rows: Sequence[str] = ()  # ex: ("RA", "Ano")

    # Normalização de texto
    categorical_lower: bool = True
    categorical_remove_accents: bool = True
    categorical_collapse_whitespace: bool = True

    # Canonização + validação (contrato)
    categorical_value_map: Mapping[str, Mapping[str, str]] = field(default_factory=dict)
    categorical_allowed_values: Mapping[str, Sequence[str]] = field(default_factory=dict)
    categorical_validate_strict: bool = True


# =============================================================================
# Helpers
# =============================================================================

def remove_excel_suffix(col: str) -> str:
    """Remove sufixos .1/.2... do pandas ao ler Excel e aplica strip()."""
    return re.sub(r"\.\d+$", "", str(col)).strip()


def standardize_columns(
    df: pd.DataFrame,
    *,
    remove_excel_suffixes: bool = True,
    drop_duplicated_columns: bool = True,
    keep: str = "first",
) -> pd.DataFrame:
    """
    Padroniza nomes de colunas e remove colunas duplicadas.

    - Remove sufixos ".1", ".2" (opcional)
    - Aplica strip() nos nomes
    - Remove colunas duplicadas pelo nome (opcional)
    """
    base = df.copy()

    if remove_excel_suffixes:
        base.columns = [remove_excel_suffix(c) for c in base.columns]
    else:
        base.columns = [str(c).strip() for c in base.columns]

    if drop_duplicated_columns:
        base = base.loc[:, ~base.columns.duplicated(keep=keep)]

    return base


def rename_merge_aliases(df: pd.DataFrame, *, aliases: Mapping[str, str]) -> pd.DataFrame:
    """
    Renomeia/une colunas equivalentes (aliases) para um padrão único.

    Regras:
    - Se origem existe e destino não: renomeia origem -> destino.
    - Se ambos existem: destino = destino.combine_first(origem) e remove origem.
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
    df_before: pd.DataFrame,
    df_after: pd.DataFrame,
    *,
    aliases: Mapping[str, str],
) -> list[str]:
    """
    Valida que a união de aliases não perdeu informação.

    Para cada origem->destino:
    - se origem tinha valor e destino era NaN em df_before,
      então destino deve estar preenchido em df_after.
    """
    inconsistencias: list[str] = []
    if not aliases:
        return inconsistencias

    for origem, destino in aliases.items():
        if origem not in df_before.columns:
            continue

        origem_notna = df_before[origem].notna()
        if not origem_notna.any():
            continue

        destino_antes = (
            df_before[destino]
            if destino in df_before.columns
            else pd.Series(np.nan, index=df_before.index)
        )

        precisa_transferir = origem_notna & destino_antes.isna()

        if destino not in df_after.columns:
            inconsistencias.append(
                f"Destino ausente após aliases: '{destino}' (origem: '{origem}')"
            )
            continue

        destino_depois = df_after[destino]
        faltantes = int((precisa_transferir & destino_depois.isna()).sum())
        if faltantes > 0:
            inconsistencias.append(
                f"Falha na transferência {origem} -> {destino}: {faltantes} linhas não preenchidas."
            )

    return inconsistencias


def normalize_missing_values(
    df: pd.DataFrame,
    *,
    na_like: Mapping[Any, Any] | None = None,
) -> pd.DataFrame:
    """
    Padroniza ausentes (pd.NA -> np.nan) e aplica substituições definidas em na_like.
    """
    base = df.replace({pd.NA: np.nan})
    if na_like:
        base = base.replace(na_like)
    return base


def coerce_numeric_columns(
    df: pd.DataFrame,
    *,
    numeric_cols: Sequence[str],
) -> pd.DataFrame:
    """Converte colunas listadas para numérico (errors='coerce')."""
    base = df.copy()
    for col in numeric_cols:
        if col in base.columns:
            base[col] = pd.to_numeric(base[col], errors="coerce")
    return base


def remove_accents(text: str) -> str:
    """Remove acentos de uma string usando unicode normalization."""
    if text is None:
        return text
    return "".join(
        c for c in unicodedata.normalize("NFD", text)
        if unicodedata.category(c) != "Mn"
    )


def normalize_categorical_columns(
    df: pd.DataFrame,
    *,
    cat_cols: Sequence[str],
    lower: bool = True,
    remove_accents_flag: bool = True,
    collapse_whitespace: bool = True,
) -> pd.DataFrame:
    """
    Normaliza valores em colunas categóricas.

    Por padrão:
    - strip()
    - lower()
    - remove acentos
    - colapsa espaços internos duplicados
    """
    base = df.copy()

    def _norm(v: Any) -> Any:
        if pd.isna(v):
            return np.nan

        s = str(v).strip()

        if lower:
            s = s.lower()

        if remove_accents_flag:
            s = remove_accents(s)

        if collapse_whitespace:
            s = " ".join(s.split())

        return s

    for col in cat_cols:
        if col in base.columns:
            base[col] = base[col].map(_norm)

    return base


def apply_categorical_value_map(
    df: pd.DataFrame,
    *,
    value_map: Mapping[str, Mapping[str, str]],
) -> pd.DataFrame:
    """
    Aplica canonização/mapeamento de valores categóricos por coluna.

    Exemplo:
    value_map = {
        "genero": {"m": "masculino", "f": "feminino"},
        "ativo/ inativo": {"ativo(a)": "ativo"},
    }

    Observação:
    - É recomendado que o DataFrame já esteja normalizado (lower/sem acento),
      e que o value_map use as chaves já normalizadas.
    """
    if not value_map:
        return df.copy()

    base = df.copy()
    for col, mapping in value_map.items():
        if col not in base.columns:
            continue

        def _map_value(v: Any) -> Any:
            if pd.isna(v):
                return np.nan
            return mapping.get(v, v)

        base[col] = base[col].map(_map_value)

    return base


def validate_categorical_allowed_values(
    df: pd.DataFrame,
    *,
    allowed: Mapping[str, Sequence[str]],
    strict: bool = True,
) -> None:
    """
    Valida se colunas categóricas possuem apenas valores permitidos.

    Se strict=True, levanta ValueError listando:
    - coluna
    - valores inesperados
    - valores permitidos
    """
    if not allowed:
        return

    errors: list[str] = []

    for col, allowed_values in allowed.items():
        if col not in df.columns:
            continue

        allowed_set = set(allowed_values)
        observed = set(df[col].dropna().unique().tolist())
        unexpected = sorted([v for v in observed if v not in allowed_set])

        if unexpected:
            errors.append(
                f"Coluna '{col}' possui valores inesperados: {unexpected}. "
                f"Permitidos: {sorted(allowed_set)}"
            )

    if errors and strict:
        raise ValueError("Validação de categóricas falhou:\n- " + "\n- ".join(errors))


def validate_required_columns(df: pd.DataFrame, *, required: Sequence[str]) -> None:
    """Falha com ValueError se alguma coluna obrigatória estiver ausente."""
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
    """
    Remove linhas duplicadas com base em uma chave (subset).
    Se subset foi informado e faltar alguma coluna, levanta ValueError com mensagem clara.
    """
    if not subset:
        return df.copy()

    base = df.copy()
    missing = [c for c in subset if c not in base.columns]
    if missing:
        raise ValueError(
            f"Não dá para deduplicar: colunas ausentes {missing}. "
            f"Subset={list(subset)} Colunas atuais={list(base.columns)}"
        )

    return base.drop_duplicates(subset=list(subset), keep=keep)


def reorder_columns(df: pd.DataFrame, *, ordered_cols: Sequence[str]) -> pd.DataFrame:
    """Reordena colunas: as conhecidas primeiro na ordem desejada, e o restante ao final."""
    if not ordered_cols:
        return df.copy()

    base = df.copy()
    existing = [c for c in ordered_cols if c in base.columns]
    remaining = [c for c in base.columns if c not in existing]
    return base[existing + remaining].copy()


# =============================================================================
# Pipeline
# =============================================================================

def preprocess(
    df: pd.DataFrame,
    *,
    config: PreprocessConfig,
    validate_aliases: bool = True,
) -> pd.DataFrame:
    """
    Executa o preprocessamento com base no PreprocessConfig.

    Ordem:
    1) Padroniza nomes de colunas
    2) Normaliza ausentes
    3) Aplica aliases (unifica colunas)
    4) (Opcional) valida transferência de aliases
    5) Dedup de linhas (se configurado)
    6) Converte numéricos
    7) Normaliza categóricas (minúsculo/sem acento por padrão)
    8) Aplica mapeamento/canonização de categóricas por coluna (opcional)
    9) Valida valores categóricos finais (opcional)
    10) Valida colunas obrigatórias
    11) Reordena colunas para saída
    """
    base = standardize_columns(
        df,
        remove_excel_suffixes=True,
        drop_duplicated_columns=True,
        keep=config.drop_duplicate_columns_keep,
    )

    base = normalize_missing_values(base, na_like=config.na_like)

    base_aliased = rename_merge_aliases(base, aliases=config.aliases_colunas)

    if validate_aliases:
        inconsist = validate_alias_transfer(base, base_aliased, aliases=config.aliases_colunas)
        if inconsist:
            raise ValueError(f"Inconsistências de transferência de aliases: {inconsist}")

    base_aliased = drop_duplicate_rows(base_aliased, subset=config.dedup_subset_rows, keep="first")

    base_aliased = coerce_numeric_columns(base_aliased, numeric_cols=config.colunas_numericas)

    base_aliased = normalize_categorical_columns(
        base_aliased,
        cat_cols=config.colunas_categoricas,
        lower=config.categorical_lower,
        remove_accents_flag=config.categorical_remove_accents,
        collapse_whitespace=config.categorical_collapse_whitespace,
    )

    # Canonização de valores categóricos (opcional)
    base_aliased = apply_categorical_value_map(
        base_aliased,
        value_map=config.categorical_value_map,
    )

    # Validação de domínio/contrato (opcional)
    validate_categorical_allowed_values(
        base_aliased,
        allowed=config.categorical_allowed_values,
        strict=config.categorical_validate_strict,
    )

    validate_required_columns(base_aliased, required=config.required_columns)

    base_aliased = reorder_columns(base_aliased, ordered_cols=config.colunas_saida_ordenada)

    return base_aliased