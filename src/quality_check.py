import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("postgresql://postgres:vcxa123@localhost:5432/labeling_db")

# labeling_data 읽기
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

# ✅ DataFrame 변환 후 중복 제거
if errors:
    err_df = pd.DataFrame(errors)

    # image_id + error_type 기준으로만 중복 제거
    err_df = err_df.drop_duplicates(subset=["image_id", "error_type"])

    # --- DB 중복 확인 ---
    existing = pd.read_sql("SELECT image_id, error_type FROM quality_metrics", engine)

    # (image_id, error_type) 조합이 DB에 없을 때만 추가
    merged = err_df.merge(existing, on=["image_id", "error_type"], how="left", indicator=True)
    new_errors = merged[merged["_merge"] == "left_only"].drop(columns=["_merge"])

    if not new_errors.empty:
        new_errors.to_sql("quality_metrics", engine, if_exists="append", index=False)
        print(f"✅ 새로운 오류 {len(new_errors)}건 추가 → quality_metrics 저장 완료")
    else:
        print("✅ 새로운 오류 없음 (DB에 이미 모두 존재)")
else:
    print("✅ 검출된 오류 없음")
