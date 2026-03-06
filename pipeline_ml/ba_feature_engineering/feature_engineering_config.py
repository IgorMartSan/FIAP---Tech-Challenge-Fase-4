"""
Configuração do dataset de modelagem

Objetivo:
usar dados de um ano (features) para prever
o resultado do ano seguinte (target)
"""

# ---------------------------------------------------------
# Coluna identificadora
# ---------------------------------------------------------

ID_COL = "RA"


# ---------------------------------------------------------
# Colunas finais do dataset (ordem do CSV final)
# ---------------------------------------------------------

OUTPUT_SCHEMA = (
    "RA",
    "Mat",
    "Por",
    #"Ing",
    "Pedra_0",
    "Pedra_1",
    "Pedra_2",
    "INDE",
    "IAA",
    "IEG",
    "IPS",
    "IDA",
    "IPV",
    "IAN",
    # "Atingiu PV",
    "Defasagem",
    "Defasagem futura",
)


# ---------------------------------------------------------
# Mapeamento das features
# coluna_saida (FC) <- coluna_origem_no_csv
# ---------------------------------------------------------

FEATURE_MAP_2022 = {
    "Mat": "Mat",
    "Por": "Por",
    #"Ing": "Ing",

    "Pedra_0": "Pedra 2020",
    "Pedra_1": "Pedra 2021",
    "Pedra_2": "Pedra 2022",
    "INDE": "INDE 2022",
    "IAA": "IAA",
    "IEG": "IEG",
    "IPS": "IPS",
    "IDA": "IDA",
    "IPV": "IPV",
    "IAN": "IAN",
    #"Atingiu PV": "Atingiu PV",
    "Defasagem": "Defasagem",

}

FEATURE_MAP_2023 = {
    "Mat": "Mat",
    "Por": "Por",
    #"Ing": "Ing",
    "Pedra_0": "Pedra 2021",
    "Pedra_1": "Pedra 2022",
    "Pedra_2": "Pedra 2023",
    "INDE": "INDE 2023",
    "IAA": "IAA",
    "IEG": "IEG",
    "IPS": "IPS",
    "IDA": "IDA",
    "IPV": "IPV",
    "IAN": "IAN",
    #"Atingiu PV": "Atingiu PV",
    "Defasagem": "Defasagem",


}


FEATURE_MAP_2024 = {
    "Mat": "Mat",
    "Por": "Por",
    #"Ing": "Ing",
    "Pedra_0": "Pedra 2022",
    "Pedra_1": "Pedra 2023",
    "Pedra_2": "Pedra 2024",
    "INDE": "INDE 2024",
    "IAA": "IAA",
    "IEG": "IEG",
    "IPS": "IPS",
    "IDA": "IDA",
    "IPV": "IPV",
    "IAN": "IAN",
    # "Atingiu PV": "Atingiu PV",
    "Defasagem": "Defasagem",


}


# ---------------------------------------------------------
# Mapeamento do target
# coluna_saida (FC) <- coluna_origem_no_csv
# ---------------------------------------------------------

TARGET_MAP = {
    "Defasagem futura": "Defasagem",
}


# ---------------------------------------------------------
# Configuração do join
# ---------------------------------------------------------

JOIN_TYPE = "inner"


# ---------------------------------------------------------
# Se True → erro se faltar coluna
# Se False → preenche com NaN
# ---------------------------------------------------------

STRICT_SCHEMA = True