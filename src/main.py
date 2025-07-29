# src/main.py
from preprocess import preprocess_text, preprocess_image
from classify_summarize import classify_and_style_transform, summarize_text
from detect_ocr import detect_objects_and_ocr
from agentica_api import send_to_agentica

def process_complaint(input_data: str, is_image: bool = False):
    """텍스트 또는 이미지 민원을 처리하여 Agentica에 전송."""
    if is_image:
        # 이미지 민원 처리
        image = preprocess_image(input_data)
        ocr_results = detect_objects_and_ocr(image)
        visual_summary = "\n".join([f"{r['class_name']}: {r['text']}" for r in ocr_results])
        classification = "이미지 기반 민원"
        text_summary = "이미지에서 추출한 민원 정보 요약"
    else:
        # 텍스트 민원 처리
        clean_text = preprocess_text(input_data)
        result = classify_and_style_transform(clean_text)
        classification = result["classification"]
        transformed_text = result["transformed"]
        text_summary = summarize_text(transformed_text)
        visual_summary = ""

    complaint_data = {
        "classification": classification,
        "summary_text": text_summary,
        "visual_summary": visual_summary
    }

    response = send_to_agentica(complaint_data)
    if response.status_code == 200:
        print("민원 접수 완료:", response.json())
    else:
        print("민원 접수 실패:", response.text)

if __name__ == "__main__":
    # 텍스트 민원 테스트
    process_complaint("불법 주차 차량을 신고합니다.", is_image=False)
    # 이미지 민원 테스트 (이미지 경로 수정)
    # process_complaint("./data/images/sample.jpg", is_image=True)
