# Preprocessing

Este diretório contém a etapa de **preprocessing** do pipeline de ML.
O objetivo é transformar os dados brutos em dados consistentes e prontos
para as próximas fases (`feature_engineering`, `train` e `evaluate`).

## Objetivo da etapa

No preprocessing, você prepara o dado para reduzir ruído e evitar erros no modelo.
Em termos práticos, esta etapa deve:

- carregar a base bruta de forma confiável;
- padronizar estrutura e tipos das colunas;
- tratar dados faltantes e inconsistentes;
- aplicar regras de qualidade de dados;
- gerar uma base limpa para as próximas etapas.

## O que deve existir no preprocessing

1. Leitura de dados
- Funções para carregar arquivos (Excel/CSV/Parquet) com validação de caminho.
- Exemplo atual: `load_raw_data` em `load_data.py`.

2. Padronização de esquema
- Normalização de nomes de colunas.
- Conversão de tipos (`str`, `int`, `float`, `datetime`).
- Garantia de colunas obrigatórias.

3. Tratamento de valores ausentes
- Regras explícitas por coluna (mediana, moda, constante, ou remoção).
- Evitar regras implícitas que mudem entre treino e produção.

4. Tratamento de inconsistências
- Remoção de duplicados.
- Correção de faixas inválidas (ex.: idade negativa).
- Padronização de categorias textuais.

5. Validação de qualidade
- Checagens mínimas antes de salvar saída:
- colunas esperadas presentes;
- quantidade mínima de linhas;
- proporção de nulos aceitável.

6. Saída versionada
- Salvar dataset preprocessado em caminho definido (ex.: `pipeline_ml/outputs/`).
- Registrar data, origem e parâmetros utilizados na transformação.

## Fluxo recomendado

1. `load_raw_data(...)` lê a base original.
2. Aplicar funções de limpeza e padronização.
3. Validar qualidade e schema final.
4. Salvar dataset preprocessado para `feature_engineering`.

## Exemplo de uso (carga)

```python
from pipeline_ml.aa_preprocessing.load_data import load_raw_data

df_raw = load_raw_data(
    file_path="BASE DE DADOS PEDE 2024 - DATATHON.xlsx",
    sheet_name=None,
)
```

## Boas práticas

- Manter funções pequenas e testáveis.
- Evitar lógica de negócio espalhada: centralizar regras em funções nomeadas.
- Garantir reprodutibilidade: mesma entrada + mesmos parâmetros = mesma saída.
- Documentar toda regra que remove ou altera dados.

## Relação com API de predição

A API deve usar as **mesmas regras de preprocessing aplicadas no treino**.
Se treino e produção divergem, a predição perde confiabilidade.
