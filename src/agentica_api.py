# src/agentica_api.py
import requests
import yaml
from pathlib import Path

CONFIG_PATH = Path(__file__).resolve().parent.parent / "config.yaml"
with open(CONFIG_PATH, encoding="utf-8") as f:
    config = yaml.safe_load(f)

def send_to_agentica(data: dict) -> requests.Response:
    """Agentica API로 데이터 전송."""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {config['agentica']['api_token']}"
    }
    try:
        response = requests.post(config["agentica"]["api_url"], json=data, headers=headers, timeout=10)
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        raise RuntimeError(f"Agentica API 호출 오류: {e}")
