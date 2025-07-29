# src/classify_summarize.py
import openai
import yaml
from pathlib import Path

# config.yaml 절대 경로 계산
CONFIG_PATH = Path(__file__).resolve().parent.parent / "config.yaml"
with open(CONFIG_PATH, encoding="utf-8") as f:
    config = yaml.safe_load(f)

openai.api_key = config["openai"]["api_key"]

def classify_and_style_transform(text: str, style: str = "formal") -> dict:
    """민원 문장을 주어진 문체로 변환하고 유형을 분류하여 딕셔너리로 반환."""
    prompt = (
        f"다음 민원 문장을 {style} 문체로 변환하고 민원 유형을 판단하세요.\n"
        f"문장: {text}\n\n"
        "출력 형식은 '분류: [민원 유형]\\n변환된 문장: [결과]' 입니다."
    )
    try:
        res = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role":"user", "content":prompt}],
            max_tokens=150,
            temperature=0.3,
        )
        content = res.choices[0].message["content"].strip()
    except Exception as e:
        raise RuntimeError(f"OpenAI API 호출 오류: {e}")

    # 응답 파싱
    classification, transformed = "", ""
    for line in content.splitlines():
        if line.startswith("분류:"):
            classification = line.split(":", 1)[1].strip()
        elif line.startswith("변환된 문장:") or line.startswith("변환된 문장 :"):
            transformed = line.split(":", 1)[1].strip()
    return {"classification": classification, "transformed": transformed}

def summarize_text(text: str) -> str:
    """긴 민원 문장을 한 문장으로 요약."""
    prompt = f"다음 민원 문장을 한 문장으로 요약하세요.\n\n문장: {text}\n\n요약:"
    try:
        res = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role":"user", "content":prompt}],
            max_tokens=100,
            temperature=0.3,
        )
        return res.choices[0].message["content"].strip()
    except Exception as e:
        raise RuntimeError(f"OpenAI API 호출 오류: {e}")
