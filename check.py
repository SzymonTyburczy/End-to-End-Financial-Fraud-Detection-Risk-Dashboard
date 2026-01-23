import pandas as pd
from sqlalchemy import create_engine, inspect
from src.config import settings

engine = create_engine(settings.db_url)
inspector = inspect(engine)

tables = inspector.get_table_names()
print(f"Tbale in database'{settings.DB_NAME}': {tables}")

if "transactions" in tables:
    count = pd.read_sql("SELECT COUNT(*) FROM transactions", engine).iloc[0, 0]
    print(f"📊 Table 'transactions' exists and has  {count} rows.")
else:

    print("Error: No such table 'transactions'.")