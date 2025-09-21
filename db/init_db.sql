CREATE TABLE IF NOT EXISTS labeling_data (
    id SERIAL PRIMARY KEY,
    image_id TEXT NOT NULL,
    class_name TEXT NOT NULL,
    x1 INT,
    y1 INT,
    x2 INT,
    y2 INT,
    annotator TEXT,
    created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE IF NOT EXISTS quality_metrics (
    id SERIAL PRIMARY KEY,
    image_id TEXT NOT NULL,
    error_type TEXT,
    error_detail TEXT,
    created_at TIMESTAMP DEFAULT now()
);
