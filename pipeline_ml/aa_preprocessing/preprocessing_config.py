# =============================================================================
# aa_preprocessing/preprocessing_config.py
# =============================================================================

# -------------------------------------------------------------------
# ALIASES DE COLUNAS
# -------------------------------------------------------------------
# Mapeamento para padronizar nomes de colunas que aparecem com variações
# entre diferentes anos ou abas do Excel.
#
# Regras do preprocess:
# - Se a coluna origem existir e a destino não existir → renomeia.
# - Se ambas existirem → destino recebe valores faltantes da origem.
#
# Exemplo:
# "Matem" -> "Mat"
# "Portug" -> "Por"
# "INDE 23" -> "INDE 2023"
ALIASES_COLUNAS = {
    "Matem": "Mat",
    "Portug": "Por",
    "Inglês": "Ing",
    "Defas": "Defasagem",
    "Nome Anonimizado": "Nome",

    # padroniza variações de fase ideal
    "Fase ideal": "Fase Ideal",

    # INDE por ano
    "INDE 22": "INDE 2022",
    "INDE 23": "INDE 2023",
    "INDE 24": "INDE 2024",

    # Pedra por ano
    "Pedra 20": "Pedra 2020",
    "Pedra 21": "Pedra 2021",
    "Pedra 22": "Pedra 2022",
    "Pedra 23": "Pedra 2023",
}


# -------------------------------------------------------------------
# COLUNAS NUMÉRICAS
# -------------------------------------------------------------------
# Colunas convertidas com:
# pd.to_numeric(coluna, errors="coerce")
COLUNAS_NUMERICAS = [
    "Idade",
    "Ano nasc",
    "Ano ingresso",
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


# -------------------------------------------------------------------
# COLUNAS CATEGÓRICAS
# -------------------------------------------------------------------
# Nessas colunas o preprocess aplica:
# - strip()
# - lower() (se habilitado)
# - remove acentos (se habilitado)
# - colapsa espaços (se habilitado)
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

    "Indicado",
    "Atingiu PV",
    "Ativo/ Inativo",

    "Destaque IDA",
    "Destaque IEG",
    "Destaque IPV",

    "Rec Psicologia",
    "Rec Av4",
    "Rec Av3",
    "Rec Av2",
    "Rec Av1",
]


# -------------------------------------------------------------------
# CANONIZAÇÃO DE VALORES CATEGÓRICOS (opcional, mas recomendado)
# -------------------------------------------------------------------
# IMPORTANTE:
# Como seu preprocess normaliza para (lower + sem acento),
# as CHAVES e VALORES aqui devem estar nesse formato.
#
# Ex.: "Masculino" -> vira "masculino"
# Ex.: "Não" -> vira "nao"
CATEGORICAL_VALUE_MAP = {
    "Pedra 2020": {
        "incluir": None,
    },
        "Pedra 2021": {
        "incluir": None,
    },
        "Pedra 2022": {
        "incluir": None,
    },
        "Pedra 2023": {
        "incluir": None,
    },
        "Pedra 2024": {
        "incluir": None,
    },



    "Gênero": {
        "m": "masculino",
        "masc": "masculino",
        "masculino": "masculino",
        "f": "feminino",
        "fem": "feminino",
        "feminino": "feminino",
        "menina": "feminino",
        "menino": "masculino",
        
    },
    "Ativo/ Inativo": {
        "ativo(a)": "ativo",
        "cursando": "ativo",
        "ativo": "ativo",
        "inativo(a)": "inativo",
        "inativo": "inativo",
    },
    "Indicado": {
        "s": "sim",
        "sim": "sim",
        "n": "nao",
        "nao": "nao",
    },
    "Atingiu PV": {
        "s": "sim",
        "sim": "sim",
        "n": "nao",
        "nao": "nao",
    },
}


# -------------------------------------------------------------------
# VALIDAÇÃO DE DOMÍNIO (allowed values) DAS CATEGÓRICAS
# -------------------------------------------------------------------
# Define o conjunto FINAL permitido por coluna.
# Se aparecer algo fora disso, o preprocess levanta erro e mostra os valores.
CATEGORICAL_ALLOWED_VALUES = {
    "Gênero": ["masculino", "feminino"],
    "Ativo/ Inativo": ["ativo", "inativo"],
    "Indicado": ["sim", "nao"],
    "Atingiu PV": ["sim", "nao"],
    "Pedra 2020": ["quartzo", "agata", "ametista", "topazio"],
    "Pedra 2021": ["quartzo", "agata", "ametista", "topazio"],
    "Pedra 2022": ["quartzo", "agata", "ametista", "topazio"],
    "Pedra 2023": ["quartzo", "agata", "ametista", "topazio"],
    "Pedra 2024": ["quartzo", "agata", "ametista", "topazio"],
    # Se você quiser, pode ir adicionando mais colunas aos poucos:
    # "Fase": [...],
    # "Fase Ideal": [...],
    # "Turma": [...],
}


# -------------------------------------------------------------------
# ORDEM FINAL DAS COLUNAS
# -------------------------------------------------------------------
# Colunas que não estiverem nessa lista permanecem no final do dataset.
COLUNAS_SAIDA_ORDENADA = [
    "RA",
    "Nome",
    "Gênero",
    "Instituição de ensino",

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

    "Pedra 2020",
    "Pedra 2021",
    "Pedra 2022",
    "Pedra 2023",
    "Pedra 2024",

    "INDE 2022",
    "INDE 2023",
    "INDE 2024",

    "Turma",
    "Ativo/ Inativo",
    "Ano ingresso",
    "Fase",
    "Fase Ideal",
    "Defasagem",
]