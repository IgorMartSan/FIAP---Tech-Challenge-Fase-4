# Datathon --- Passos Mágicos

## Storytelling + Checklist de Execução (do zero ao deploy)

### Contexto (história do problema)

A Associação Passos Mágicos atua há décadas transformando a vida de
crianças e jovens em vulnerabilidade social por meio da educação. O
desafio do Datathon é usar os dados de 2022, 2023 e 2024 para prever o
risco de defasagem escolar e permitir intervenções antecipadas.

### Objetivo do projeto

Construir um sistema de Machine Learning completo capaz de: - Treinar um
modelo preditivo confiável - Servir previsões via API - Ser replicável
com Docker - Ser testável com pytest - Ser monitorável com logs e
detecção de drift

------------------------------------------------------------------------

# Checklist passo a passo

## 0) Preparação do repositório

-   Criar repositório GitHub
-   Criar estrutura do projeto

```{=html}
<!-- -->
```
    project/
    ├── data/
    │   ├── raw/
    │   ├── processed/
    │   └── features/
    ├── models/
    ├── notebooks/
    ├── src/
    │   ├── preprocessing.py
    │   ├── feature_engineering.py
    │   ├── train.py
    │   ├── evaluate.py
    │   ├── predict.py
    │   └── utils.py
    ├── api/
    │   ├── main.py
    │   └── schemas.py
    ├── tests/
    ├── Dockerfile
    ├── requirements.txt
    └── README.md

------------------------------------------------------------------------

## 1) Entendimento do dataset

-   Identificar ID do aluno
-   Identificar coluna de ano (2022, 2023, 2024)
-   Identificar variáveis educacionais (nota, frequência etc)
-   Identificar variáveis socioeconômicas
-   Definir variável TARGET (risco de defasagem)

------------------------------------------------------------------------

## 2) Ingestão e padronização dos dados

-   Colocar arquivos originais em `data/raw`
-   Criar script de preprocessing:
    -   padronizar nomes de colunas
    -   remover duplicados
    -   tratar valores nulos
    -   corrigir tipos
-   Salvar dados limpos em `data/processed`

------------------------------------------------------------------------

## 3) Feature Engineering

Criar novas variáveis importantes:

-   tendência de nota
-   tendência de frequência
-   média histórica de desempenho
-   flag de baixa frequência
-   histórico de apoio psicopedagógico

Salvar dataset final em:

    data/features/dataset_features.parquet

------------------------------------------------------------------------

## 4) Estratégia de treino

Treino: - dados de 2022 - dados de 2023

Teste: - dados de 2024

Isso simula o cenário real de previsão.

------------------------------------------------------------------------

## 5) Treinamento do modelo

-   Carregar dataset
-   Separar X e y
-   Treinar modelo (LightGBM recomendado)
-   Avaliar com:
    -   ROC-AUC
    -   F1 Score
    -   Recall

Salvar modelo:

    models/model.pkl

------------------------------------------------------------------------

## 6) API de previsão

Criar API com FastAPI:

Endpoint:

    POST /predict

Entrada: - nota - frequência - dados socioeconômicos

Saída:

    {
      "risk_probability": 0.82,
      "risk_label": 1
    }

------------------------------------------------------------------------

## 7) Docker

Criar Dockerfile e rodar:

    docker build -t passos-magicos-ml .
    docker run -p 8000:8000 passos-magicos-ml

------------------------------------------------------------------------

## 8) Testes unitários

Criar testes para:

-   preprocessamento
-   geração de features
-   modelo
-   endpoint da API

Executar:

    pytest --cov

------------------------------------------------------------------------

## 9) Monitoramento

Adicionar:

-   logs de requests
-   logs de previsão
-   monitoramento de drift das features

------------------------------------------------------------------------

## 10) Documentação

No README incluir:

-   objetivo do projeto
-   arquitetura da solução
-   instruções de execução
-   exemplos de chamada da API
-   métricas do modelo

------------------------------------------------------------------------

## 11) Vídeo de apresentação

Estrutura sugerida:

1.  Contexto social
2.  Problema de previsão
3.  Abordagem de ML
4.  Pipeline de dados
5.  API e deploy
6.  Impacto da solução
