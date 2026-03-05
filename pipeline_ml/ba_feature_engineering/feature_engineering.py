from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping, Sequence, Any, Optional

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class SingleYearToNextYearConfig:
    """
    Configuração para montar um dataset de modelagem do tipo:

        (features do ano A)  ->  (target do ano A+1)

    Você define explicitamente:
    - quais colunas saem no dataset final (output_schema)
    - de onde vem cada coluna (feature_map e target_map)
    - qual é a chave de merge (id_col)

    O objetivo é garantir um "contrato" rígido:
    - O CSV final sempre terá as colunas definidas em `output_schema`.
    - Se alguma coluna não puder ser preenchida, falha com erro claro
      (ou, opcionalmente, preenche com NaN).
    """

    # chave única do aluno
    id_col: str = "RA"

    # colunas finais (ordem do CSV final)
    output_schema: Sequence[str] = field(default_factory=tuple)

    # Mapeamento: coluna_final -> coluna_origem_no_df_features
    # Ex.: {"mat": "Mat", "por": "Por", "pedra": "Pedra 2023"}
    feature_map: Mapping[str, str] = field(default_factory=dict)

    # Mapeamento: coluna_final -> coluna_origem_no_df_target
    # Ex.: {"target__inde": "INDE 2024"}
    target_map: Mapping[str, str] = field(default_factory=dict)

    # Se True, exige que todas as colunas do schema sejam preenchidas (exceto id).
    # Se False, colunas ausentes viram NaN.
    strict_schema: bool = True

    # Como fazer merge entre features e target:
    # - "inner" mantém só alunos presentes em ambos
    # - "left" mantém todos de features e target pode virar NaN
    join_how: str = "inner"


class SingleYearToNextYearBuilder:
    """
    Builder para montar dataset tabular simples:
    features (ano A) + target (ano A+1) via merge por id_col.

    Ele também aplica um "schema fixo" para o CSV final.
    """

    def __init__(self, config: SingleYearToNextYearConfig):
        self.config = config

    def _ensure_id(self, df: pd.DataFrame, df_name: str) -> None:
        if self.config.id_col not in df.columns:
            raise ValueError(
                f"[{df_name}] Coluna id '{self.config.id_col}' não existe. "
                f"Colunas disponíveis: {list(df.columns)}"
            )

    def _dedup_by_id(self, df: pd.DataFrame, df_name: str) -> pd.DataFrame:
        """
        Garante 1 linha por id.
        Se houver duplicatas, mantém a primeira (regra simples e testável).
        """
        self._ensure_id(df, df_name)
        return df.drop_duplicates(subset=[self.config.id_col], keep="first").copy()

    def _build_side(
        self,
        df: pd.DataFrame,
        mapping: Mapping[str, str],
        df_name: str,
    ) -> pd.DataFrame:
        """
        Seleciona colunas do df e renomeia para o nome final.

        Retorna um DF com:
          [id_col] + colunas finais definidas no mapping
        """
        base = self._dedup_by_id(df, df_name)

        # valida colunas de origem
        missing_src = [src for src in mapping.values() if src not in base.columns]
        if missing_src and self.config.strict_schema:
            raise ValueError(
                f"[{df_name}] Colunas de origem ausentes: {missing_src}. "
                f"Colunas disponíveis: {list(base.columns)}"
            )

        out = base[[self.config.id_col]].copy()

        # cria cada coluna final
        for out_col, src_col in mapping.items():
            if src_col in base.columns:
                out[out_col] = base[src_col]
            else:
                out[out_col] = np.nan  # se strict_schema=False isso permite seguir

        return out

    def _validate_output_schema(self, df_final: pd.DataFrame) -> pd.DataFrame:
        """
        Garante que o DF final tem exatamente o schema e na ordem do schema.
        """
        if not self.config.output_schema:
            raise ValueError("output_schema está vazio. Defina as colunas finais do CSV.")

        # id_col precisa estar no schema
        if self.config.id_col not in self.config.output_schema:
            raise ValueError(
                f"id_col '{self.config.id_col}' deve estar dentro de output_schema."
            )

        # cria colunas faltantes (se strict_schema=False) ou falha (se True)
        missing_out = [c for c in self.config.output_schema if c not in df_final.columns]
        if missing_out:
            if self.config.strict_schema:
                raise ValueError(
                    f"Schema final incompleto. Faltando colunas: {missing_out}. "
                    f"Colunas presentes: {list(df_final.columns)}"
                )
            for c in missing_out:
                df_final[c] = np.nan

        # remove colunas extras (mantém só as do schema)
        df_final = df_final[list(self.config.output_schema)].copy()

        return df_final

    def build(self, df_features: pd.DataFrame, df_target: pd.DataFrame) -> pd.DataFrame:
        """
        Constrói o dataset final:

        1) Lê df_features e monta colunas conforme feature_map
        2) Lê df_target e monta colunas conforme target_map
        3) Faz merge por id_col
        4) Reordena/valida schema final (output_schema)

        Returns
        -------
        pd.DataFrame
            Dataset final pronto para salvar em CSV e treinar modelo.
        """
        # monta lados
        features_side = self._build_side(df_features, self.config.feature_map, "features")
        target_side = self._build_side(df_target, self.config.target_map, "target")

        # merge
        merged = features_side.merge(
            target_side,
            on=self.config.id_col,
            how=self.config.join_how,
        )

        # schema final
        merged = self._validate_output_schema(merged)

        return merged