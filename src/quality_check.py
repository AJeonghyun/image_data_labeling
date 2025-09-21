import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("postgresql://user:password@localhost:5432/labeling_db")

df = pd.read_sql("SELECT * FROM labeling_data", engine)

errors = []

# 1. 좌표 오류 (bbox 잘못된 값)
invalid_bboxes = df[(df['x1'] >= df['x2']) | (df['y1'] >= df['y2'])]
for _, row in invalid_bboxes.iterrows():
    errors.append({"image_id": row['image_id'], "error_type": "bbox_invalid"})

# 2. 클래스 불균형 체크
class_counts = df['class_name'].value_counts(normalize=True)
imbalanced_classes = class_counts[class_counts < 0.05]
for cls in imbalanced_classes.index:
    errors.append({"image_id": None, "error_type": "class_imbalance", "error_detail": cls})

print(f"✅ 검출된 오류 {len(errors)}건")
