from pathlib import Path
from typing import Optional

import pandas as pd


def load_raw_data(file_path: str, sheet_name: Optional[str] = None) -> pd.DataFrame:
    """
    Carrega dados de uma aba do arquivo Excel.

    Args:
        file_path: Caminho absoluto ou relativo para o arquivo Excel.
        sheet_name: Nome da aba. Se None, usa a primeira aba.

    Returns:
        DataFrame com os dados carregados.
    """
    target = Path(file_path)

    if not target.is_absolute():
        target = Path(__file__).resolve().parents[2] / target

    if not target.exists():
        raise FileNotFoundError(f"Arquivo de dados nao encontrado: {target}")

    return pd.read_excel(target, sheet_name=sheet_name)
