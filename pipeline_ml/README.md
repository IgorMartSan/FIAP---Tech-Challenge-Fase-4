# Pipeline ML

Este diretório concentra as etapas do pipeline de Machine Learning do projeto.

## Estrutura de pastas

- `1_preprocessing/`
  - Responsável pela limpeza e padronização dos dados brutos.
  - Exemplos: tratamento de nulos, ajuste de tipos, normalização de campos e organização do dataset para etapas seguintes.
  - Arquivo inicial criado: `1_preprocessing/load_data.py` para carregar a base Excel do projeto.

- `2_feature_engineering/`
  - Responsável pela criação e transformação de variáveis (features).
  - Exemplos: geração de atributos derivados, codificação de categorias, seleção/redução de variáveis e preparação da matriz de treino.

- `3_train/`
  - Responsável pelo treinamento dos modelos.
  - Exemplos: separação treino/validação, ajuste de hiperparâmetros, treinamento final e salvamento do artefato do modelo.

- `4_evaluate/`
  - Responsável pela avaliação de desempenho dos modelos treinados.
  - Exemplos: cálculo de métricas, análise de erros, comparação entre modelos e geração de relatórios de performance.

- `utils/`
  - Contém utilitários compartilhados entre as etapas do pipeline.
  - Exemplos: funções auxiliares, leitura/escrita de arquivos, configurações comuns e logging.

## Fluxo esperado

`1_preprocessing` -> `2_feature_engineering` -> `3_train` -> `4_evaluate`

As funções utilitárias em `utils` podem ser reutilizadas por todas as etapas.

## Carregamento inicial de dados (1_preprocessing)

Script:

- `pipeline_ml/1_preprocessing/load_data.py`

Função principal:

- `load_raw_data(file_path: Optional[str] = None, sheet_name: Optional[str] = None) -> pd.DataFrame`

Uso rápido:

```bash
python3 pipeline_ml/1_preprocessing/load_data.py
```

Dependências para leitura de Excel:

```bash
pip install pandas openpyxl
```

## Notebook de desenvolvimento

Arquivo:

- `pipeline_ml/notebooks/dev_pipeline.ipynb`

Abrir no Jupyter:

```bash
jupyter notebook pipeline_ml/notebooks/dev_pipeline.ipynb
```
