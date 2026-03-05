import pandas as pd
from typing import Tuple

import pandas as pd
from typing import Dict
import re


def read_pede_excel(path: str):
    sheets = pd.read_excel(path, sheet_name=None)

    datasets = {}
    for sheet_name, df in sheets.items():
        match = re.search(r"20\d{2}", str(sheet_name))
        if match:
            ano = int(match.group())
            df = df.copy()
            df["Ano"] = ano
            datasets[str(ano)] = df

    return datasets