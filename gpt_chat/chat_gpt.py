import gradio as gr
import openai
import openai
import deepl
from openai import OpenAI

# OpenAI 라이브러리에 API 키 설정
openai.api_key = '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'
client = OpenAI(api_key='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')

def chatbot_response(message, history):
    # 대화 기록을 OpenAI 형식으로 변환
    messages = [{"role": "user", "content": pair[0]} for pair in history] + [{"role": "assistant", "content": pair[1]} for pair in history]
    messages.append({"role": "user", "content": message})

    # OpenAI에 요청을 보냅니다.
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    # 수정된 부분: OpenAI로부터 받은 응답의 내용을 올바르게 추출합니다.
    return response.choices[0].message.content


# Gradio 채팅 인터페이스 생성
demo = gr.ChatInterface(
    fn=chatbot_response,
    examples=["안녕", "오늘 날씨는 어때?", "좋은 영화 추천해줘"],
    title="ChatGPT 기반 채팅봇"
)

# 애플리케이션 실행
demo.launch()
