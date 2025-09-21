import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("postgresql://postgres:vcxa123@localhost:5432/labeling_db")

df = pd.read_sql("SELECT * FROM labeling_data", engine)

errors = []

# 1. 좌표 오류 (bbox 잘못된 값)
invalid_bboxes = df[(df['x1'] >= df['x2']) | (df['y1'] >= df['y2'])]
for _, row in invalid_bboxes.iterrows():
    errors.append({
        "image_id": row['image_id'],
        "error_type": "bbox_invalid",
        "error_detail": f"{row['x1']},{row['y1']},{row['x2']},{row['y2']}"
    })

# 2. 클래스 불균형 체크 (비율 < 25%)
class_counts = df['class_name'].value_counts(normalize=True)
imbalanced_classes = class_counts[class_counts < 0.25]

for cls in imbalanced_classes.index:
    subset = df[df['class_name'] == cls]
    for _, row in subset.iterrows():
        errors.append({
            "image_id": row['image_id'],
            "error_type": "class_imbalance",
            "error_detail": f"class={cls}, count={len(subset)}"
        })

# ✅ DB 저장
if errors:
    err_df = pd.DataFrame(errors)
    err_df.to_sql("quality_metrics", engine, if_exists="append", index=False)
    print(f"✅ 검출된 오류 {len(errors)}건 → quality_metrics에 저장 완료")
else:
    print("✅ 검출된 오류 없음")
