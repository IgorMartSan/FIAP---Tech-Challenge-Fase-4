# Análise de Tabelas e Colunas (`arquivos/`)

Este documento resume os arquivos tabulares encontrados em `arquivos/` e descreve as colunas por bloco funcional.

Inventário completo (todas as tabelas e cabeçalhos):
- [inventario_colunas_tabelas.csv](/home/igor/Projetos/FIAP---Tech-Challenge-Fase-4/arquivos/inventario_colunas_tabelas.csv)

## 1) Tabela principal do Datathon (2022-2024)

Arquivo:
- `arquivos/BASE DE DADOS PEDE 2024 - DATATHON.xlsx`

Abas:
- `PEDE2022` (42 colunas)
- `PEDE2023` (48 colunas)
- `PEDE2024` (50 colunas)

Descrição das colunas (por grupo):
- Identificação e contexto: `RA`, `Nome/Nome Anonimizado`, `Gênero`, `Turma`, `Ano ingresso`, `Instituição de ensino`, `Escola`, `Ativo/ Inativo`.
- Perfil escolar: `Fase`, `Fase Ideal/Fase ideal`, `Defasagem/Defas`.
- Histórico de classificação: `Pedra 20`, `Pedra 21`, `Pedra 22`, `Pedra 23`, `Pedra 2023`, `Pedra 2024`.
- Histórico de score: `INDE 22`, `INDE 23`, `INDE 2023`, `INDE 2024`.
- Indicadores de desempenho: `IAA`, `IEG`, `IPS`, `IPP`, `IDA`, `IPV`, `IAN`.
- Notas de disciplina: `Matem/Mat`, `Portug/Por`, `Inglês/Ing`.
- Avaliação humana: `Avaliador1..6`, `Rec Av1..4`, `Rec Psicologia`, `Nº Av`.
- Sinais operacionais: `Indicado`, `Atingiu PV`, `Destaque IEG/IDA/IPV`.

Observações:
- Há duplicidade de colunas em algumas abas (`Destaque IPV` em 2023 e `Ativo/ Inativo` em 2024).
- Há variação de nomenclatura entre anos (`Matem` vs `Mat`, `Defas` vs `Defasagem`).

## 2) Base antiga consolidada (2020-2022)

Arquivos:
- `arquivos/Bases antigas/PEDE_PASSOS_DATASET_FIAP.xlsx`
- `arquivos/Bases antigas/PEDE_PASSOS_DATASET_FIAP.csv`

Descrição:
- Base consolidada com colunas sufixadas por ano (`_2020`, `_2021`, `_2022`).
- O CSV está separado por `;`.

Blocos de colunas:
- Contexto do aluno: `NOME`, `IDADE_ALUNO_2020`, `ANO_INGRESSO_2022`, `INSTITUICAO_ENSINO_ALUNO_2020/2021`.
- Progresso e risco: `FASE_*`, `NIVEL_IDEAL_*`, `DEFASAGEM_2021`.
- Desempenho: `INDE_*`, `INDE_CONCEITO_2020`, `PEDRA_*`, `IAA/IEG/IPS/IDA/IPP/IPV/IAN`.
- Notas e avaliações: `NOTA_PORT_2022`, `NOTA_MAT_2022`, `NOTA_ING_2022`, `QTD_AVAL_2022`, `REC_EQUIPE_*`, `REC_AVA_*`.
- Sinais de decisão: `PONTO_VIRADA_*`, `BOLSISTA_2022`, `INDICADO_BOLSA_2022`.

## 3) Base relacional antiga em ZIP

Arquivo:
- `arquivos/Bases antigas/Base de dados - Passos Mágicos.zip`

Resumo:
- 68 CSV internos (originais e merges).
- Modelo relacional acadêmico/administrativo com chaves `Id*`.

Principais famílias de tabelas:
- `TbAluno*`: cadastro de aluno, vínculo com turma, histórico de turma, observações.
- `TbTurma*`: dados de turma, professores, situação do aluno na turma.
- `TbFase*`: estrutura de fases/notas, notas por aluno e disciplina.
- `TbDiario*`: aulas, diário de classe e frequência.
- `TbHistorico*`: histórico escolar e notas finais.
- `TbMeta*`: metas, conceitos e situação por disciplina.
- `TbProfessor*`: cadastro e vínculo docente.
- `TbResponsavel*`: cadastro de responsáveis e vínculos.
- `Outras tabelas/*`: dimensões de apoio (`TbPais`, `TbMunicipio`, `TbDisciplina`, etc.).

Padrão das colunas (convenções):
- `Id*`: chaves primárias/estrangeiras.
- `Nome*`, `Descricao*`: campos descritivos.
- `Data*`: datas de evento/cadastro.
- `St*`: status/flags booleanas.
- `Codigo*`, `Sigla*`: códigos de integração/classificação.

## 4) Arquivos não-tabulares

Também existem documentos de apoio em PDF/DOCX/IPYNB, úteis para contexto, mas sem cabeçalho tabular direto:
- `Dicionário Dados Datathon.pdf`
- `Relatórios PEDE*.pdf`
- `desvendando_passos.pdf`
- `Links adicionais da passos.docx`
- `PEDE_ Pontos importantes.docx`
- `DATATHON-PASSOS-MÁGICOS.ipynb`

## 5) Como consultar rapidamente as colunas

Use o inventário CSV para filtrar por arquivo/aba:
- `fonte`: `csv`, `xlsx` ou `zip_csv`
- `arquivo`: caminho físico
- `tabela_ou_aba`: nome da aba (xlsx) ou tabela interna (zip)
- `qtd_colunas`: total
- `colunas`: lista completa do cabeçalho
