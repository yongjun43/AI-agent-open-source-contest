import "dotenv/config";
import axios from "axios";
import { Agentica } from "@agentica/core";
import typia from "typia";
import { TextComplaintAgent } from "./TextComplaintAgent";

(async () => {
  /* ① FastAPI Swagger 로드 */
  const swagger = await axios
    .get("http://localhost:8000/openapi.json")
    .then(r => r.data);

  /* ② Agentica 설정 */
  const agent = new Agentica({
    model: "gpt-4o" as any,          // enum 미포함 시 as any
    controllers: [
      {
        protocol: "class",
        name: "text",
        application: typia.llm.application<TextComplaintAgent>(),
        execute: new TextComplaintAgent()
      },
      {
        protocol: "http",            // 필수 필드 connection!
        name: "vision",
        connection: { baseUrl: "http://localhost:8000" },
        application: swagger
      }
    ]
  });

  /* ③ 테스트 대화 */
  const result = await agent.conversate(
    "인도에 불법 주차된 차량을 신고합니다. (이미지 있음)"
  );
  console.log(result);
})();
