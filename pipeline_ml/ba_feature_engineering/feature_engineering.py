import re
from typing import Any

import numpy as np
import pandas as pd


COLUNAS_INDICADORES = ["IAA", "IEG", "IPS", "IPP", "IDA", "IPV", "IAN"]
COLUNAS_MATERIAS = ["Mat", "Por", "Ing"]
COLUNAS_AVALIADORES = [
    "Avaliador1",
    "Avaliador2",
    "Avaliador3",
    "Avaliador4",
    "Avaliador5",
    "Avaliador6",
]
COLUNAS_RECOMENDACOES = ["Rec Av1", "Rec Av2", "Rec Av3", "Rec Av4", "Rec Psicologia"]
COLUNAS_DERIVADAS = [
    "DERIV_ANO_REFERENCIA",
    "DERIV_ANOS_NO_PROGRAMA",
    "DERIV_FASE_NUMERICA",
    "DERIV_MEDIA_NOTAS",
    "DERIV_DESVIO_NOTAS",
    "DERIV_MEDIA_INDICADORES",
    "DERIV_QTD_AVALIADORES_PREENCHIDOS",
    "DERIV_QTD_RECOMENDACOES_PREENCHIDAS",
    "DERIV_INDE_ATUAL",
    "DERIV_PEDRA_ATUAL",
]

COLUNAS_SAIDA_ORDENADA_FE = [
    "RA",
    "Nome",
    "Gênero",
    "Turma",
    "Escola",
    "Instituição de ensino",
    "Ativo/ Inativo",
    "Ano ingresso",

    "Fase",
    "Fase Ideal",
    "Defasagem",
    "Pedra 2020",
    "Pedra 2021",
    "Pedra 2022",
    "Pedra 2023",
    "Pedra 2024",
    "INDE 22",
    "INDE 23",
    "INDE 2023",
    "INDE 2024",
    "Mat",
    "Por",
    "Ing",
    "IAA",
    "IEG",
    "IPS",
    "IPP",
    "IDA",
    "IPV",
    "IAN",

    "Nº Av",
    "Indicado",
    "Atingiu PV",
    "DERIV_*",

]


def converter_fase_para_numerico(valor_fase: Any) -> float:
    """
    Converte a fase textual (`ALFA`, `1A`, `1B`, etc.) para escala numérica.
    """
    if pd.isna(valor_fase):
        return np.nan

    texto = str(valor_fase).strip().upper()
    if texto == "ALFA":
        return 0.0

    match = re.match(r"^(\d+)\s*([A-Z])?$", texto)
    if not match:
        return np.nan

    numero = int(match.group(1))
    letra = match.group(2)
    deslocamento_letra = 0.0 if not letra else (ord(letra) - ord("A")) / 10.0
    return numero + deslocamento_letra


def unificar_alvos_do_ano(df: pd.DataFrame, ano_referencia: int) -> pd.DataFrame:
    """
    Unifica as colunas de INDE e Pedra do ano de referência em colunas únicas.

    Saída:
    - `DERIV_INDE_ATUAL`
    - `DERIV_PEDRA_ATUAL`
    """
    base = df.copy()
    mapa_inde = {
        2022: ["INDE 22"],
        2023: ["INDE 2023", "INDE 23"],
        2024: ["INDE 2024"],
    }
    mapa_pedra = {
        2022: ["Pedra 2022"],
        2023: ["Pedra 2023", "Pedra 23"],
        2024: ["Pedra 2024"],
    }

    base["DERIV_INDE_ATUAL"] = np.nan
    base["DERIV_PEDRA_ATUAL"] = np.nan

    for coluna in mapa_inde.get(ano_referencia, []):
        if coluna in base.columns:
            base["DERIV_INDE_ATUAL"] = base[coluna]
            break

    for coluna in mapa_pedra.get(ano_referencia, []):
        if coluna in base.columns:
            base["DERIV_PEDRA_ATUAL"] = base[coluna]
            break

    return base


def gerar_atributos_derivados(df: pd.DataFrame, ano_referencia: int) -> pd.DataFrame:
    """
    Gera atributos derivados usados no treino e na análise.

    Atributos gerados:
    - `DERIV_ANO_REFERENCIA`
    - `DERIV_ANOS_NO_PROGRAMA`
    - `DERIV_FASE_NUMERICA`
    - `DERIV_MEDIA_NOTAS`
    - `DERIV_DESVIO_NOTAS`
    - `DERIV_MEDIA_INDICADORES`
    - `DERIV_QTD_AVALIADORES_PREENCHIDOS`
    - `DERIV_QTD_RECOMENDACOES_PREENCHIDAS`
    """
    base = df.copy()
    base["DERIV_ANO_REFERENCIA"] = ano_referencia

    if "Ano ingresso" in base.columns:
        base["DERIV_ANOS_NO_PROGRAMA"] = ano_referencia - base["Ano ingresso"]
    else:
        base["DERIV_ANOS_NO_PROGRAMA"] = np.nan

    if "Fase" in base.columns:
        base["DERIV_FASE_NUMERICA"] = base["Fase"].apply(converter_fase_para_numerico)
    else:
        base["DERIV_FASE_NUMERICA"] = np.nan

    colunas_materias_existentes = [c for c in COLUNAS_MATERIAS if c in base.columns]
    if colunas_materias_existentes:
        base["DERIV_MEDIA_NOTAS"] = base[colunas_materias_existentes].mean(axis=1)
        base["DERIV_DESVIO_NOTAS"] = base[colunas_materias_existentes].std(axis=1)
    else:
        base["DERIV_MEDIA_NOTAS"] = np.nan
        base["DERIV_DESVIO_NOTAS"] = np.nan

    colunas_indicadores_existentes = [c for c in COLUNAS_INDICADORES if c in base.columns]
    if colunas_indicadores_existentes:
        base["DERIV_MEDIA_INDICADORES"] = base[colunas_indicadores_existentes].mean(axis=1)
    else:
        base["DERIV_MEDIA_INDICADORES"] = np.nan

    colunas_avaliadores_existentes = [c for c in COLUNAS_AVALIADORES if c in base.columns]
    colunas_recomendacoes_existentes = [c for c in COLUNAS_RECOMENDACOES if c in base.columns]

    if colunas_avaliadores_existentes:
        base["DERIV_QTD_AVALIADORES_PREENCHIDOS"] = base[colunas_avaliadores_existentes].notna().sum(axis=1)
    else:
        base["DERIV_QTD_AVALIADORES_PREENCHIDOS"] = 0

    if colunas_recomendacoes_existentes:
        base["DERIV_QTD_RECOMENDACOES_PREENCHIDAS"] = base[colunas_recomendacoes_existentes].notna().sum(axis=1)
    else:
        base["DERIV_QTD_RECOMENDACOES_PREENCHIDAS"] = 0

    return base


def organizar_colunas_saida_feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
    """
    Reorganiza as colunas finais na ordem lógica de saída do feature engineering.

    Mantém todas as colunas:
    - Colunas conhecidas vêm primeiro, na ordem definida.
    - O marcador `DERIV_*` em `COLUNAS_SAIDA_ORDENADA_FE` expande para
      todas as colunas derivadas existentes.
    - Colunas não mapeadas são anexadas ao final.
    """
    colunas_derivadas = [col for col in COLUNAS_DERIVADAS if col in df.columns]
    colunas_derivadas_extras = [
        col for col in df.columns if col.startswith("DERIV_") and col not in colunas_derivadas
    ]
    todas_colunas_derivadas = colunas_derivadas + colunas_derivadas_extras

    colunas_ordenadas: list[str] = []
    for coluna in COLUNAS_SAIDA_ORDENADA_FE:
        if coluna == "DERIV_*":
            colunas_ordenadas.extend(
                [col for col in todas_colunas_derivadas if col not in colunas_ordenadas]
            )
            continue
        if coluna in df.columns and coluna not in colunas_ordenadas:
            colunas_ordenadas.append(coluna)

    colunas_restantes = [col for col in df.columns if col not in colunas_ordenadas]
    return df[colunas_ordenadas + colunas_restantes].copy()
