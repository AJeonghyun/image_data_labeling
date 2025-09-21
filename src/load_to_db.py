# src/load_to_db.py
import pandas as pd
from sqlalchemy import create_engine

csv_path = "data/raw/labels_openimages_pascal.csv"
engine = create_engine("postgresql://postgres:vcxa123@localhost:5432/labeling_db")

df = pd.read_csv(csv_path)
df.to_sql("labeling_data", engine, if_exists="append", index=False)
print("✅ loaded rows:", len(df))
