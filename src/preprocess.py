# src/preprocess.py
import nltk
import string
import numpy as np
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from PIL import Image
from pathlib import Path

nltk.download("punkt", quiet=True)
nltk.download("stopwords", quiet=True)
nltk.download("wordnet", quiet=True)

def preprocess_text(text: str) -> str:
    """텍스트를 소문자 변환, 구두점 제거, 불용어 제거 후 표제어화."""
    text = text.lower().translate(str.maketrans("", "", string.punctuation))
    tokens = nltk.word_tokenize(text)
    tokens = [w for w in tokens if w not in set(stopwords.words("english"))]
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(w) for w in tokens]
    return " ".join(tokens)

def preprocess_image(image_path: str) -> np.ndarray:
    """이미지를 RGB np.ndarray로 반환."""
    img = Image.open(image_path).convert("RGB")
    return np.array(img)
