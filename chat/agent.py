from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def ask_question(question: str, context: str) -> str:
    system_prompt = """
당신은 서울시 공공자전거 분석 전문가야.
아래에 제공되는 분석 데이터를 바탕으로 사용자의 질문에 성실히 응답해주세요.
가능하다면 수치나 요약 정보를 포함하고, 모호하거나 데이터가 없으면 그렇게 말해주세요.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"분석 요약:\n{context}"},
                {"role": "user", "content": f"질문:\n{question}"}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[ERROR] GPT 응답 실패: {e}"