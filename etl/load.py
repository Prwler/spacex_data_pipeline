# etl/load.py
from sqlalchemy import create_engine, text
import pandas as pd
from config import DB_CONNECTION_STRING

engine = create_engine(DB_CONNECTION_STRING)


def table_exists(conn, table_name: str) -> bool:
    """Return True if table exists in public schema."""
    result = conn.execute(text(
        "SELECT to_regclass(:t)"
    ), {"t": f"public.{table_name}"}).scalar()
    return result is not None


def load_table(df: pd.DataFrame, table_name: str):
    """
    Safely loads df into table_name:
    - If the table doesn't exist, create an empty table then insert rows.
    - If the table exists, TRUNCATE CASCADE then append new rows.
    """

    # Convert Python lists -> Postgres array literal
    for col in df.columns:
        if df[col].apply(lambda x: isinstance(x, list)).any():
            df[col] = df[col].apply(
                lambda x: "{" + ",".join([str(i) for i in x]) + "}" if isinstance(x, list) else x
            )

    with engine.begin() as conn:
        if not table_exists(conn, table_name):
            # Create an empty table with the correct columns (no drop because it doesn't exist)
            # to_sql with if_exists='replace' is safe here because table is absent.
            df.head(0).to_sql(table_name, conn, if_exists="replace", index=False)
        else:
            # Table exists: safely clear its rows while preserving the schema and constraints
            conn.execute(text(f"TRUNCATE TABLE {table_name} CASCADE"))

        # Append new rows
        df.to_sql(table_name, conn, if_exists="append", index=False)
