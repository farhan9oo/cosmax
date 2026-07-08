import streamlit as st
import random
from datetime import datetime

st.set_page_config(page_title="RIA - AI 뷰티 크리에이터", page_icon="💄", layout="wide")

# ------------------------------------------------------------------
# COSMAX 브랜드 스타일 (레드 EA1D2C / 블랙 14161A / Pretendard)
# ------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.css');

html, body, [class*="css"] { font-family: 'Pretendard Variable', 'Pretendard', sans-serif; }

.main { background-color: #FAFAFA; }

.ria-header {
    background-color: #14161A;
    padding: 18px 28px;
    border-radius: 10px;
    border-bottom: 4px solid #EA1D2C;
    margin-bottom: 18px;
}
.ria-header h1 { color: #FFFFFF; font-size: 24px; margin: 0; }
.ria-header p { color: #CCCCCC; font-size: 13px; margin: 4px 0 0 0; }

.live-badge {
    background-color: #EA1D2C; color: white; font-size: 11px;
    padding: 2px 8px; border-radius: 4px; font-weight: 600;
}

.chat-box {
    background-color: #14161A; border-radius: 8px; padding: 12px;
    height: 340px; overflow-y: auto; color: #EEEEEE; font-size: 13px;
}
.chat-line { margin-bottom: 6px; }
.chat-nick { color: #EA1D2C; font-weight: 600; }

.reco-card {
    border: 1px solid #E5E5E5; border-left: 4px solid #EA1D2C;
    border-radius: 6px; padding: 14px 16px; margin-bottom: 12px; background: white;
}
.reco-title { font-weight: 700; font-size: 15px; color: #14161A; }
.reco-reason { color: #333333; font-size: 13px; margin-top: 4px; }

.warn-card {
    border: 1px solid #E5E5E5; border-left: 4px solid #999999;
    border-radius: 6px; padding: 12px 14px; background: #F5F5F5; font-size: 13px; color: #444444;
}
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------
# 목업 데이터 (2시간 프로토타입 범위 — 실제 이미지 분석/실시간 연동 제외)
# ------------------------------------------------------------------
PRODUCTS = {
    "건성": {
        "name": "모이스처 리페어 크림",
        "reason": "저분자 히알루론산과 세라마이드가 건조한 각질층에 즉각적인 수분막을 형성합니다.",
        "usage": "세안 후 토너 다음 단계에서 적당량을 얼굴 전체에 펴 발라주세요.",
        "not_for": "지성·트러블 피부는 유분감이 과도하게 느껴질 수 있습니다.",
    },
    "지성": {
        "name": "라이트 밸런싱 젤크림",
        "reason": "무유분 젤 제형으로 피지 분비를 조절하고 산뜻한 마무리감을 줍니다.",
        "usage": "세안 후 소량을 T존 위주로 얇게 펴 발라주세요.",
        "not_for": "건성 피부는 보습감이 부족하게 느껴질 수 있습니다.",
    },
    "복합성": {
        "name": "듀얼 컨트롤 에멀전",
        "reason": "부위별 다른 유수분 밸런스를 하나의 제형으로 동시에 관리합니다.",
        "usage": "T존은 얇게, 볼 부위는 조금 더 두껍게 발라주세요.",
        "not_for": "극건성 피부는 별도의 고보습 제품 병행을 권장합니다.",
    },
    "민감성": {
        "name": "센시티브 배리어 앰플",
        "reason": "무향·저자극 성분으로 피부 장벽을 보호하며 진정 효과를 줍니다.",
        "usage": "자극 없이 소량씩 두드리듯 흡수시켜 주세요.",
        "not_for": "트러블성 여드름 피부는 별도 트러블 케어 제품과 병행이 필요합니다.",
    },
}

LIVE_COMMENTS = [
    ("뷰티러버23", "리아야 오늘 신제품 발림성 어때?"),
    ("정유나", "저는 색소침착 고민인데 추천 있을까요?"),
    ("복숭아",  "가격대가 좀 궁금해요"),
    ("건조맨",  "이거 건성한테도 괜찮아요?"),
]

# ------------------------------------------------------------------
# 헤더
# ------------------------------------------------------------------
st.markdown("""
<div class="ria-header">
    <h1>💄 RIA <span class="live-badge">LIVE</span></h1>
    <p>신뢰를 쌓는 AI 뷰티 크리에이터 · 추천 기준을 투명하게 공개합니다</p>
</div>
""", unsafe_allow_html=True)

mode = st.radio("방송 모드", ["공개 라이브 (1:N)", "개인 맞춤 시뮬레이션"], horizontal=True, label_visibility="collapsed")

col_left, col_right = st.columns([1.3, 1])

# ------------------------------------------------------------------
# 좌측: 라이브 화면 + 채팅
# ------------------------------------------------------------------
with col_left:
    st.subheader("라이브 화면")
    st.image(
        "https://placehold.co/640x400/14161A/EA1D2C?text=RIA+Virtual+Beauty+Creator",
        use_container_width=True,
    )
    st.caption("※ 실제 서비스에서는 사용자 사진 기반 버추얼 얼굴이 표시됩니다. (프로토타입 단계에서는 목업 이미지로 대체)")

    st.subheader("실시간 채팅")
    if "chat" not in st.session_state:
        st.session_state.chat = LIVE_COMMENTS.copy()

    chat_html = "<div class='chat-box'>"
    for nick, msg in st.session_state.chat:
        chat_html += f"<div class='chat-line'><span class='chat-nick'>{nick}</span> : {msg}</div>"
    chat_html += "</div>"
    st.markdown(chat_html, unsafe_allow_html=True)

    new_msg = st.text_input("댓글을 입력하세요", key="new_comment")
    if st.button("전송"):
        if new_msg.strip():
            st.session_state.chat.append(("나", new_msg.strip()))
            reply = "리아: 댓글 확인했습니다. 개인 맞춤 시뮬레이션 모드에서 자세히 안내드릴게요."
            st.session_state.chat.append(("RIA", reply))
            st.rerun()

# ------------------------------------------------------------------
# 우측: 개인 맞춤 추천
# ------------------------------------------------------------------
with col_right:
    st.subheader("개인 맞춤 제품 추천")
    st.caption("Input: 피부 타입 · 고민 · 예산 → Process: 데이터 매칭 → Output: 추천 + 근거 + 사용법")

    skin_type = st.selectbox("피부 타입", list(PRODUCTS.keys()))
    concerns = st.multiselect("피부 고민", ["모공", "색소침착", "건조함", "트러블", "탄력"])
    budget = st.slider("예산 범위 (원)", 10000, 100000, (20000, 50000), step=5000)

    if st.button("맞춤 추천 받기", type="primary"):
        info = PRODUCTS[skin_type]
        st.markdown(f"""
        <div class="reco-card">
            <div class="reco-title">추천 제품 : {info['name']}</div>
            <div class="reco-reason">추천 이유 : {info['reason']}</div>
            <div class="reco-reason">사용 방법 : {info['usage']}</div>
        </div>
        """, unsafe_allow_html=True)

        with st.expander("추천 기준 공개"):
            st.write(f"- 선택한 피부 타입 : {skin_type}")
            st.write(f"- 선택한 고민 : {', '.join(concerns) if concerns else '선택 안 함'}")
            st.write(f"- 예산 범위 : {budget[0]:,}원 ~ {budget[1]:,}원")
            st.write("- 매칭 로직 : 피부 타입별 대표 성분 데이터와 사용자 입력값을 비교하여 산출합니다.")

        st.markdown(f"""
        <div class="warn-card">
            ⚠ 비추천 대상 안내 : {info['not_for']}
        </div>
        """, unsafe_allow_html=True)

st.divider()
st.caption(f"프로토타입 버전 · 마지막 업데이트 {datetime.now().strftime('%Y-%m-%d %H:%M')} · 사랑반 2조")
