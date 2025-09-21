from fastapi import FastAPI
import pandas as pd
from sqlalchemy import create_engine

app = FastAPI()
engine = create_engine("postgresql://user:password@localhost:5432/labeling_db")

@app.get("/metrics")
def get_metrics():
    df = pd.read_sql("SELECT * FROM labeling_data", engine)
    total = len(df)
    classes = df['class_name'].value_counts().to_dict()
    return {"total_labels": total, "class_distribution": classes}

@app.get("/errors")
def get_errors():
    df = pd.read_sql("SELECT * FROM quality_metrics", engine)
    return df.to_dict(orient="records")
