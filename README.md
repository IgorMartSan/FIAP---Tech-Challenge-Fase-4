# FIAP - Tech Challenge Fase 4

## Checklist Macro do Projeto

### 1. Planejamento e Contexto
- [ ] Definir problema de negócio e objetivo preditivo (risco de defasagem escolar)
- [ ] Mapear dados disponíveis (2022, 2023, 2024) e critérios de sucesso
- [ ] Definir stack e padrão de organização do projeto

### 2. Dados e Modelagem
- [ ] Construir pipeline de dados (preprocessamento + engenharia de atributos)
- [ ] Treinar e validar modelo com métrica justificada para produção
- [ ] Serializar modelo treinado (`pickle` ou `joblib`)

### 3. Engenharia de Software e MLOps
- [ ] Modularizar código em componentes reutilizáveis (`src/`, serviços, utilitários)
- [ ] Implementar API de predição (`/predict`) com Flask ou FastAPI
- [ ] Containerizar solução com Docker (`Dockerfile` + execução local)
- [ ] Realizar deploy local ou em nuvem e garantir disponibilidade da API

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
