import pandas as pd
from sqlalchemy import create_engine
import os
from pathlib import Path
from src.config import settings


def load_csv_to_sql(csv_filename="fraud_dataset.csv"):
    """
    Loading into PostgreSQL in chunks.
    """
    base_dir = Path(__file__).resolve().parent.parent
    csv_path = base_dir / "data" / "raw" / csv_filename

    if not csv_path.exists():
        print(f"No file found: {csv_path}")
        return

    engine = create_engine(settings.db_url)
    print(f"Starting migration {csv_filename} to PostgreSQL")

    chunk_size = 100000

    try:
        for i, chunk in enumerate(pd.read_csv(csv_path, chunksize=chunk_size)):
            mode = 'replace' if i == 0 else 'append'

            chunk.to_sql('transactions', engine, if_exists=mode, index=False)

            if (i + 1) % 5 == 0:
                print(f"Loaded {(i + 1) * chunk_size / 1_000_000 :.1f} mln rows")

        print("Successfully migrated to PostgreSQL.")

    except Exception as e:
        print(f"Error occurred during loading phase: {e}")

if __name__ == "__main__":
    load_csv_to_sql()