import pandas as pd
from aa_preprocessing.load_data import load_raw_data

file_path = "/home/igor/Projetos/FIAP---Tech-Challenge-Fase-4/BASE DE DADOS PEDE 2024 - DATATHON.xlsx"
sheets_name = ["PEDE2022", "PEDE2023", "PEDE2024"]




def main() -> None:
   
    # Carregar os dados
    
    df_2022 = load_raw_data(file_path=file_path, sheet_name="PEDE2022")
    df_2023 = load_raw_data(file_path=file_path, sheet_name="PEDE2023")
    df_2024 = load_raw_data(file_path=file_path, sheet_name="PEDE2024")

    print(f"PEDE2022: {df_2022.shape[0]} linhas x {df_2022.shape[1]} colunas")
    print(f"PEDE2023: {df_2023.shape[0]} linhas x {df_2023.shape[1]} colunas")
    print(f"PEDE2024: {df_2024.shape[0]} linhas x {df_2024.shape[1]} colunas")

    datasets = {
        "PEDE2022": df_2022,
        "PEDE2023": df_2023,
        "PEDE2024": df_2024,
    }




if __name__ == "__main__":
    main()
