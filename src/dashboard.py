import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

st.title("📊 Labeling Quality Dashboard")

engine = create_engine("postgresql://user:password@localhost:5432/labeling_db")
df = pd.read_sql("SELECT * FROM labeling_data", engine)

st.subheader("클래스 분포")
st.bar_chart(df['class_name'].value_counts())

st.subheader("오류 유형")
errors = pd.read_sql("SELECT * FROM quality_metrics", engine)
st.dataframe(errors)
