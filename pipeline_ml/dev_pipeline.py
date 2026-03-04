from pathlib import Path
import pandas as pd
from utils.load_data import load_raw_data
from utils.print_utils import print_student_participation_stats
from aa_preprocessing.preprocessing_data import (
    ajustar_tipos_numericos,
    normalizar_colunas_categoricas,
    normalizar_valores_ausentes,
    organizar_colunas_para_saida,
    padronizar_nomes_e_remover_duplicadas,
    renomear_colunas_equivalentes,
    validar_transferencia_colunas_equivalentes,
)
from ba_feature_engineering.feature_engineering import (
    COLUNAS_DERIVADAS,
    gerar_atributos_derivados,
    organizar_colunas_saida_feature_engineering,
    unificar_alvos_do_ano,
)

TRAINING_IMPORT_ERROR = None

file_path = "arquivos_do_projeto/BASE DE DADOS PEDE 2024 - DATATHON.xlsx"
sheets_name = ["PEDE2022", "PEDE2023", "PEDE2024"]


def main() -> None:
    # =========================
    # 1) Carregamento das abas
    # =========================
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

    # ============================================
    # 2) Merge bruto das abas (antes de qualquer tratamento)
    # ============================================
    output_dir = Path(__file__).resolve().parent / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    raw_merged = pd.concat(
        [df.assign(ABA_ORIGEM=sheet) for sheet, df in datasets.items()],
        ignore_index=True,
        sort=False,
    )
    raw_merged = padronizar_nomes_e_remover_duplicadas(raw_merged)
    raw_merged = renomear_colunas_equivalentes(raw_merged)
    raw_output_file = output_dir / "dados_merge_abas_bruto.csv"
    raw_merged.to_csv(raw_output_file, index=False)
    print(f"\nCSV bruto (merge das abas) salvo em: {raw_output_file}")

    # ===========================================
    # 3) Lista de features criadas no tratamento
    # ===========================================
    featured_datasets = {}

    # ==========================================================
    # 4) Preprocessing por ano (funcao por funcao) + engineering
    # ==========================================================
    for sheet, df in datasets.items():
        year = int(sheet[-4:])

        # Etapa 1: Preprocessing (limpeza e padronização)
        preprocessado = padronizar_nomes_e_remover_duplicadas(df)
        antes_alias = preprocessado.copy()
        preprocessado = renomear_colunas_equivalentes(preprocessado)
        inconsistencias_alias = validar_transferencia_colunas_equivalentes(antes_alias, preprocessado)
        if inconsistencias_alias:
            raise ValueError(f"Inconsistencias de transferencia de aliases em {sheet}: {inconsistencias_alias}")
        preprocessado = ajustar_tipos_numericos(preprocessado)
        preprocessado = normalizar_colunas_categoricas(preprocessado)
        preprocessado = normalizar_valores_ausentes(preprocessado)
        preprocessado = organizar_colunas_para_saida(preprocessado)

        # Etapa 2: Feature engineering (geração de atributos derivados)
        featured = unificar_alvos_do_ano(preprocessado, ano_referencia=year)
        featured = gerar_atributos_derivados(featured, ano_referencia=year)
        featured = organizar_colunas_saida_feature_engineering(featured)

        # Etapa 3: Armazenar resultado por aba
        featured_datasets[sheet] = featured

        # Etapa 4: Preview das colunas derivadas
        print(f"{sheet} (feature engineering): {featured.shape[0]} linhas x {featured.shape[1]} colunas")
        existing_cols = [col for col in COLUNAS_DERIVADAS if col in featured.columns]
        if existing_cols:
            print(f"\nPreview de features geradas em {sheet}:")
            print(featured[existing_cols].head(5).to_string(index=False))

    # ==================================
    # 5) Consolidacao entre todos os anos
    # ==================================
    df_featured_all_years = pd.concat(featured_datasets.values(), ignore_index=True, sort=False)
    df_featured_all_years = organizar_colunas_saida_feature_engineering(df_featured_all_years)
    colunas_ordenacao = [c for c in ["RA", "DERIV_ANO_REFERENCIA"] if c in df_featured_all_years.columns]
    if colunas_ordenacao:
        df_featured_all_years = df_featured_all_years.sort_values(
            by=colunas_ordenacao,
            kind="mergesort",
            na_position="last",
        ).reset_index(drop=True)
    print(
        f"Dataset consolidado: {df_featured_all_years.shape[0]} linhas x "
        f"{df_featured_all_years.shape[1]} colunas"
    )
    print_student_participation_stats(df_featured_all_years)

    # ==========================================
    # 6) Exibicao final das features consolidadas
    # ==========================================
    existing_created_columns = [col for col in COLUNAS_DERIVADAS if col in df_featured_all_years.columns]
    print(f"Features geradas: {existing_created_columns}")
    if existing_created_columns:
        print("\nPreview consolidado das features geradas:")
        print(df_featured_all_years[existing_created_columns].head(10).to_string(index=False))

    # ==================================
    # 7) Exportacao do dataset para CSV
    # ==================================
    output_file = output_dir / "dados_feature_engineering_consolidado.csv"
    df_featured_all_years.to_csv(output_file, index=False)
    print(f"\nCSV salvo em: {output_file}")




    # ============================================
    # 8) Treino rapido usando funcao configuravel
    # ============================================
    if TRAINING_IMPORT_ERROR is None:
        try:
            train_df = build_target(df_featured_all_years)
            X, _, _ = select_features(train_df)
            train_config = {
                "target_column": "RISCO_DEFASAGEM",
                "feature_columns": X.columns.tolist(),
                "group_column": "RA",
                "test_size": 0.2,
                "validation_size": 0.2,
                "random_state": 42,
                "verbose": True,
                "model_params": {
                    "n_estimators": 300,
                    "min_samples_leaf": 2,
                    "class_weight": "balanced",
                },
            }
            training_result = train_model_from_config(df=train_df, config=train_config)
            pipeline = training_result["pipeline"]
            validation_metrics = training_result["validation_metrics"]
            test_metrics = training_result["test_metrics"]
            save_training_artifacts(
                pipeline,
                {
                    "validation": validation_metrics,
                    "test": test_metrics,
                },
            )

            print("\nTreino executado dentro do dev_pipeline.")
            print(
                f"Amostras de treino: {training_result['X_train_shape'][0]} | "
                f"validacao: {training_result['X_validation_shape'][0]} | "
                f"teste: {training_result['X_test_shape'][0]}"
            )
            print(f"Target: {training_result['target_column']}")
            print(f"Features usadas ({len(training_result['feature_columns'])}): "
                f"{training_result['feature_columns']}"
            )
            if training_result["removed_leakage_features"]:
                print(
                    f"Features removidas por vazamento: "
                    f"{training_result['removed_leakage_features']}"
                )
            print(f"Modelo salvo em: {MODEL_PATH}")
            print(f"Métricas salvas em: {METRICS_PATH}")
            print(
                f"Validacao - F1: {validation_metrics['f1']:.4f} | "
                f"Precision: {validation_metrics['precision']:.4f} | "
                f"Recall: {validation_metrics['recall']:.4f}"
            )
            print(
                f"Teste - F1: {test_metrics['f1']:.4f} | "
                f"Precision: {test_metrics['precision']:.4f} | "
                f"Recall: {test_metrics['recall']:.4f}"
            )
        except Exception as exc:
            print(f"\nTreino nao executado no dev_pipeline por erro de configuracao: {exc}")
    else:
        print(f"\nTreino nao executado no dev_pipeline por dependencia ausente: {TRAINING_IMPORT_ERROR}")



if __name__ == "__main__":
    main()
