from fastapi import FastAPI, UploadFile, File
import numpy as np
from PIL import Image
from detect_ocr import detect_objects_and_ocr   # 같은 폴더의 모듈

app = FastAPI(title="VisionService")

@app.post("/vision/analyze")
async def analyze(file: UploadFile = File(...)):
    """객체 검출 + OCR 후 결과 반환"""
    img = np.array(Image.open(file.file).convert("RGB"))
    return {"ocr": detect_objects_and_ocr(img)}
