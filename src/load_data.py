import pandas as pd
import psycopg2
from sqlalchemy import create_engine

engine = create_engine("postgresql://user:password@localhost:5432/labeling_db")

df = pd.read_csv("data/sample_labels.csv")
df.to_sql("labeling_data", engine, if_exists="append", index=False)
print("✅ CSV 데이터를 DB에 적재 완료")
