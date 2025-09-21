# src/concat_pascal_to_csv.py
import os, glob
import xml.etree.ElementTree as ET
import pandas as pd

BASE = "openimages_data"
rows = []

for class_dir in ["Car","Person","Traffic light","Bus"]:
    xml_dir = os.path.join(BASE, class_dir, "pascal")
    img_dir = os.path.join(BASE, class_dir, "images")
    for xml in glob.glob(os.path.join(xml_dir, "*.xml")):
        tree = ET.parse(xml); root = tree.getroot()
        filename = root.findtext("filename")
        path = os.path.join(img_dir, filename)  # 이미지 절대/상대 경로
        image_id = os.path.splitext(filename)[0]
        size = root.find("size")
        if size is None: 
            width = height = None
        else:
            width  = int(size.findtext("width"))
            height = int(size.findtext("height"))
        for obj in root.findall("object"):
            name = obj.findtext("name")
            bnd  = obj.find("bndbox")
            x1,y1 = int(float(bnd.findtext("xmin"))), int(float(bnd.findtext("ymin")))
            x2,y2 = int(float(bnd.findtext("xmax"))), int(float(bnd.findtext("ymax")))
            rows.append({
                "image_id": image_id,
                "image_path": path,
                "class_name": name,
                "x1": x1, "y1": y1, "x2": x2, "y2": y2,
                "width": width, "height": height,
                "annotator": "openimages"  
            })

df = pd.DataFrame(rows)
os.makedirs("data/raw", exist_ok=True)
df.to_csv("data/raw/labels_openimages_pascal.csv", index=False)
print("✅ to CSV:", len(df))
