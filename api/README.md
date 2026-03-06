# API - Defasagem Prediction

## Requisitos
- Python 3.10+
- `uv` instalado

## Executar a API (uv)
```bash
cd /home/igor/Projetos/FIAP---Tech-Challenge-Fase-4/api
uv sync
uv run python src/main.py
```

A API sobe em `http://0.0.0.0:8000`.

## Executar testes
```bash
cd /home/igor/Projetos/FIAP---Tech-Challenge-Fase-4/api
uv sync --dev
uv run pytest
```

## Cobertura de testes
```bash
cd /home/igor/Projetos/FIAP---Tech-Challenge-Fase-4/api
uv sync --dev
uv run pytest --cov=src --cov-report=term-missing --cov-fail-under=80
```
