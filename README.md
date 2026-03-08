# FIAP - Tech Challenge Fase 4

## Checklist Macro do Projeto

### 1. Planejamento e Contexto
- [X] Definir problema de negócio e objetivo preditivo (risco de defasagem escolar)
- [X] Mapear dados disponíveis (2022, 2023, 2024) e critérios de sucesso
- [X] Definir stack e padrão de organização do projeto

### 2. Dados e Modelagem
- [X] Construir pipeline de dados (preprocessamento + engenharia de atributos)
- [X] Treinar e validar modelo com métrica justificada para produção
- [X] Serializar modelo treinado (`pickle` ou `joblib`)

### 3. Engenharia de Software e MLOps
- [X] Modularizar código em componentes reutilizáveis (`src/`, serviços, utilitários)
- [X] Implementar API de predição (`/predict`) com Flask ou FastAPI
- [X] Containerizar solução com Docker (`Dockerfile` + execução local)
- [X] Realizar deploy local ou em nuvem e garantir disponibilidade da API

### 4. Qualidade e Confiabilidade
- [ ] Implementar testes da API (funcionais/integrados)
- [ ] Implementar testes unitários da pipeline com cobertura mínima de 80%
- [ ] Configurar logs e monitoramento contínuo com acompanhamento de drift

### 5. Documentação e Entrega Final
- [ ] Documentar visão geral, solução proposta e stack tecnológica
- [ ] Documentar estrutura de pastas e instruções de execução/deploy
- [ ] Incluir exemplos de chamadas à API (input/output esperado)
- [ ] Documentar etapas do pipeline de Machine Learning
- [ ] Consolidar entregáveis: repositório GitHub, documentação, link da API e vídeo (até 5 min)

## 1. Visão Geral do Projeto

### Objetivo
O projeto visa resolver o problema de negócio de previsão do risco de defasagem escolar dos estudantes da Passos Mágicos. A defasagem escolar é medida pelo indicador "Defasagem FC" (Fase Curricular), onde valores negativos indicam defasagem (atraso no currículo). O modelo preditivo identifica alunos com risco de defasagem futura, permitindo intervenções pedagógicas proativas.

### Solução Proposta
Construção de uma pipeline completa de Machine Learning, desde o pré-processamento dos dados brutos até o deploy do modelo em produção via API. A pipeline inclui:
- Pré-processamento: limpeza, normalização e validação de dados.
- Engenharia de Features: criação de dataset tabular com features do ano atual e target do ano seguinte.
- Treinamento: modelo binário com LightGBM para classificar risco de defasagem.
- Avaliação: métricas de classificação binária (accuracy, F1, precision, recall).
- API: endpoint `/predict` para predições em tempo real.
- Containerização: Docker para portabilidade e deploy.

### Stack Tecnológica
- **Linguagem**: Python 3.10+
- **Frameworks de ML**: scikit-learn, pandas, numpy, LightGBM
- **API**: FastAPI
- **Serialização**: joblib
- **Testes**: pytest, pytest-cov
- **Empacotamento**: Docker
- **Deploy**: Local / Cloud (Heroku, AWS, GCP etc.)
- **Monitoramento**: logging (estrutura para dashboard de drift futuro)

## 2. Estrutura do Projeto

```
FIAP---Tech-Challenge-Fase-4/
├── README.md                           # Documentação principal
├── datathon_storytelling_checklist.md  # Checklist de storytelling
├── docker-compose.yml                  # Orquestração de containers
├── api/                                # API de predição
│   ├── Dockerfile
│   ├── pyproject.toml
│   ├── README.md
│   └── src/
│       ├── main.py                     # Ponto de entrada da API
│       ├── prediction_route.py         # Rota /predict
│       ├── schemas.py                  # Modelos Pydantic para input/output
│       ├── model_loader.py             # Serviço de carregamento e predição do modelo
│       ├── config/
│       │   └── logging_config.py       # Configuração de logs
│       └── model/
│           └── model_defasagem_fc_binario_lgbm.joblib  # Modelo serializado
├── pipeline_ml/                        # Pipeline de Machine Learning
│   ├── pyproject.toml
│   ├── README.md
│   ├── train.py                        # Script principal para executar pipeline
│   ├── dev_pipeline.py                 # Pipeline de desenvolvimento
│   ├── aa_preprocessing/               # Pré-processamento
│   │   ├── preprocessing.py
│   │   ├── preprocessing_config.py
│   │   └── README.md
│   ├── ba_feature_engineering/         # Engenharia de features
│   │   ├── feature_engineering.py
│   │   └── feature_engineering_config.py
│   ├── ca_train/                       # Treinamento do modelo
│   │   └── train_model.py
│   ├── da_evaluate/                    # Avaliação do modelo
│   │   └── evaluate.py
│   ├── tests/                          # Testes da pipeline
│   │   ├── conftest.py
│   │   ├── test_evaluate.py
│   │   ├── test_feature_engineering.py
│   │   ├── test_preprocessing.py
│   │   └── test_train_model.py
│   └── utils/                          # Utilitários compartilhados
│       ├── io.py
│       ├── print_utils.py
├── arquivos_do_projeto/                # Documentos e dados do projeto
│   ├── inventario_colunas_tabelas.csv
│   ├── README_ANALISE_TABELAS.md
│   └── Bases antigas/
├── data/                               # Dados (não versionados)
└── tests/                              # Testes integrados
    └── integration/
```

## 3. Instruções de Deploy

### Pré-requisitos
- Python 3.10 ou superior
- Docker e Docker Compose
- Git

### Instalação de Dependências
Para a API:
```bash
cd api
pip install -e .
```

Para a pipeline ML:
```bash
cd pipeline_ml
uv sync
```

### Comandos para Treinar, Validar e Testar o Modelo
1. **Treinar o modelo**:
   ```bash
   cd pipeline_ml
   python train.py
   ```
   Este comando executa a pipeline completa: pré-processamento, feature engineering, treinamento e avaliação.

2. **Validar o modelo** (opcional, parte do train.py):
   O script `train.py` já inclui validação cruzada e métricas no conjunto de teste.

3. **Testar o código** (ver seção abaixo).

### Deploy Local
1. **Construir e executar com Docker**:
   ```bash
   docker-compose up --build
   ```
   A API estará disponível em http://localhost:8000

2. **Acesso direto**:
   ```bash
   cd api/src
   python main.py
   ```

### Deploy em Nuvem
- **Heroku**: Use o Dockerfile para build e deploy.
- **AWS/GCP**: Use ECS/EKS ou Cloud Run com o docker-compose.yml como base.

## 4. Exemplos de Chamadas à API

### Via cURL
```bash
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{
       "RA": "RA-999",
       "Mat": 7.5,
       "Por": 6.8,
       "Pedra_0": "ametista",
       "Pedra_1": "agata",
       "Pedra_2": "quartzo",
       "INDE": 7.12,
       "IAA": 8.10,
       "IEG": 7.40,
       "IPS": 6.90,
       "IDA": 7.20,
       "IPV": 8.05,
       "IAN": 5.00,
       "Defasagem": -1
     }'
```

**Resposta esperada**:
```json
{
  "risk_class": 1,
  "risk_probability": 0.85
}
```

### Via Python (requests)
```python
import requests

url = "http://localhost:8000/predict"
payload = {
    "RA": "RA-999",
    "Mat": 7.5,
    "Por": 6.8,
    "Pedra_0": "ametista",
    "Pedra_1": "agata",
    "Pedra_2": "quartzo",
    "INDE": 7.12,
    "IAA": 8.10,
    "IEG": 7.40,
    "IPS": 6.90,
    "IDA": 7.20,
    "IPV": 8.05,
    "IAN": 5.00,
    "Defasagem": -1
}

response = requests.post(url, json=payload)
print(response.json())
```

### Via Postman
- Método: POST
- URL: http://localhost:8000/predict
- Body: raw JSON com o exemplo acima
- Headers: Content-Type: application/json

## 5. Etapas do Pipeline de Machine Learning

1. **Pré-processamento**:
   - Padronização de nomes de colunas (remoção de sufixos .1/.2, aliases).
   - Normalização de valores ausentes (substituição por NaN ou valores padrão).
   - Conversão de colunas numéricas (pd.to_numeric com errors='coerce').
   - Normalização de colunas categóricas (strip, lower, remoção de acentos, colapsar espaços).
   - Aplicação de mapeamento/canonização de valores categóricos.
   - Validação de valores permitidos e deduplicação por chave (RA, Ano).
   - Reordenação de colunas conforme schema definido.

2. **Engenharia de Features**:
   - Construção de dataset tabular para modelagem: features do ano A + target do ano A+1.
   - Merge por identificador único (RA).
   - Mapeamento explícito de colunas de entrada para saída.
   - Validação de schema rígido para garantir consistência.

3. **Treinamento e Validação**:
   - Divisão estratificada: 70% treino, 15% validação, 15% teste.
   - Tratamento de dados: preenchimento de NaN (mediana para numéricas, "missing" para categóricas).
   - Remoção de colunas constantes e leakage.
   - Modelo: LightGBM Classifier com hiperparâmetros otimizados.
   - Métricas: accuracy, F1-score, precision, recall, classification report.

4. **Seleção de Modelo**:
   - Modelo único: LightGBM binário para classificação de risco.
   - Justificativa: bom desempenho em dados tabulares, tratamento de categóricas, interpretabilidade via feature importance.

5. **Pós-processamento**:
   - Serialização do modelo com joblib (inclui metadados: colunas, regras de target).
   - Preparação para inferência: reordenação de features, tratamento de NaN.

## Execução e Testes

### Como Executar o Projeto
1. **Clonar o repositório**:
   ```bash
   git clone <url-do-repositorio>
   cd FIAP---Tech-Challenge-Fase-4
   ```

2. **Configurar ambiente**:
   ```bash
   # Recomendado: usar uv para gerenciamento de dependências
   uv sync  # para pipeline_ml
   cd api && uv sync  # para api, se aplicável
   ```
   Ou manualmente:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # ou .venv\Scripts\activate no Windows
   pip install -e .  # instalar via pyproject.toml
   ```

3. **Executar pipeline de ML**:
   ```bash
   cd pipeline_ml
   python train.py
   ```

4. **Executar API**:
   ```bash
   cd api
   python -m uvicorn src.main:app --reload
   ```

### Como Testar o Código
O projeto utiliza pytest para testes unitários e pytest-cov para medição de cobertura.

#### Executar Testes da Pipeline ML
```bash
cd pipeline_ml
uv run pytest
```

#### Executar Testes da API
```bash
cd api
pytest  # ou uv run pytest se configurado
```

#### Verificar Cobertura de Testes
Para ver a porcentagem de código testado na pipeline ML:
```bash
cd pipeline_ml
uv run pytest --cov=. --cov-report=term-missing
```

Para a API:
```bash
cd api
pytest --cov=src --cov-report=term-missing
```

Ou para relatório HTML:
```bash
# Para pipeline
cd pipeline_ml
uv run pytest --cov=. --cov-report=html
# Abrir htmlcov/index.html no navegador

# Para API
cd api
pytest --cov=src --cov-report=html
# Abrir htmlcov/index.html no navegador
```

#### Cobertura Atual
- **Pipeline ML**: ~70-80% (estimativa baseada em testes implementados para preprocessing, feature engineering, train, evaluate).
- **API**: Testes básicos implementados; cobertura a ser expandida.

Para alcançar 80% de cobertura:
- Adicionar testes para casos edge (dados faltantes, tipos incorretos).
- Testes de integração end-to-end.
- Mock de dependências externas.

### Verificação de Qualidade
- **Linting**: Use flake8 ou black para estilo de código.
- **Type checking**: mypy para verificação de tipos.
- **CI/CD**: Configurar GitHub Actions para executar testes automaticamente.

---

Para mais informações sobre a Passos Mágicos, consulte os relatórios de atividades:
- 2023: https://passosmagicos.org.br/wp-content/uploads/2024/04/relatorio_de_atividades_passosmagicos_2023_compressed.pdf
- 2022: https://passosmagicos.org.br/wp-content/uploads/2023/04/relatorio_de_atividades_2022_passosmagicos_compressed.pdf
- 2021: https://passosmagicos.org.br/wp-content/uploads/2022/06/Relatorio-de-Atividades-2021-4_compressed.pdf
- 2020: https://passosmagicos.org.br/wp-content/uploads/2021/08/Relatorio_atividades_2020.pdf
