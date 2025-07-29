import OpenAI from "openai";

export class TextComplaintAgent {
  openai = new OpenAI({ apiKey: process.env.OPENAI_KEY! });

  async classify(props: { text: string }) {
    const prompt =
      `다음 문장을 공손체로 바꾸고 민원 카테고리를 추론하세요.\n` +
      `문장: ${props.text}\n\nJSON({category, polite})`;
    const res = await this.openai.chat.completions.create({
      model: "gpt-4o",
      messages: [{ role: "user", content: prompt }],
      response_format: { type: "json_object" }
    });
    return JSON.parse(res.choices[0].message.content);
  }

  async summarize(props: { polite: string }) {
    const prompt = `다음 문장을 한 문장으로 요약하세요.\n${props.polite}\n\n요약:`;
    const res = await this.openai.chat.completions.create({
      model: "gpt-4o",
      messages: [{ role: "user", content: prompt }],
      max_tokens: 60, temperature: 0.3
    });
    return res.choices[0].message.content.trim();
  }
}
