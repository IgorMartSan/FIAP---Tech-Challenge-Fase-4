# README Apresentacao

## FIAP - Tech Challenge Fase 4

## Predicao de risco de defasagem escolar na Passos Magicos

## 1. Contexto

Este projeto foi desenvolvido como entrega da **FIAP - Tech Challenge Fase 4** com base no desafio de negocio da instituicao **Passos Magicos**.

A proposta central foi usar dados educacionais historicos para antecipar alunos com maior risco de defasagem escolar, permitindo uma atuacao mais preventiva e orientada por dados.

## 2. Problema de negocio

A instituicao precisa identificar com antecedencia quais estudantes podem apresentar maior risco academico no periodo seguinte.

Sem esse tipo de previsao, a atuacao tende a ser mais reativa. Com um modelo preditivo, torna-se possivel:

- priorizar alunos com maior probabilidade de risco
- apoiar decisoes pedagogicas
- melhorar a alocacao de esforcos de acompanhamento
- reduzir o tempo de resposta da equipe educacional

## 3. Objetivo da solucao

Construir uma solucao completa de Machine Learning capaz de:

- tratar os dados brutos
- gerar uma base analitica para modelagem
- treinar um modelo de classificacao binaria
- avaliar o desempenho da predicao
- disponibilizar o modelo por API

## 4. Abordagem tecnica

O projeto foi organizado em quatro etapas principais:

### 4.1 Preprocessamento

Nesta fase foram realizados:

- padronizacao de colunas
- limpeza dos dados
- tratamento de valores ausentes
- normalizacao de variaveis categoricas
- deduplicacao por aluno e ano

### 4.2 Engenharia de features

Foi montado um dataset de previsao no formato:

- dados do aluno no ano atual
- resultado de defasagem no ano seguinte

Os pares usados no treinamento foram:

- `2022 -> 2023`
- `2023 -> 2024`

### 4.3 Treinamento

O problema foi tratado como **classificacao binaria**:

- `0`: sem risco de defasagem futura
- `1`: com risco de defasagem futura

O modelo escolhido foi o **LightGBM**, por seu bom desempenho em bases tabulares.

Configuracao do split:

- `70%` treino
- `15%` validacao
- `15%` teste

### 4.4 Avaliacao

As metricas observadas foram:

- accuracy
- precision
- recall
- f1-score

## 5. Resultado do modelo

```text
              precision    recall  f1-score   support

           0     0.8205    0.7619    0.7901        42
           1     0.7059    0.7742    0.7385        31

    accuracy                         0.7671        73
   macro avg     0.7632    0.7680    0.7643        73
weighted avg     0.7718    0.7671    0.7682        73
```

## 6. Interpretacao dos resultados

O modelo alcancou **76,71% de acuracia geral**, com desempenho equilibrado entre as duas classes.

O principal destaque para o negocio esta no **recall da classe 1 = 77,42%**, o que indica boa capacidade de identificar alunos que realmente apresentam risco de defasagem futura.

Em termos praticos, isso significa que o modelo consegue capturar a maior parte dos casos mais sensiveis, funcionando como uma ferramenta de priorizacao para a equipe pedagogica.

### Quando usar recall, precision e F1-score

Em problemas educacionais como este, olhar apenas para a acuracia nao e suficiente. Por isso, `recall`, `precision` e `F1-score` ajudam a interpretar melhor a qualidade do modelo.

- **Recall** deve ser priorizado quando o mais importante e **nao deixar passar alunos em risco**.
- **Precision** deve ser priorizada quando o mais importante e **evitar sinalizar alunos sem necessidade real de acompanhamento**.
- **F1-score** deve ser usado quando se busca **equilibrio entre identificar os casos de risco e evitar excessos de falsos alertas**.

### Interpretacao das porcentagens do modelo

- **Accuracy = 76,71%**: considerando todas as previsoes, o modelo acertou cerca de 77 em cada 100 casos.
- **Precision da classe 1 = 70,59%**: entre os alunos que o modelo classificou como risco, aproximadamente 71 em cada 100 realmente eram casos de risco.
- **Recall da classe 1 = 77,42%**: entre os alunos que realmente tinham risco de defasagem, o modelo conseguiu identificar cerca de 77 em cada 100.
- **F1-score da classe 1 = 73,85%**: esse valor representa o equilibrio entre `precision` e `recall` para a classe de risco.

### Leitura para o negocio

Se a prioridade da Passos Magicos for **encontrar o maior numero possivel de alunos vulneraveis**, a metrica mais importante e o **recall**.

Se a prioridade for **evitar sobrecarregar a equipe pedagogica com alertas indevidos**, a metrica mais importante passa a ser a **precision**.

Se a necessidade for manter um ponto de equilibrio entre essas duas perspectivas, a melhor referencia e o **F1-score**.

## 7. Testes realizados

O projeto tambem conta com testes automatizados para garantir maior confiabilidade.

### Pipeline de Machine Learning

Foram testados:

- preprocessamento
- engenharia de features
- treinamento
- avaliacao

Arquivos:

- `pipeline_ml/tests/test_preprocessing.py`
- `pipeline_ml/tests/test_feature_engineering.py`
- `pipeline_ml/tests/test_train_model.py`
- `pipeline_ml/tests/test_evaluate.py`

### API

Foram testados:

- carregamento do modelo
- preparacao das features
- funcionamento da rota `/predict`
- validacao de payload

Arquivos:

- `api/tests/test_model_loader.py`
- `api/tests/test_predict.py`

## 8. Entrega da solucao

Como entrega final, o projeto disponibiliza:

- pipeline de treinamento estruturada
- modelo treinado e serializado
- API FastAPI para inferencia
- testes automatizados
- documentacao do projeto

## 9. Conclusao

Este trabalho demonstra como tecnicas de Machine Learning podem apoiar o contexto educacional de forma pratica.

Ao prever o risco de defasagem escolar, a Passos Magicos pode atuar de forma mais preventiva, direcionando esforcos para os alunos com maior necessidade e usando dados como apoio a decisao.
