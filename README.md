# AI agent(agentica) 
**FastAPI + YOLOv8(+OCR) Vision Service** × **Agentica (Node TS) Orchestrator**

```
~/yyj1010/study/agentica
├── .venv/                 # Python 가상환경
├── config.yaml
├── yolov8l.pt, yolov13x.pt  # 모델 가중치(100 MB↑ → Git LFS 권장)
├── orchestrator/          # ← Node + Agentica (실제 루트)
│   ├── package.json
│   ├── tsconfig.json
│   └── src/
│       ├── main.ts
│       └── TextComplaintAgent.ts
└── vision-service/        # ← FastAPI + YOLOv8 + OCR
    ├── app.py
    └── detect_ocr.py
```

> **주의** : 레포 최상단의 `package.json`·`node_modules/`·`pnpm-lock.yaml` 은 실수 설치 ⇒ 삭제하거나 무시  
> Node 관련 작업은 **`orchestrator/`** 폴더만 사용합니다.

---

## 1️⃣ Python Vision-Service

```bash
# 1. 가상환경 활성화
cd ~/yyj1010/study/agentica
source .venv/bin/activate

# 2. 필수 패키지
pip install --upgrade pip
pip install fastapi uvicorn[standard] ultralytics pillow numpy pytesseract python-multipart

# 3. 시스템 Tesseract (한글 포함)
sudo apt update
sudo apt install -y tesseract-ocr tesseract-ocr-kor

# 4. YOLO 가중치 경로 확인 (detect_ocr.py)
#    가장 간단: model = YOLO("yolov8n.pt")
#    커스텀 : model = YOLO("../yolov13x.pt")

# 5. 서버 실행
cd vision-service
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
# Swagger: http://localhost:8000/docs
```

---

## 2️⃣ Node Orchestrator (Agentica)

```bash
# 1. 루트 이동
cd ~/yyj1010/study/agentica/orchestrator

# 2. 의존성 설치
pnpm install          # 필요 시 --frozen-lockfile

# 3. 환경변수 (.env)
echo "OPENAI_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx" > .env

# 4. 실행
pnpm exec ts-node --esm src/main.ts
```

`src/main.ts` 에서 Vision API 스웨거를 불러와 GPT 컨트롤러 + Vision 컨트롤러를 구성합니다.

```ts
const agent = new Agentica({
  model: "gpt-4o-mini" as any,
  controllers: [
    {
      protocol: "class",
      name: "text",
      application: typia.llm.application<TextComplaintAgent>(),
      execute: new TextComplaintAgent()
    },
    {
      protocol: "http",
      name: "vision",
      connection: { baseUrl: "http://localhost:8000" },
      application: swagger            // FastAPI OpenAPI spec
    }
  ]
});
```

---

## 3️⃣ 디버깅 Quick Table

| 증상 | 체크 포인트 |
|------|-------------|
| **Could not import module "app"** | CWD =`vision-service/` 인지 or `uvicorn vision_service.app:app` |
| **python-multipart RuntimeError** | `pip install python-multipart` |
| **TypeError: 'type' object is not subscriptable** | Python \<3.9 → `List[Dict]` 구문 사용 |
| **AttributeError: DSC3k2** | 커스텀 YOLO 가중치 문제 → `yolov8n.pt` 로 교체 |
| **Swagger 404** | FastAPI 서버 포트·주소 확인 |
| **Node connection 타입 오류** | Vision 컨트롤러 `connection: { baseUrl }` 필수 |

---

## 4️⃣ 불필요한 상위 node_modules 정리 (선택)

```bash
cd ~/yyj1010/study/agentica
rm -rf node_modules package.json pnpm-lock.yaml
# orchestrator/node_modules/ 는 그대로 유지
```

---

## ✅ 최종 사용 흐름

| 터미널 | 명령 | 결과 |
|--------|------|-------|
| **A** | `uvicorn app:app --reload` | Vision API ↑  → Swagger /vision/analyze |
| **B** | `pnpm exec ts-node --esm src/main.ts` | GPT + Vision 통합 JSON 출력 |

콘솔 예시 (JSON 요약):

```json
{
  "classification": "불법 주정차",
  "summary_text": "인도 침범 차량 신고 접수",
  "visual_summary": "차량이 인도를 막고 서 있음"
}
```

---

## 📜 License
MIT — 자유롭게 사용·배포 가능. 인용 시 레포 링크를 남겨 주세요.
