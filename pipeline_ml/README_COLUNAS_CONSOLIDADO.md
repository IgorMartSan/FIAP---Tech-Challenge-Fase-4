# Guia Didatico das Colunas - Dataset Consolidado

Arquivo documentado:
`pipeline_ml/outputs/dados_feature_engineering_consolidado.csv`

Objetivo deste guia:
- Explicar cada coluna em linguagem simples.
- Mostrar como interpretar o valor.
- Indicar como usar (ou nao usar) no modelo de ML.

Legenda rapida:
- `Feature`: pode entrar como variavel de entrada do modelo.
- `Target`: variavel alvo para prever.
- `Nao usar`: evitar no treino (identificador, texto livre ou risco de vazamento).

## 1) Identificacao e contexto do aluno

| Coluna | O que e | Como interpretar | Uso em ML | Exemplo |
|---|---|---|---|---|
| RA | Codigo unico do aluno. | Mesmo aluno pode aparecer em anos diferentes com o mesmo RA. | `Nao usar` como feature (identificador). Pode usar para agrupar/split temporal por aluno. | `RA-1` |
| Nome | Nome anonimizado do aluno. | Identificacao textual do aluno. | `Nao usar` (identificador, alta cardinalidade). | `Aluno-1` |
| Gênero | Genero informado. | Categoria demografica. | `Feature` categorial (com encoding). | `Menina` |
| Data de Nasc | Data de nascimento na planilha. | Data completa; pode virar idade precisa por ano. | Melhor derivar idade e descartar texto/data bruta. | `6/17/2015` |
| Ano nasc | Ano de nascimento. | Versao simplificada de nascimento. | `Feature` numerica (com cuidado por nulos). | `2003.0` |
| Idade 22 | Idade no ano de 2022. | Congelada em 2022, util para historico. | `Feature` historica (somente quando fizer sentido temporal). | `19.0` |
| Idade | Idade no ano da linha. | Idade corrente para o ano de referencia. | `Feature` numerica forte. | `8.0` |
| Instituição de ensino | Tipo de escola (publica/privada). | Contexto socioeducacional do aluno. | `Feature` categorial. | `Escola Pública` |
| Escola | Nome da escola. | Categoria de alta cardinalidade. | Usar so com encoding robusto; no baseline, `Nao usar`. | `EE Chácara Florida II` |
| Ativo/ Inativo | Status de permanencia no programa. | Ex.: Cursando, Inativo. | `Feature` categorial, mas tem muitos nulos em anos antigos. | `Cursando` |
| Ano ingresso | Ano de entrada no programa. | Quanto menor, mais tempo de casa. | `Feature` numerica; base para `ANOS_NO_PROGRAMA`. | `2016` |
| ANO_REFERENCIA | Ano da observacao (2022/2023/2024). | Linha representa o aluno naquele ano. | `Feature` temporal importante. | `2022` |
| ANOS_NO_PROGRAMA | Tempo no programa no ano da linha. | `ANO_REFERENCIA - Ano ingresso`. | `Feature` numerica forte de maturidade. | `6` |
| Turma | Letra/codigo da turma. | Segmento/turma do aluno no ano. | `Feature` categorial (pode refletir perfil pedagogico). | `A` |

## 2) Fase escolar e defasagem

| Coluna | O que e | Como interpretar | Uso em ML | Exemplo |
|---|---|---|---|---|
| Fase | Fase atual do aluno. | Ordem pedagogica (ALFA, 1A, 1B, ...). | `Feature` importante (ordinal/categorial). | `7` |
| Fase Ideal | Fase esperada para o aluno. | Referencia pedagogica do nivel ideal. | `Feature` categorial/ordinal. | `Fase 8 (Universitários)` |
| Defasagem | Diferenca entre fase atual e ideal. | Negativo: atrasado; zero: adequado; positivo: adiantado (depende regra interna). | `Feature` numerica muito relevante. | `-1` |
| FASE_NUMERICA | Conversao de `Fase` para escala numerica. | Ex.: ALFA=0, 1A=1.0, 1B=1.1. | `Feature` pronta para modelos numericos. | `7.0` |

## 3) Indicadores academicos (score)

| Coluna | O que e | Como interpretar | Uso em ML | Exemplo |
|---|---|---|---|---|
| IAA | Indicador academico IAA. | Quanto maior, melhor no criterio do indicador. | `Feature` numerica. | `8.3` |
| IEG | Indicador academico IEG. | Mesmo principio: score de desempenho especifico. | `Feature` numerica. | `4.1` |
| IPS | Indicador academico IPS. | Score de dimensao especifica. | `Feature` numerica. | `5.6` |
| IPP | Indicador academico IPP. | Disponivel principalmente em anos recentes. | `Feature` numerica (com imputacao). | `8.4375` |
| IDA | Indicador academico IDA. | Score por eixo/dimensao IDA. | `Feature` numerica. | `4.0` |
| IPV | Indicador academico IPV. | Score por eixo/dimensao IPV. | `Feature` numerica. | `7.278` |
| IAN | Indicador academico IAN. | Score por eixo/dimensao IAN. | `Feature` numerica. | `5.0` |
| MEDIA_INDICADORES | Media dos indicadores (IAA, IEG, IPS, IPP, IDA, IPV, IAN). | Resumo global de desempenho. | `Feature` sintetica util para baseline. | `5.713` |
| Cg | Campo tecnico da base original. | Sigla sem definicao formal no desafio. | Pode testar como `Feature`, mas validar impacto e qualidade antes. | `753.0` |
| Cf | Campo tecnico da base original. | Sigla sem definicao formal no desafio. | Mesmo tratamento de `Cg`. | `18.0` |
| Ct | Campo tecnico da base original. | Sigla sem definicao formal no desafio. | Mesmo tratamento de `Cg`. | `10.0` |

## 4) Notas por disciplina

| Coluna | O que e | Como interpretar | Uso em ML | Exemplo |
|---|---|---|---|---|
| Mat | Nota/score de matematica (padronizada). | Valor mais alto indica melhor desempenho na disciplina. | `Feature` numerica. | `2.7` |
| Por | Nota/score de portugues (padronizada). | Mesmo racional da disciplina. | `Feature` numerica. | `3.5` |
| Ing | Nota/score de ingles (padronizada). | Tem mais nulos em anos antigos. | `Feature` numerica (imputar nulos). | `6.0` |
| MEDIA_NOTAS | Media entre Mat, Por, Ing. | Resume desempenho geral em disciplinas. | `Feature` sintetica. | `4.066666666666666` |
| DESVIO_NOTAS | Variacao entre Mat, Por, Ing. | Alto desvio = desempenho desigual entre materias. | `Feature` de estabilidade academica. | `1.721433511156714` |

## 5) Avaliacao humana e recomendacoes

| Coluna | O que e | Como interpretar | Uso em ML | Exemplo |
|---|---|---|---|---|
| Nº Av | Numero de avaliacoes registradas. | Mais avaliacoes podem indicar acompanhamento mais completo. | `Feature` numerica. | `4.0` |
| Avaliador1 | Identificador do avaliador 1. | Codigo de quem avaliou. | Geralmente `Nao usar` no baseline (alta cardinalidade). | `Avaliador-5` |
| Avaliador2 | Identificador do avaliador 2. | Mesmo criterio do Avaliador1. | `Nao usar` no baseline. | `Avaliador-27` |
| Avaliador3 | Identificador do avaliador 3. | Mesmo criterio do Avaliador1. | `Nao usar` no baseline. | `Avaliador-28` |
| Avaliador4 | Identificador do avaliador 4. | Mesmo criterio do Avaliador1. | `Nao usar` no baseline. | `Avaliador-31` |
| Avaliador5 | Identificador do avaliador 5. | Preenchido em poucas linhas. | `Nao usar` no baseline. | `Avaliador-7` |
| Avaliador6 | Identificador do avaliador 6. | Quase sempre nulo. | `Nao usar`. | `Avaliador-26` |
| Rec Av1 | Texto de recomendacao do avaliador 1. | Conteudo qualitativo de decisao/encaminhamento. | So usar com NLP; baseline: `Nao usar`. | `Mantido na Fase atual` |
| Rec Av2 | Texto de recomendacao do avaliador 2. | Mesmo criterio do Rec Av1. | Baseline: `Nao usar`. | `Promovido de Fase + Bolsa` |
| Rec Av3 | Texto de recomendacao do avaliador 3. | Mesmo criterio do Rec Av1. | Baseline: `Nao usar`. | `Promovido de Fase` |
| Rec Av4 | Texto de recomendacao do avaliador 4. | Mesmo criterio do Rec Av1. | Baseline: `Nao usar`. | `Mantido na Fase atual` |
| Rec Psicologia | Recomendacao da psicologia. | Texto clinico/educacional. | So usar com NLP e cuidado etico; baseline: `Nao usar`. | `Requer avaliação` |
| QTD_AVALIADORES_PREENCHIDOS | Quantos campos `Avaliador*` estao preenchidos. | Proxi de cobertura avaliativa. | `Feature` numerica robusta. | `4` |
| QTD_RECOMENDACOES_PREENCHIDAS | Quantos campos de recomendacao estao preenchidos. | Proxi de volume de observacoes. | `Feature` numerica robusta. | `5` |

## 6) Sinais de destaque e status

| Coluna | O que e | Como interpretar | Uso em ML | Exemplo |
|---|---|---|---|---|
| Indicado | Marcador de indicacao. | Ex.: aluno foi indicado para algo especifico. | `Feature` categorial (avaliar nulos). | `Sim` |
| Atingiu PV | Marcador de atingimento de PV. | Ex.: atingiu criterio PV (sim/nao). | `Feature` categorial. | `Não` |
| Destaque IEG | Texto de destaque sobre IEG. | Comentario qualitativo de melhoria/forca. | NLP apenas; baseline: `Nao usar`. | `Melhorar: ... lições de casa.` |
| Destaque IDA | Texto de destaque sobre IDA. | Comentario qualitativo. | NLP apenas; baseline: `Nao usar`. | `Melhorar: ... aulas e avaliações.` |
| Destaque IPV | Texto de destaque sobre IPV. | Comentario qualitativo. | NLP apenas; baseline: `Nao usar`. | `Melhorar: ... Princípios Passos Mágicos.` |

## 7) Historico de INDE e Pedra por ano (colunas originais)

| Coluna | O que e | Como interpretar | Uso em ML | Exemplo |
|---|---|---|---|---|
| INDE 22 | INDE do ano 2022. | Score continuo de desempenho no ano. | Pode usar como historico para prever ano futuro. | `5.783` |
| INDE 23 | INDE do ano 2023 (nome curto). | Mesmo indicador, outra nomenclatura. | Igual ao acima. | `8.63895` |
| INDE 2023 | INDE do ano 2023 (nome longo). | Duplicidade de nomenclatura na origem. | Preferir coluna unificada no pipeline. | `9.31095` |
| INDE 2024 | INDE do ano 2024. | Score continuo do ano 2024. | Historico/analise temporal. | `7.611366666700001` |
| Pedra 20 | Pedra (faixa) de 2020. | Categoria de desempenho historico. | `Feature` historica categorial. | `Ametista` |
| Pedra 21 | Pedra (faixa) de 2021. | Categoria de desempenho historico. | `Feature` historica categorial. | `Ametista` |
| Pedra 22 | Pedra (faixa) de 2022. | Categoria de desempenho historico. | `Feature` historica categorial. | `Quartzo` |
| Pedra 23 | Pedra (faixa) de 2023 (nome curto). | Mesma ideia com variacao de nome. | `Feature` historica categorial. | `Topázio` |
| Pedra 2023 | Pedra (faixa) de 2023 (nome longo). | Variacao da mesma informacao. | Preferir forma unificada. | `Topázio` |
| Pedra 2024 | Pedra (faixa) de 2024. | Categoria de desempenho em 2024. | Historico/analise temporal. | `Ametista` |

## 8) Alvos unificados para treino (gerados no feature engineering)

| Coluna | O que e | Como interpretar | Uso em ML | Exemplo |
|---|---|---|---|---|
| INDE_ATUAL | INDE correspondente ao ano da linha (unificado). | Se a linha e 2023, traz o INDE de 2023. | `Target` para regressao. Nao usar como feature quando for alvo. | `5.783` |
| PEDRA_ATUAL | Pedra correspondente ao ano da linha (unificado). | Se a linha e 2024, traz a Pedra de 2024. | `Target` para classificacao. Nao usar como feature quando for alvo. | `Quartzo` |

## Regras praticas para modelagem

1. Baseline de classificacao:
- `y = PEDRA_ATUAL`
- Remover de `X`: `PEDRA_ATUAL`, todas colunas `Pedra ...` do mesmo ano, `RA`, `Nome`, textos longos.

2. Baseline de regressao:
- `y = INDE_ATUAL`
- Remover de `X`: `INDE_ATUAL`, todas colunas `INDE ...` do mesmo ano, `RA`, `Nome`, textos longos.

3. Sobre indicadores (`IAA`, `IEG`, `IPS`, `IPP`, `IDA`, `IPV`, `IAN`):
- Sao variaveis numericas de desempenho por dimensao.
- Em geral, valores maiores indicam melhor resultado naquela dimensao.
- Podem ser usados individualmente e tambem via `MEDIA_INDICADORES`.

4. Sobre texto (`Rec Av*`, `Destaque*`, `Rec Psicologia`):
- Para baseline, melhor remover.
- Se quiser usar, criar um pipeline NLP separado (vetorizacao + validacao adequada).

## Opcoes e significado (colunas categóricas)

Observacao:
- As listas abaixo foram extraidas do CSV consolidado atual.
- Onde o negocio nao define oficialmente cada categoria, o significado foi descrito de forma operacional.

### Gênero

- `Feminino`: aluna do sexo feminino.
- `Menina`: aluna do sexo feminino (variante de preenchimento).
- `Masculino`: aluno do sexo masculino.
- `Menino`: aluno do sexo masculino (variante de preenchimento).

Recomendacao:
- Padronizar para 2 valores (`Feminino`, `Masculino`) antes de treinar.

### Indicado

- `Sim`: aluno marcado como indicado.
- `Não`: aluno nao marcado como indicado.

### Atingiu PV

- `Sim`: aluno atingiu o criterio PV.
- `Não`: aluno nao atingiu o criterio PV.

### Ativo/ Inativo

- `Cursando`: aluno ativo no programa (no recorte atual, so apareceu esse valor).

### Pedra (faixa de desempenho)

Opcoes encontradas nas colunas `Pedra 20`, `Pedra 21`, `Pedra 22`, `Pedra 23`, `Pedra 2023`, `Pedra 2024`, `PEDRA_ATUAL`:

- `Ágata` / `Agata`: mesma categoria (diferenca apenas de acento).
- `Ametista`
- `Quartzo`
- `Topázio`
- `INCLUIR`: valor especial encontrado em 2024; normalmente indica situacao administrativa/pendente e deve ser tratado antes do treino (ex.: mapear para categoria propria ou como nulo).

Significado operacional:
- Sao classes de desempenho por faixa (categoria), em vez de nota continua.
- Regra de ordenacao oficial nao foi explicitada no material; portanto, usar como categorial nominal por padrao.

### Instituição de ensino

Opcoes encontradas:
- `Escola Pública`
- `Pública`
- `Privada`
- `Privada *Parcerias com Bolsa 100%`
- `Privada - Pagamento por *Empresa Parceira`
- `Privada - Programa de Apadrinhamento`
- `Privada - Programa de apadrinhamento`
- `Rede Decisão`
- `Escola JP II`
- `Concluiu o 3º EM`
- `Bolsista Universitário *Formado (a)`
- `Nenhuma das opções acima`

Significado operacional:
- Mistura tipo de escola com status/condicao educacional.

Recomendacao:
- Criar normalizacao em camadas:
1. Tipo macro (`Publica`, `Privada`, `Outra`).
2. Sinalizadores adicionais (`bolsista`, `formado`, `apadrinhamento`).

### Fase Ideal

Opcoes encontradas:
- `ALFA  (2º e 3º ano)`
- `ALFA (1° e 2° ano)`
- `Fase 1 (3° e 4° ano)`
- `Fase 1 (4º ano)`
- `Fase 2 (5° e 6° ano)`
- `Fase 2 (5º e 6º ano)`
- `Fase 3 (7° e 8° ano)`
- `Fase 3 (7º e 8º ano)`
- `Fase 4 (9° ano)`
- `Fase 4 (9º ano)`
- `Fase 5 (1° EM)`
- `Fase 5 (1º EM)`
- `Fase 6 (2° EM)`
- `Fase 6 (2º EM)`
- `Fase 7 (3° EM)`
- `Fase 7 (3º EM)`
- `Fase 8 (Universitários)`

Significado:
- Define a fase esperada para a idade/ano escolar do aluno.
- Variacoes com `°` e `º` sao equivalentes e podem ser padronizadas.

### Fase

Valores encontrados no CSV:
- `ALFA`
- `0`, `1`, `2`, `3`, `4`, `5`, `6`, `7`, `9`
- `1A`, `1B`, `1C`, `1D`, `1E`, `1G`, `1H`, `1J`, `1K`, `1L`, `1M`, `1N`, `1P`, `1R`
- `2A`, `2B`, `2C`, `2D`, `2G`, `2H`, `2I`, `2K`, `2L`, `2M`, `2N`, `2P`, `2R`, `2U`
- `3A`, `3B`, `3C`, `3D`, `3F`, `3G`, `3H`, `3I`, `3K`, `3L`, `3M`, `3N`, `3P`, `3R`, `3U`
- `4A`, `4B`, `4C`, `4F`, `4H`, `4L`, `4M`, `4N`, `4R`
- `5A`, `5B`, `5C`, `5D`, `5F`, `5G`, `5L`, `5M`, `5N`
- `6A`, `6L`
- `7A`, `7E`
- `8A`, `8B`, `8D`, `8E`, `8F`
- `FASE 1`, `FASE 2`, `FASE 3`, `FASE 4`, `FASE 5`, `FASE 6`, `FASE 7`, `FASE 8`

Significado operacional:
- Mesmo conceito de nivel pedagogico, mas com padroes diferentes de preenchimento.
- Ex.: `FASE 3` e `3` indicam a mesma fase macro; sufixos (`A`, `B`, etc.) costumam segmentar subgrupos/turma.

### Turma

Valores encontrados (120 categorias):
- codigos curtos: `A`, `B`, `C`, ..., `Z`
- codigos fase+tumra: `1A`, `1B`, ..., `8F`
- codigos ALFA detalhados, por exemplo: `ALFA A - G0/G1`, `ALFA B - G2/G3`, ..., `ALFA Y - G0/G1`

Significado operacional:
- Identificador de grupo/turma do aluno no ano.
- Sufixos como `G0/G1` e `G2/G3` aparentam subgrupos internos.

Recomendacao:
- Para baseline, usar encoding categorial simples (one-hot/frequency).
- Para reduzir cardinalidade, extrair `fase_base` da turma e manter sufixo em coluna separada.
