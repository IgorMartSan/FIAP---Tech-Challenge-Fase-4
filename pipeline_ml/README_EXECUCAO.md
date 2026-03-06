# Como executar a pipeline (dev) e os testes

Este documento explica como rodar o `dev_pipeline.py`, executar os testes e dá uma visão rápida do projeto.

## Visão geral do projeto

Este repositório contém uma pipeline de ML para prever risco de defasagem escolar. As etapas principais são:
- **Preprocessamento**: limpeza, padronização e validação de colunas.
- **Feature engineering**: construção do dataset de modelagem (ano A -> ano A+1).
- **Treino**: treinamento do modelo (LightGBM) e persistência do artefato.
- **Avaliação**: cálculo de métricas e relatório textual.

Fluxo esperado:
`aa_preprocessing` -> `ba_feature_engineering` -> `ca_train` -> `da_evaluate`

## Pré‑requisitos

- Python 3.10+
- `uv` (recomendado) ou `pip`

Instalação de dependências:
```bash
uv sync
```

## Executar o dev pipeline

1. Ajuste o caminho do Excel no `dev_pipeline.py`:
```python
PATH = "/caminho/para/BASE DE DADOS PEDE 2024 - DATATHON.xlsx"
```

2. Rode o pipeline:
```bash
python3 dev_pipeline.py
```

Principais saídas:
- `data/bruto/*.csv`
- `data/processed/*.csv`
- `data/model/pede_dataset_model_all_years.csv`
- `data/model/model_defasagem_fc_binario_lgbm.joblib`
- `data/model/evaluation_report.txt`

## Executar os testes

Com `uv`:
```bash
uv run pytest
```

Com cobertura:
```bash
uv run pytest --cov=. --cov-report=term-missing
```

Observação: `train.py` e `dev_pipeline.py` são ignorados na cobertura.
