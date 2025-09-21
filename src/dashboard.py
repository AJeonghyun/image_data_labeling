import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import os

st.title("📊 Labeling Quality Dashboard")

# DB 연결
engine = create_engine("postgresql://postgres:vcxa123@localhost:5432/labeling_db")

# 데이터 불러오기
df = pd.read_sql("SELECT * FROM labeling_data", engine)
errors = pd.read_sql("SELECT * FROM quality_metrics", engine)

# --- 클래스 분포 ---
st.subheader("클래스 분포")
st.bar_chart(df['class_name'].value_counts())

# --- 오류 유형 ---
st.subheader("오류 유형 테이블")
st.dataframe(errors)

# --- 오류 이미지 ---
st.subheader("오류 이미지 미리보기")

# quality_metrics 와 labeling_data 조인 (image_id 기준)
merged = errors.merge(df[['image_id', 'image_path']], on='image_id', how='left')

merged_unique = merged.drop_duplicates(subset=["image_id"])
for _, row in merged_unique.iterrows():
    st.markdown(f"**Image ID:** {row['image_id']} | **Error:** {row['error_type']} | **Detail:** {row.get('error_detail','')}")
    if pd.notna(row['image_path']) and os.path.exists(row['image_path']):
        st.image(row['image_path'], width=400)
    else:
        st.warning(f"이미지를 찾을 수 없음: {row['image_path']}")
