import re

import numpy as np
import pandas as pd


# Mapa de renomeação para unificar colunas equivalentes entre anos/abas.
# Uso: aplicado em `renomear_colunas_equivalentes`.
ALIASES_COLUNAS = {
    "Matem": "Mat",
    "Portug": "Por",
    "Inglês": "Ing",
    "Fase ideal": "Fase Ideal",
    "Defas": "Defasagem",
    "Nome Anonimizado": "Nome",
    "INDE 23": "INDE 2023",
    "INDE 22": "INDE 2022",
    "Pedra 23": "Pedra 2023",
    "Pedra 20": "Pedra 2020",
    "Pedra 21": "Pedra 2021",
    "Pedra 22": "Pedra 2022",
    
}

# Lista de colunas que devem ser convertidas para tipo numérico.
# Uso: aplicada em `ajustar_tipos_numericos` com `pd.to_numeric(..., errors="coerce")`.
COLUNAS_NUMERICAS = [
    "Idade",
    "Idade 22",
    "Ano nasc",
    "Ano ingresso",
    "Nº Av",
    "INDE 22",
    "INDE 23",
    "INDE 2022",
    "INDE 2023",
    "INDE 2024",
    "IAA",
    "IEG",
    "IPS",
    "IPP",
    "IDA",
    "IPV",
    "IAN",
    "Mat",
    "Por",
    "Ing",
    "Defasagem",
]

# Lista de colunas categóricas/textuais para padronização de string.
# Uso: aplicada em `normalizar_colunas_categoricas` (trim e manutenção de nulos).
COLUNAS_CATEGORICAS = [
    "Fase",
    "Turma",
    "Gênero",
    "Instituição de ensino",
    "Fase Ideal",
    "Pedra 2020",
    "Pedra 2021",
    "Pedra 2022",
    "Pedra 2023",
    "Pedra 2024",
    "PEDRA_ATUAL",
    "Indicado",
    "Atingiu PV",
    "Ativo/ Inativo",
]

# Ordem final desejada das colunas no dataset preprocessado.
# Uso: aplicada em `organizar_colunas_para_saida`; colunas inexistentes são ignoradas.
COLUNAS_SAIDA_ORDENADA = [
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
    "INDE 2020",
    "INDE 2021",
    "INDE 2022",
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
    "Avaliador1",
    "Avaliador2",
    "Avaliador3",
    "Avaliador4",
    "Avaliador5",
]


def remover_sufixo_duplicado_excel(nome_coluna: str) -> str:
    """
    Remove sufixos `.1`, `.2`, etc. criados automaticamente pelo pandas.

    Isso evita que a mesma coluna apareça com variações de nome após leitura
    de planilhas com cabeçalhos repetidos.
    """
    return re.sub(r"\.\d+$", "", nome_coluna).strip()


def padronizar_nomes_e_remover_duplicadas(df: pd.DataFrame) -> pd.DataFrame:
    """
    Padroniza nomes de colunas e mantém apenas a primeira ocorrência de duplicatas.

    Regras aplicadas:
    1. Remove sufixos de duplicidade (`.1`, `.2`, ...).
    2. Remove espaços extras no começo/fim.
    3. Elimina colunas duplicadas pelo nome.
    """
    base = df.copy()
    base.columns = [remover_sufixo_duplicado_excel(col) for col in base.columns]
    base.columns = [col.strip() for col in base.columns]
    base = base.loc[:, ~base.columns.duplicated(keep="first")]
    return base


def renomear_colunas_equivalentes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Renomeia/une colunas equivalentes para um padrão único.

    Regras:
    - Se a coluna de origem existe e a de destino não existe, renomeia origem -> destino.
    - Se origem e destino existem, mantém valores já preenchidos em destino,
      completa nulos de destino com origem (`combine_first`) e remove origem.
    - Se origem não existe, não faz alteração.

    Exemplos:
    - `Matem` -> `Mat`
    - `Portug` -> `Por`
    """
    base = df.copy()
    for origem, destino in ALIASES_COLUNAS.items():
        if origem not in base.columns:
            continue
        if destino in base.columns:
            base[destino] = base[destino].combine_first(base[origem])
            base = base.drop(columns=[origem])
        else:
            base = base.rename(columns={origem: destino})
    return base


def validar_transferencia_colunas_equivalentes(
    df_original: pd.DataFrame, df_renomeado: pd.DataFrame
) -> list[str]:
    """
    Valida se valores de colunas de alias foram transferidos para o destino sem perda.

    Retorna uma lista de mensagens de erro. Lista vazia = sem inconsistências.
    """
    inconsistencias: list[str] = []
    for origem, destino in ALIASES_COLUNAS.items():
        if origem not in df_original.columns:
            continue

        origem_notna = df_original[origem].notna()
        if not origem_notna.any():
            continue

        destino_antes = (
            df_original[destino] if destino in df_original.columns else pd.Series(np.nan, index=df_original.index)
        )
        precisa_transferir = origem_notna & destino_antes.isna()

        if destino not in df_renomeado.columns:
            inconsistencias.append(
                f"Destino ausente apos renomeacao: '{destino}' (origem: '{origem}')"
            )
            continue

        destino_depois = df_renomeado[destino]
        faltantes = int((precisa_transferir & destino_depois.isna()).sum())
        if faltantes > 0:
            inconsistencias.append(
                f"Falha de transferencia {origem} -> {destino}: {faltantes} linhas nao preenchidas."
            )

        if inconsistencias:
            raise ValueError(f"Inconsistencias de transferencia de aliases em : {inconsistencias}")

    return inconsistencias


def ajustar_tipos_numericos(df: pd.DataFrame) -> pd.DataFrame:
    """
    Converte para numérico as colunas conhecidas como numéricas.

    Valores inválidos são convertidos para `NaN` com `errors='coerce'`.
    """
    base = df.copy()
    for coluna in COLUNAS_NUMERICAS:
        if coluna in base.columns:
            base[coluna] = pd.to_numeric(base[coluna], errors="coerce")
    return base


def normalizar_colunas_categoricas(df: pd.DataFrame) -> pd.DataFrame:
    """
    Converte colunas categóricas para string padronizada.

    - Remove espaços extras.
    - Mantém nulos como `np.nan`.
    """
    base = df.copy()
    for coluna in COLUNAS_CATEGORICAS:
        if coluna in base.columns:
            base[coluna] = base[coluna].apply(
                lambda valor: str(valor).strip() if pd.notna(valor) else np.nan
            )
    return base


def normalizar_valores_ausentes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Padroniza valores ausentes para `np.nan`.
    """
    return df.replace({pd.NA: np.nan})


def organizar_colunas_para_saida(df: pd.DataFrame) -> pd.DataFrame:
    """
    Reordena o DataFrame para o conjunto de colunas esperado na saída.

    Mantém todas as colunas:
    - Colunas conhecidas vêm primeiro, na ordem definida.
    - Colunas não mapeadas são anexadas ao final.
    """
    colunas_existentes = [col for col in COLUNAS_SAIDA_ORDENADA if col in df.columns]
    colunas_restantes = [col for col in df.columns if col not in colunas_existentes]
    return df[colunas_existentes + colunas_restantes].copy()


def executar_preprocessamento(df: pd.DataFrame) -> pd.DataFrame:
    """
    Executa o preprocessing em sequência para uso no `main`.

    Ordem aplicada:
    1. `padronizar_nomes_e_remover_duplicadas`
    2. `renomear_colunas_equivalentes`
    3. `ajustar_tipos_numericos`
    4. `normalizar_colunas_categoricas`
    5. `normalizar_valores_ausentes`
    6. `organizar_colunas_para_saida`
    """
    base = padronizar_nomes_e_remover_duplicadas(df)
    base = renomear_colunas_equivalentes(base)
    base = ajustar_tipos_numericos(base)
    base = normalizar_colunas_categoricas(base)
    base = normalizar_valores_ausentes(base)
    base = organizar_colunas_para_saida(base)
    return base
