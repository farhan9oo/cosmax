import pathlib
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="코스미맥스로 | 대화로 찾는 내 피부 솔루션",
    page_icon="🍎",
    layout="centered",
)

# 원본 index.html은 순수 HTML/CSS/JS(DOM 조작)로 동작하는 챗봇 프로토타입입니다.
# Streamlit 위젯으로 재작성하면 인터랙션 로직(타이핑 효과, 슬롯필링, 메시지 삭제 등)이
# 손실되므로, components.html로 원본 파일을 그대로 임베드합니다.

HTML_PATH = pathlib.Path(__file__).parent / "index.html"
html_content = HTML_PATH.read_text(encoding="utf-8")

components.html(html_content, height=900, scrolling=False)
