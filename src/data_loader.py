import pandas as pd
from pathlib import Path
import os
from src.database import get_db_connection


class DataLoader:
    def __init__(self):
        self.engine = get_db_connection()
        self.processed_path = Path("data/processed")
        self.raw_cache_path = Path("data/raw_cache")
        self.processed_path.mkdir(parents=True, exist_ok=True)
        self.raw_cache_path.mkdir(parents=True, exist_ok=True)

    def load_with_cache(self, query: str, cache_name: str) -> pd.DataFrame:

        file_path = self.raw_cache_path / f"{cache_name}.parquet"

        if file_path.exists():
            print(f"Found locally: {file_path}. From disk...")
            return pd.read_parquet(file_path)

        print(f"Dowloading from SQL")
        print(f"Query: {query}")
        df = pd.read_sql(query, self.engine)

        print(f"Saving to: {file_path}")
        df.to_parquet(file_path, index=False)

        return df

    def save_processed(self, df: pd.DataFrame, name: str):
        file_path = self.processed_path / f"{name}.parquet"
        df.to_parquet(file_path, index=False)
        print(f"Saved snapshot in : {file_path}")

def temporal_train_test_split(df: pd.DataFrame, test_step_start: int = 600):
    print(f"Dividing dataset (Cutoff step: {test_step_start})...")

    df = df.sort_values(by='step')

    train = df[df['step'] < test_step_start].copy()
    test = df[df['step'] >= test_step_start].copy()

    print(f" Training set: {train.shape[0]} rows")
    print(f" Test set:    {test.shape[0]} rows")

    return train, test