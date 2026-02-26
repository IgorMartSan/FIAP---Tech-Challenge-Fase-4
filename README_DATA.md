# Dicionario de Dados

Este arquivo descreve as colunas da base `BASE DE DADOS PEDE 2024 - DATATHON.xlsx`.

## Abas da planilha

- `PEDE2022`
- `PEDE2023`
- `PEDE2024`

## Observacoes importantes

- Existem nomes de colunas que mudam entre anos (ex.: `Matem` em 2022 e `Mat` em 2023/2024).
- Existem colunas duplicadas no arquivo original:
  - `Destaque IPV` aparece duas vezes na aba `PEDE2023`.
  - `Ativo/ Inativo` aparece duas vezes na aba `PEDE2024`.
- Algumas siglas nao possuem definicao explicita no material do desafio; as descricoes abaixo sao operacionais, baseadas no nome da coluna e nos valores observados.

## Glossario rapido

- `INDE`: indice numerico de desenvolvimento/desempenho educacional do aluno. Quanto maior o valor, melhor o resultado observado no indice.
- `Pedra`: classificacao em faixa de desempenho (categoria), derivada da avaliacao do aluno em cada ano. Exemplos de categorias observadas na base: `Agata`, `Ametista`, `Topazio`, `Quartzo`.
- Relacao entre os dois:
  - `INDE` representa o valor continuo (numero).
  - `Pedra` representa o nivel/faixa (categoria).
  - Em ML, `INDE` costuma ser usado como variavel numerica e `Pedra` como variavel categorial.

## Dicionario (coluna por coluna)

- `RA`: identificador do aluno (registro academico). Abas: 2022, 2023, 2024.
- `Fase`: fase educacional atual do aluno (ex.: `ALFA`, `1A`, `1B`). Abas: 2022, 2023, 2024.
- `Turma`: turma/grupo do aluno. Abas: 2022, 2023, 2024.
- `Nome`: nome do aluno (apenas 2022). Aba: 2022.
- `Nome Anonimizado`: identificador anonimizado do aluno (ex.: `Aluno-1275`). Abas: 2023, 2024.
- `Ano nasc`: ano de nascimento. Aba: 2022.
- `Data de Nasc`: data de nascimento (em formato de data do Excel na base bruta). Abas: 2023, 2024.
- `Idade 22`: idade do aluno no ano de 2022. Aba: 2022.
- `Idade`: idade do aluno no ano de referencia da aba. Abas: 2023, 2024.
- `Gênero`: genero do aluno. Abas: 2022, 2023, 2024.
- `Ano ingresso`: ano de ingresso no programa/escola. Abas: 2022, 2023, 2024.
- `Instituição de ensino`: tipo de instituicao de ensino (ex.: publica, privada). Abas: 2022, 2023, 2024.
- `Escola`: nome da escola do aluno. Aba: 2024.
- `Ativo/ Inativo`: status de atividade do aluno (ex.: `Cursando`). Aba: 2024 (duplicada).

- `Pedra 20`: classificacao `Pedra` no ano de 2020. Abas: 2022, 2023, 2024.
- `Pedra 21`: classificacao `Pedra` no ano de 2021. Abas: 2022, 2023, 2024.
- `Pedra 22`: classificacao `Pedra` no ano de 2022. Abas: 2022, 2023, 2024.
- `Pedra 23`: classificacao `Pedra` no ano de 2023. Abas: 2023, 2024.
- `Pedra 2023`: classificacao `Pedra` no ano de 2023 (coluna anual da aba 2023). Aba: 2023.
- `Pedra 2024`: classificacao `Pedra` no ano de 2024 (coluna anual da aba 2024). Aba: 2024.

- `INDE 22`: score INDE referente a 2022. Abas: 2022, 2023, 2024.
- `INDE 23`: score INDE referente a 2023. Abas: 2023, 2024.
- `INDE 2023`: score INDE do ano de 2023 (coluna anual da aba 2023). Aba: 2023.
- `INDE 2024`: score INDE do ano de 2024 (coluna anual da aba 2024). Aba: 2024.

- `Cg`: componente/sigla de avaliacao (na base observada aparece majoritariamente vazio). Abas: 2022, 2023, 2024.
- `Cf`: componente/sigla de avaliacao (na base observada aparece majoritariamente vazio). Abas: 2022, 2023, 2024.
- `Ct`: componente/sigla de avaliacao (na base observada aparece majoritariamente vazio). Abas: 2022, 2023, 2024.
- `Nº Av`: quantidade de avaliacoes registradas para o aluno. Abas: 2022, 2023, 2024.

- `Avaliador1`: identificador do avaliador 1. Abas: 2022, 2023, 2024.
- `Avaliador2`: identificador do avaliador 2. Abas: 2022, 2023, 2024.
- `Avaliador3`: identificador do avaliador 3. Abas: 2022, 2023, 2024.
- `Avaliador4`: identificador do avaliador 4. Abas: 2022, 2023, 2024.
- `Avaliador5`: identificador do avaliador 5. Aba: 2024.
- `Avaliador6`: identificador do avaliador 6. Aba: 2024.
- `Rec Av1`: recomendacao/comentario associado ao avaliador 1. Abas: 2022, 2023, 2024.
- `Rec Av2`: recomendacao/comentario associado ao avaliador 2. Abas: 2022, 2023, 2024.
- `Rec Av3`: recomendacao/comentario associado ao avaliador 3. Abas: 2022, 2023.
- `Rec Av4`: recomendacao/comentario associado ao avaliador 4. Abas: 2022, 2023.
- `Rec Psicologia`: recomendacao/comentario da area de psicologia. Abas: 2022, 2023, 2024.

- `IAA`: indicador IAA (score numerico). Abas: 2022, 2023, 2024.
- `IEG`: indicador IEG (score numerico). Abas: 2022, 2023, 2024.
- `IPS`: indicador IPS (score numerico). Abas: 2022, 2023, 2024.
- `IPP`: indicador IPP (score numerico). Abas: 2023, 2024.
- `IDA`: indicador IDA (score numerico). Abas: 2022, 2023, 2024.
- `IPV`: indicador IPV (score numerico). Abas: 2022, 2023, 2024.
- `IAN`: indicador IAN (score numerico). Abas: 2022, 2023, 2024.

- `Matem`: nota/desempenho de matematica. Aba: 2022.
- `Mat`: nota/desempenho de matematica (nome abreviado). Abas: 2023, 2024.
- `Portug`: nota/desempenho de portugues. Aba: 2022.
- `Por`: nota/desempenho de portugues (nome abreviado). Abas: 2023, 2024.
- `Inglês`: nota/desempenho de ingles. Aba: 2022.
- `Ing`: nota/desempenho de ingles (nome abreviado). Abas: 2023, 2024.

- `Indicado`: marcador de indicacao (campo categorial/booleano, depende do preenchimento da base). Abas: 2022, 2023, 2024.
- `Atingiu PV`: marcador de atingimento de PV (campo categorial/booleano, depende do preenchimento da base). Abas: 2022, 2023, 2024.
- `Fase ideal`: fase ideal esperada para o aluno (nomenclatura 2022). Aba: 2022.
- `Fase Ideal`: fase ideal esperada para o aluno (nomenclatura 2023/2024). Abas: 2023, 2024.
- `Defas`: medida de defasagem escolar (nomenclatura 2022). Aba: 2022.
- `Defasagem`: medida de defasagem escolar (nomenclatura 2023/2024). Abas: 2023, 2024.

- `Destaque IEG`: marcador de destaque no indicador IEG. Abas: 2022, 2023, 2024.
- `Destaque IDA`: marcador de destaque no indicador IDA. Abas: 2022, 2023, 2024.
- `Destaque IPV`: marcador de destaque no indicador IPV. Abas: 2022, 2023, 2024 (duplicada na aba 2023).

## Sugestao para padronizacao no preprocessing

Antes de treinar modelo, padronizar nomes equivalentes:

- `Matem` -> `Mat`
- `Portug` -> `Por`
- `Inglês` -> `Ing`
- `Fase ideal` -> `Fase Ideal`
- `Defas` -> `Defasagem`
- Tratar colunas duplicadas (`Destaque IPV`, `Ativo/ Inativo`) mantendo apenas uma versao.
