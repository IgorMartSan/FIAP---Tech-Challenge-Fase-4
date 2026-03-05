
# 📊 Datathon – Previsão de Defasagem Escolar

## 1. Visão Geral

Este projeto tem como objetivo desenvolver um modelo de **Machine Learning capaz de prever o risco de defasagem escolar dos estudantes** utilizando dados educacionais dos anos de **2022, 2023 e 2024**.

A proposta é construir uma **pipeline completa de Machine Learning**, incluindo:

- Pré-processamento de dados
- Engenharia de features
- Treinamento do modelo
- Validação
- API para previsão
- Empacotamento com Docker

---

# 2. Problema de Negócio

A defasagem escolar ocorre quando um aluno está **atrasado em relação à série esperada para sua idade**.

Identificar alunos com risco de defasagem permite:

- oferecer suporte educacional antecipado
- acompanhar o progresso do estudante
- reduzir evasão escolar

O objetivo do modelo é **prever o risco de defasagem no próximo ano escolar**.

---

# 3. Estrutura do Dataset

O dataset contém dados educacionais dos anos:

2022  
2023  
2024  

Cada aba do Excel representa um ano.

Cada linha representa **um aluno em determinado ano**.

Principais colunas:

| Coluna | Descrição |
|------|------|
| RA | Identificador do aluno |
| Idade | Idade do estudante |
| Fase | Série atual |
| Fase Ideal | Série esperada para idade |
| Defasagem | Indicador de atraso escolar |
| INDE | Índice de desempenho educacional |
| Mat | Nota de matemática |
| Por | Nota de português |
| Ing | Nota de inglês |
| IAA | Indicador de desempenho acadêmico |
| IEG | Engajamento |
| IPS | Participação |
| IPP | Progresso |
| IDA | Disciplina |
| IPV | Presença |
| IAN | Indicador de notas |
| Pedra | Classificação de desempenho |

---

# 4. Estratégia de Modelagem

Para construir o dataset de Machine Learning foi utilizada uma abordagem **temporal**.

A ideia é usar o desempenho atual do aluno para prever seu desempenho no ano seguinte.

### Construção das amostras

Foram criados dois conjuntos de exemplos:

2022 → 2023  
2023 → 2024  

Cada exemplo representa:

estado do aluno no ano **t** → resultado no ano **t+1**

Exemplo:

| INDE_t | Mat_t | Por_t | Defasagem_t | Target |
|------|------|------|------|------|
| INDE_2022 | Mat_2022 | Por_2022 | Defasagem_2022 | INDE_2023 |
| INDE_2023 | Mat_2023 | Por_2023 | Defasagem_2023 | INDE_2024 |

Esses datasets são então **unificados para treinamento do modelo**.

---

# 5. Engenharia de Features

Algumas features importantes utilizadas:

### Indicadores de desempenho

INDE  
IAA  
IEG  
IPS  
IPP  
IDA  
IPV  
IAN  

### Notas escolares

Mat  
Por  
Ing  

### Indicadores educacionais

Fase  
Fase Ideal  
Defasagem  

### Evolução do desempenho

Exemplo:

ΔINDE = INDE_2023 - INDE_2022

Essa variável indica se o aluno:

- melhorou
- piorou
- manteve desempenho

---

# 6. Pipeline de Machine Learning

A pipeline do projeto segue as etapas:

Leitura dos dados  
↓  
Pré-processamento  
↓  
Engenharia de features  
↓  
Construção do dataset temporal  
↓  
Treinamento do modelo  
↓  
Validação  
↓  
Deploy via API  

---

# 7. Pré-processamento

O pré-processamento realiza:

### Padronização de colunas
Remoção de sufixos duplicados gerados pelo Excel.

### Unificação de colunas equivalentes

Exemplo:

Matem → Mat  
Portug → Por  
Inglês → Ing  

### Conversão de tipos

Conversão de colunas numéricas para `float`.

### Normalização de valores ausentes

Valores como:

""  
NA  
-  
N/A  

são convertidos para **NaN**.

### Remoção de duplicatas

Duplicatas são removidas usando:

RA + Ano

---

# 8. Divisão dos dados

Após construir o dataset final, os dados são divididos em:

Treino  
Validação  
Teste  

Utilizando `train_test_split`.

---

# 9. Tecnologias utilizadas

| Tecnologia | Uso |
|------|------|
| Python | linguagem principal |
| Pandas | manipulação de dados |
| Numpy | operações numéricas |
| Scikit-Learn | treinamento do modelo |
| FastAPI | API de previsão |
| Docker | empacotamento |
| Pytest | testes |

---

# 10. Estrutura do Projeto

project/

data/
- raw/
- processed/

pipeline_ml/
- preprocessing/
- feature_engineering/
- training/
- utils/

api/

tests/

Dockerfile  
requirements.txt  
README.md

---

# 11. Execução do projeto

Criar ambiente virtual:

python -m venv .venv

Instalar dependências:

pip install -r requirements.txt

Executar pipeline:

python pipeline_ml/dev_pipeline.py

---

# 12. API de previsão

Endpoint:

POST /predict

Exemplo de entrada:

{
    "INDE": 6.5,
    "Mat": 7.0,
    "Por": 6.8,
    "Defasagem": 0
}

Saída esperada:

{
    "risco_defasagem": 0.23
}

---

# 13. Conclusão

Este projeto demonstra como construir uma **pipeline completa de Machine Learning aplicada à educação**, com o objetivo de identificar estudantes com risco de defasagem escolar e permitir intervenções educacionais mais eficazes.
