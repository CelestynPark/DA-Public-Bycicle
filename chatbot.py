import streamlit as st
from chat.agent import ask_question
from chat.context import load_context

st.set_page_config(page_title="AI 분석 질의응답", layout="wide")
st.title("서울시 공공자전거 AI 분석 도우미")

st.markdown("""
자연어로 질문을 입력하면,
공공자전거 분석 데이터를 기반으로 AI가 답변해드립니다.
""")

question = st.text_input("질문을 입력하세요:", placeholder="예: 가장 많이 대여한 요일은 언제인가요?")

if question:
    with st.spinner("AI 응답 생성 중..."):
        context = load_context()
        answer = ask_question(question, context)
        st.markdown("##### 답변")
        st.success(answer)