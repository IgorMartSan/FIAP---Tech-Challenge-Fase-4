import pandas as pd


def print_student_participation_stats(df: pd.DataFrame) -> None:
    """
    Exibe estatísticas de participação dos alunos entre os anos.
    """
    required_columns = {"RA", "DERIV_ANO_REFERENCIA"}
    if not required_columns.issubset(df.columns):
        print("\nEstatística de participação não executada: colunas RA/DERIV_ANO_REFERENCIA ausentes.")
        return

    participation = (
        df[["RA", "DERIV_ANO_REFERENCIA"]]
        .dropna()
        .drop_duplicates()
        .groupby("RA")["DERIV_ANO_REFERENCIA"]
        .nunique()
    )
    total_alunos = int(participation.shape[0])
    alunos_3_anos = int((participation == 3).sum())

    print("\nParticipação de alunos por ano:")
    print(f"Total de alunos únicos: {total_alunos}")
    print(f"Alunos que participaram dos 3 anos: {alunos_3_anos}")
