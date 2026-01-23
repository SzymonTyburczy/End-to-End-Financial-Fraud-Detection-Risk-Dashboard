import sys
import os
import pandas as pd
from pathlib import Path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from src.data_loader import DataLoader, temporal_train_test_split
from src.features import FeatureEngineer
from src.trainer import FraudTrainer
from src.evaluator import ModelEvaluator


def run_pipeline():
    print("🚀 --- START: Enterprise Fraud Detection Pipeline ---")
    loader = DataLoader()

    query = """
    SELECT * FROM transactions 
    WHERE type IN ('TRANSFER', 'CASH_OUT')
    """


    raw_df = loader.load_with_cache(query, cache_name="raw_transactions_filtered")

    print(f"Data loaded. Number of rows: {len(raw_df)}")

    print("🛠️  Data preprocessing and feature engineering...")
    fe = FeatureEngineer()

    processed_df = fe.preprocess(raw_df)

    if 'isFraud' not in processed_df.columns:
        raise ValueError("❌ ERROR: Lost 'isFraud' column during preprocessing!")

    train_df, test_df = temporal_train_test_split(processed_df, test_step_start=600)


    drop_cols = ['isFraud', 'step']

    X_train = train_df.drop(columns=drop_cols)
    y_train = train_df['isFraud']

    X_test = test_df.drop(columns=drop_cols)
    y_test = test_df['isFraud']

    trainer = FraudTrainer()

    custom_params = {
        'n_estimators': 300,
        'max_depth': 8,
        'learning_rate': 0.05
    }

    model = trainer.train(X_train, y_train, X_test, y_test, params=custom_params)

    print("\n📊 --- Starting full evaluation ---")
    evaluator = ModelEvaluator(model)

    sample_size = min(1000, len(X_test))
    evaluator.explain_with_shap(X_test.iloc[:sample_size])

    trainer.save_model("models/production_model.pkl")

    print("\n🎉 --- Pipeline completed successfully! ---")


if __name__ == "__main__":
    run_pipeline()