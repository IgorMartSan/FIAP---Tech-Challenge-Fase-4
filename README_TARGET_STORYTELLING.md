# Storytelling do Target: `RISCO_DEFASAGEM`

## O que a Passos Mágicos faz, na prática

A **Associação Passos Mágicos** é uma organização do terceiro setor que acompanha
crianças e jovens em jornada de desenvolvimento educacional.

Pelos materiais do projeto (PEDE, dicionário de dados e documentos de apoio),
o trabalho da instituição nao se limita a "dar aula". Ela opera um modelo completo de
acompanhamento do aluno, com:

- monitoramento anual de desempenho educacional;
- indicadores próprios (INDE, IAA, IEG, IPS, IDA, IPP, IPV, IAN);
- avaliações pedagógicas, psicossociais e psicopedagógicas;
- recomendações de avaliadores e equipe de psicologia;
- acompanhamento de evolução de fase, defasagem e ponto de virada;
- sinalizações operacionais como indicação para bolsa e status de permanência.

Em resumo: a Passos Mágicos trabalha para transformar trajetória escolar em
trajetória de oportunidade, usando acompanhamento contínuo e intervenções orientadas por dados.

## Objetivo institucional no contexto deste desafio

No Datathon, o objetivo de negócio é claro:
**identificar com antecedência alunos com risco de defasagem escolar**.

Isso permite sair de uma atuação reativa (agir tarde) para uma atuação preventiva
(agir antes da piora), priorizando melhor os recursos da equipe.

## Como a empresa trabalha com os alunos

Com base nos arquivos fornecidos, o cuidado com os alunos acontece em ciclos:
1. Coleta de dados educacionais e comportamentais ao longo do ano (`INSTITUICAO_ENSINO_ALUNO_2020`, `IDADE_ALUNO_2020`, `FASE_2021`, `TURMA_2021`, `NOTA_PORT_2022`, `NOTA_MAT_2022`, `PONTO_VIRADA_2021`).
2. Cálculo de indicadores de desenvolvimento (`INDE_2020`, `IAA_2021`, `IEG_2022`, `IPS_2022`, `IDA_2022`, `IPP_2021`, `IPV_2021`, `IAN_2021`).
3. Classificação de desempenho (como conceito por "Pedra" e INDE) (`PEDRA_2020`, `INDE_CONCEITO_2020`, `PEDRA_2021`, `CG_2022`, `CF_2022`, `CT_2022`, `NIVEL_IDEAL_2021`, `DEFASAGEM_2021`).
4. Leitura técnica da equipe (pedagógica, avaliadores e psicologia) (`DESTAQUE_IEG_2020`, `DESTAQUE_IDA_2022`, `DESTAQUE_IPV_2022`, `REC_PSICO_2021`, `REC_PSICO_2022`, `REC_EQUIPE_1_2021`, `REC_EQUIPE_2_2021`, `REC_EQUIPE_3_2021`, `REC_EQUIPE_4_2021`).
5. Definição de encaminhamentos: reforço, acompanhamento e priorização de casos (`SINALIZADOR_INGRESSANTE_2021`, `BOLSISTA_2022`, `ANO_INGRESSO_2022`, `PONTO_VIRADA_2021`, `DEFASAGEM_2021`).

Ou seja, o aluno é acompanhado de forma multidimensional: nota, engajamento,
aspectos psicossociais e aderência ao nível esperado.

## Explicação de cada coluna (descrição + exemplo)



### 1) Dados de contexto e trajetória escolar

- `INSTITUICAO_ENSINO_ALUNO_2020`: rede/tipo da escola do aluno em 2020 (sem ordem de melhor/pior). Exemplo: `Aluno estuda em escola pública estadual`. Dado: `Escola pública estadual`. Tipo: `str`.
- `IDADE_ALUNO_2020`: idade do aluno em 2020 (sem ordem de melhor/pior). Exemplo: `Aluno tinha 12 anos em 2020`. Dado: `12`. Tipo: `str`.
- `FASE_2021`: fase educacional do aluno em 2021 (quanto mais avancada para a idade, melhor). Exemplo: `Aluno estava na Fase 3`. Dado: `Fase 3`. Tipo: `float64`.
- `TURMA_2021`: turma alocada em 2021 (sem ordem de melhor/pior). Exemplo: `Aluno foi alocado na turma T3A`. Dado: `T3A`. Tipo: `str`.
- `NOTA_PORT_2022`: nota de Português no recorte de 2022 (quanto maior, melhor). Exemplo: `Aluno tirou 7.5 em Português`. Dado: `7.5`. Tipo: `float64`.
- `NOTA_MAT_2022`: nota de Matemática no recorte de 2022 (quanto maior, melhor). Exemplo: `Aluno tirou 6.8 em Matemática`. Dado: `6.8`. Tipo: `float64`.
- `PONTO_VIRADA_2021`: sinalização de virada positiva no ano (`Sim` tende a ser melhor). Exemplo: `Aluno saiu de queda e fechou o ano com melhoria`. Dado: `Sim`. Tipo: `str`.

### 2) Indicadores de desenvolvimento

- `INDE_2020`: índice consolidado de desenvolvimento educacional (quanto maior, melhor). Exemplo: `Aluno fechou o INDE em 6.9`. Dado: `6.9`. Tipo: `str`.
- `IAA_2021`: indicador de autoavaliação/aprendizagem do aluno (quanto maior, melhor). Exemplo: `Aluno recebeu IAA de 7.2 por boa autonomia`. Dado: `7.2`. Tipo: `float64`.
- `IEG_2022`: indicador de engajamento escolar (quanto maior, melhor). Exemplo: `Aluno teve IEG 8.1 por alta participação`. Dado: `8.1`. Tipo: `float64`.
- `IPS_2022`: indicador psicossocial (quanto maior, melhor). Exemplo: `Aluno marcou IPS 6.4 por oscilação emocional no semestre`. Dado: `6.4`. Tipo: `float64`.
- `IDA_2022`: indicador de desenvolvimento acadêmico (quanto maior, melhor). Exemplo: `Aluno ficou com IDA 6.7 após evoluir em leitura`. Dado: `6.7`. Tipo: `float64`.
- `IPP_2021`: indicador psicopedagógico (quanto maior, melhor). Exemplo: `Aluno teve IPP 7.0 com boa resposta a apoio pedagógico`. Dado: `7.0`. Tipo: `float64`.
- `IPV_2021`: indicador de potencial de evolução (quanto maior, melhor). Exemplo: `Aluno registrou IPV 6.1 e potencial moderado de avanço`. Dado: `6.1`. Tipo: `float64`.
- `IAN_2021`: indicador de aderência ao nível esperado (quanto maior, melhor). Exemplo: `Aluno ficou com IAN 5.8 por estar abaixo do nível ideal`. Dado: `5.8`. Tipo: `float64`.

### 3) Classificação de desempenho

- `PEDRA_2020`: classificação em faixas de desempenho no ano (faixas do menor para o maior: `Quartzo` -> `Ágata` -> `Ametista` -> `Topázio`). Exemplo: `Aluno foi classificado como Quartzo`. Dado: `Quartzo`. Tipo: `str`.
- `INDE_CONCEITO_2020`: conceito qualitativo associado ao INDE (faixas do menor para o maior: `D` -> `C` -> `B` -> `A`). Exemplo: `Com INDE 6.9, aluno ficou no conceito Intermediário`. Dado: `Intermediário`. Tipo: `str`.
- `PEDRA_2021`: atualização da faixa de desempenho em 2021 (faixas do menor para o maior: `Quartzo` -> `Ágata` -> `Ametista` -> `Topázio`). Exemplo: `Aluno evoluiu para a faixa Ágata`. Dado: `Ágata`. Tipo: `str`.
- `CG_2022`: conceito geral de desempenho em 2022 (conceitos mais altos sao melhores). Exemplo: `Aluno recebeu conceito geral B`. Dado: `B`. Tipo: `float64`.
- `CF_2022`: conceito de fechamento/final do período (conceitos mais altos sao melhores). Exemplo: `Aluno fechou o ciclo com CF B+`. Dado: `B+`. Tipo: `float64`.
- `CT_2022`: conceito técnico consolidado (conceitos mais altos sao melhores). Exemplo: `Equipe registrou CT como Adequado`. Dado: `Adequado`. Tipo: `float64`.
- `NIVEL_IDEAL_2021`: nível/fase ideal esperado para o aluno (referencia de expectativa; sem escala de melhor/pior isolada). Exemplo: `Para a idade dele, o ideal era Fase 4`. Dado: `Fase 4`. Tipo: `str`.
- `DEFASAGEM_2021`: diferença entre nível observado e ideal (quanto mais negativo, pior; quanto mais proximo de zero ou positivo, melhor). Exemplo: `Aluno estava na Fase 3 e teve defasagem -1`. Dado: `-1`. Tipo: `float64`.

### 4) Leitura técnica da equipe

- `DESTAQUE_IEG_2020`: observação de destaque no indicador de engajamento (texto qualitativo; sem ordem fixa). Exemplo: `Equipe anotou queda de participação no 2º semestre`. Dado: `Participação em queda no 2º semestre`. Tipo: `str`.
- `DESTAQUE_IDA_2022`: observação de destaque no indicador acadêmico (texto qualitativo; sem ordem fixa). Exemplo: `Equipe observou melhora contínua em leitura`. Dado: `Melhora contínua em leitura`. Tipo: `str`.
- `DESTAQUE_IPV_2022`: observação de destaque no potencial de evolução (texto qualitativo; sem ordem fixa). Exemplo: `Aluno respondeu bem ao reforço e ganhou destaque positivo`. Dado: `Alta resposta a reforço`. Tipo: `str`.
- `REC_PSICO_2021`: recomendação da psicologia para o aluno (texto de acao; sem ordem fixa). Exemplo: `Psicologia recomendou acompanhamento quinzenal`. Dado: `Acompanhamento quinzenal`. Tipo: `str`.
- `REC_PSICO_2022`: atualização da recomendação psicológica (texto de acao; sem ordem fixa). Exemplo: `Psicologia manteve acompanhamento mensal em 2022`. Dado: `Manter acompanhamento mensal`. Tipo: `str`.
- `REC_EQUIPE_1_2021`: recomendação pedagógica principal da equipe (texto de acao; sem ordem fixa). Exemplo: `Equipe pediu reforço em Matemática`. Dado: `Reforço em Matemática`. Tipo: `str`.
- `REC_EQUIPE_2_2021`: segunda recomendação da equipe (texto de acao; sem ordem fixa). Exemplo: `Equipe sugeriu plano de estudos semanal`. Dado: `Plano de estudos semanal`. Tipo: `str`.
- `REC_EQUIPE_3_2021`: terceira recomendação da equipe (texto de acao; sem ordem fixa). Exemplo: `Equipe indicou mentoria de organização`. Dado: `Mentoria de organização`. Tipo: `str`.
- `REC_EQUIPE_4_2021`: quarta recomendação da equipe (texto de acao; sem ordem fixa). Exemplo: `Equipe definiu contato frequente com o responsável`. Dado: `Contato com responsável`. Tipo: `str`.

### 5) Encaminhamentos operacionais

- `SINALIZADOR_INGRESSANTE_2021`: marca se o aluno ingressou recentemente (sem ordem de melhor/pior isolada). Exemplo: `Valor 1 indica que o aluno entrou no programa em 2021`. Dado: `1`. Tipo: `str`.
- `BOLSISTA_2022`: status de bolsa no período (sem ordem de melhor/pior isolada). Exemplo: `Aluno estava com bolsa ativa em 2022`. Dado: `Sim`. Tipo: `str`.
- `ANO_INGRESSO_2022`: ano de ingresso registrado na base de 2022 (sem ordem de melhor/pior isolada). Exemplo: `Base mostra que o aluno ingressou em 2021`. Dado: `2021`. Tipo: `float64`.
- `PONTO_VIRADA_2021`: marca de mudança relevante positiva/negativa na trajetória (`Sim` tende a ser melhor). Exemplo: `Aluno virou a curva e melhorou no fim do ano`. Dado: `Sim`. Tipo: `str`.
- `DEFASAGEM_2021`: diferença para o nível ideal usada para priorização (quanto mais negativo, pior; quanto mais proximo de zero ou positivo, melhor). Exemplo: `Com defasagem -2, aluno entra como alta prioridade`. Dado: `-2`. Tipo: `float64`.


## Definição do target do projeto

Para representar esse problema no modelo, adotamos:

- `RISCO_DEFASAGEM = 1` quando `Defasagem < 0`
- `RISCO_DEFASAGEM = 0` quando `Defasagem >= 0`

Interpretação:

- `1`: aluno abaixo da fase ideal para o momento;
- `0`: aluno sem sinal de defasagem no recorte observado.

## Storytelling (narrativa de negócio)

Todo início de ciclo, centenas de alunos precisam de acompanhamento.
A equipe da Passos Mágicos sabe que cada estudante tem um contexto diferente,
mas a capacidade de intervenção é finita.

Sem priorização analítica, os casos críticos podem aparecer apenas quando a
defasagem já se consolidou. Isso custa tempo, aprendizagem e, em alguns casos,
a permanência do aluno na trilha educacional.

Com o target `RISCO_DEFASAGEM`, a organização ganha uma "fila inteligente" de atenção:
quem tem maior risco sobe na prioridade para receber suporte pedagógico e psicossocial
mais cedo.

Na prática, o modelo nao substitui a equipe. Ele organiza o foco da equipe.
O resultado esperado é simples e poderoso: intervir antes, reduzir defasagem,
aumentar chance de progresso acadêmico e proteger a trajetória dos alunos.

## Conexão com o código

O target é construído no treino em:

- [`pipeline_ml/ca_train/train_model.py`](/home/igor/Projetos/FIAP---Tech-Challenge-Fase-4/pipeline_ml/ca_train/train_model.py)

A função `build_target` converte `Defasagem` em variável binária de risco.
