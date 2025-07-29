# src/detect_ocr.py
from ultralytics import YOLO
import pytesseract
import yaml
import numpy as np
from PIL import Image
from pathlib import Path
from typing import List, Dict

# config.yaml 읽기
CONFIG_PATH = Path(__file__).resolve().parent.parent / "config.yaml"
with open(CONFIG_PATH, encoding="utf-8") as f:
    config = yaml.safe_load(f)

# 모델 로딩
yolo_model = YOLO("/home/tenant/yyj1010/study/agentica/yolov8l.pt") 

# 필요시 클래스 명 리스트 수정
CLASS_NAMES = ["Signboard", "Document", "Vehicle", "Person", "Infrastructure"]

def detect_objects_and_ocr(image: np.ndarray, conf: float = 0.3) -> List[Dict]:
    """YOLOv8로 객체 탐지 후 각 영역에 대해 OCR 수행."""
    results = yolo_model(image, conf=conf)
    ocr_outputs = []
    for result in results:
        for bbox, cls_id in zip(result.boxes.xyxy, result.boxes.cls):
            x1, y1, x2, y2 = map(int, bbox)
            cropped_img = Image.fromarray(image).crop((x1, y1, x2, y2))
            text = pytesseract.image_to_string(cropped_img, lang="kor+eng").strip()
            ocr_outputs.append({
                "class_id": int(cls_id),
                "class_name": CLASS_NAMES[int(cls_id)] if int(cls_id) < len(CLASS_NAMES) else f"Class_{cls_id}",
                "text": text
            })
    return ocr_outputs
