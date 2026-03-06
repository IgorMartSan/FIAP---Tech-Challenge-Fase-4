   

from ca_train.train_model import BinaryTrainingConfig, BinaryDefasagemTrainer

 # ---------------------------------------------------------
    # 6) configurar treino
    # ---------------------------------------------------------
    model_output_path = "data/model/model_defasagem_fc_binario_lgbm.joblib"

    train_config = BinaryTrainingConfig(
        train_size=0.70,                    # 70% treino
        val_size=0.15,                      # 15% validação
        test_size=0.15,                     # 15% teste
        random_state=42,                    # reprodutibilidade
        stratify=True,                      # mantém proporção das classes
        id_cols=("RA",),                    # remove RA do treino
        leak_cols=("Defasagem",),           # remove coluna que gera leakage
        target_rule="negative_is_1",        # 1 se Defasagem futura < 0
        fill_numeric_with_median=True,      # preenche NaN numérico com mediana
        fill_categorical_with_missing=True, # preenche NaN categórico com "missing"
        remove_constant_columns=True,       # remove colunas constantes
        n_estimators=5000,                  # número máximo de árvores
        learning_rate=0.03,                 # taxa de aprendizado
        num_leaves=31,                      # folhas por árvore
        min_data_in_leaf=10,                # mínimo de exemplos por folha
        subsample=0.9,                      # fração de linhas por árvore
        colsample_bytree=0.9,               # fração de colunas por árvore
        reg_lambda=1.0,                     # regularização L2
        force_col_wise=True,                # otimização LightGBM
        verbosity=-1,                       # sem logs excessivos
        output_model_path=model_output_path # onde salvar o modelo
    )

    # ---------------------------------------------------------
    # 7) treinar modelo
    # ---------------------------------------------------------
    trainer = BinaryDefasagemTrainer(
        dataset=dataset_final,
        target_col="Defasagem futura",
        config=train_config,
    )

    result = trainer.train()

    # ---------------------------------------------------------
    # 8) exibir resultados
    # ---------------------------------------------------------
    print("\n==== SHAPES ====")
    print(result["shapes"])

    print("\n==== MÉTRICAS ====")
    print("Accuracy:", result["metrics"]["accuracy"])
    print("F1:", result["metrics"]["f1"])
    print(result["metrics"]["report"])

    print("\n==== FEATURE IMPORTANCE ====")
    print(result["feature_importance"].head(15))

    # opcional: salvar feature importance
    fi_path = "data/model/feature_importance.csv"
    result["feature_importance"].to_csv(fi_path, index=False)
    print(f"\n[OK] feature importance salva em: {fi_path}")