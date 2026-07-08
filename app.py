import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="코스미맥스로 | 대화로 찾는 내 피부 솔루션",
    page_icon="🍎",
    layout="centered",
)

# 원본은 순수 HTML/CSS/JS(DOM 조작)로 동작하는 챗봇 프로토타입입니다.
# Streamlit 위젯으로 재작성하면 인터랙션 로직(타이핑 효과, 슬롯필링, 메시지 삭제 등)이
# 손실되므로, components.html로 원본 마크업을 그대로 임베드합니다.
# 별도 index.html 파일에 의존하지 않도록 내용을 이 파일 안에 직접 포함합니다.

HTML_CONTENT = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, viewport-fit=cover">
<title>코스미맥스로 | 대화로 찾는 내 피부 솔루션</title>
<link rel="stylesheet" as="style" crossorigin href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable.css" />
<style>
  :root{
    --primary:#C8102E;
    --primary-dark:#A10E24;
    --primary-tint:#F7D9DD;
    --beige:#EADFC8;
    --card-bg:#F8F8F8;
    --text:#2B2B2B;
    --muted:#7A7A7A;
    --white:#FFFFFF;
    --border:#E5E5E5;
  }
  *{box-sizing:border-box;}
  html,body{
    margin:0;padding:0;height:100%;
    font-family:"Pretendard Variable","Pretendard","Apple SD Gothic Neo","Noto Sans KR",-apple-system,BlinkMacSystemFont,sans-serif;
    background:#F1EEE8;
    color:var(--text);
    -webkit-font-smoothing:antialiased;
    letter-spacing:-0.01em;
  }
  body{
    display:flex;
    align-items:center;
    justify-content:center;
    min-height:100vh;
    padding:14px;
  }
  .app{
    width:100%;
    max-width:480px;
    height:min(100dvh - 28px, 860px);
    display:flex;
    flex-direction:column;
    background:var(--white);
    border-radius:22px;
    box-shadow:0 16px 40px rgba(0,0,0,0.14);
    position:relative;
    overflow:hidden;
  }

  /* ---------- Top bar ---------- */
  .topbar{
    padding:18px 20px 16px;
    background:var(--primary);
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap:12px;
    flex-shrink:0;
  }
  .brand{display:flex;align-items:center;gap:11px;}
  .brand-logo{
    width:36px;height:36px;border-radius:11px;
    background:#FFFFFF;
    display:flex;align-items:center;justify-content:center;
    font-size:18px;flex-shrink:0;
  }
  .brand h1{font-size:15.5px;margin:0;letter-spacing:-0.1px;color:#FFFFFF;font-weight:700;}
  .brand p{font-size:11px;margin:3px 0 0;color:rgba(255,255,255,0.8);letter-spacing:-0.1px;}

  .progress{display:flex;flex-direction:column;align-items:flex-end;gap:6px;}
  .progress-dots{display:flex;gap:4px;}
  .dot{width:6px;height:6px;border-radius:50%;background:rgba(255,255,255,0.3);transition:background .25s;}
  .dot.filled{background:#FFFFFF;}
  .progress-label{font-size:10.5px;color:rgba(255,255,255,0.8);font-weight:600;}

  /* ---------- Character banner ---------- */
  .chat-banner{
    display:flex;align-items:center;gap:10px;
    padding:14px 20px;
    background:var(--white);
    box-shadow:0 1px 0 var(--border);
    flex-shrink:0;
  }
  .avatar{
    width:44px;height:44px;border-radius:50%;
    background:var(--white);
    display:flex;align-items:center;justify-content:center;
    font-size:22px;
    border:2px solid var(--primary);
    flex-shrink:0;
    overflow:hidden;
  }
  .avatar svg{width:100%;height:100%;display:block;}
  .banner-text{display:flex;flex-direction:column;gap:3px;}
  .banner-text strong{font-size:14px;font-weight:700;}
  .badge{
    display:inline-block;
    font-size:9.5px;
    font-weight:600;
    letter-spacing:0.04em;
    text-transform:uppercase;
    color:var(--muted);
    width:fit-content;
  }

  /* ---------- Screens ---------- */
  .screen{display:none;flex:1;flex-direction:column;min-height:0;overflow:hidden;}
  .screen.active{display:flex;}

  /* ---------- Chat area ---------- */
  .chat-wrap{flex:1;overflow:hidden;display:flex;flex-direction:column;min-height:0;}
  .chat-scroll{
    flex:1;overflow-y:auto;
    padding:20px 18px 10px;
    display:flex;flex-direction:column;gap:12px;
    background:var(--white);
  }
  .msg-row{display:flex;align-items:center;gap:6px;width:100%;}
  .msg-row.bot{justify-content:flex-start;}
  .msg-row.user{justify-content:flex-end;}
  .msg-delete{
    width:22px;height:22px;flex-shrink:0;
    border-radius:50%;
    border:none;
    background:var(--primary);
    color:#fff;
    font-size:13px;
    line-height:1;
    cursor:pointer;
    display:flex;align-items:center;justify-content:center;
    opacity:0;
    transform:scale(0.6);
    pointer-events:none;
    transition:opacity .15s, transform .15s;
  }
  .msg-row.selected .msg-delete{
    opacity:1;
    transform:scale(1);
    pointer-events:auto;
  }
  .msg{
    max-width:78%;
    min-width:130px;
    padding:11px 16px;
    border-radius:16px;
    font-size:13.5px;
    line-height:1.6;
    white-space:pre-wrap;
    box-shadow:0 1px 3px rgba(0,0,0,0.04);
    animation:pop .25s ease;
  }
  @keyframes pop{from{opacity:0;transform:translateY(6px);}to{opacity:1;transform:translateY(0);}}
  .msg.bot{
    background:var(--card-bg);
    border-bottom-left-radius:4px;
    color:var(--text);
  }
  .msg.user{
    background:var(--beige);
    color:var(--text);
    border-bottom-right-radius:4px;
  }
  .msg-image{
    align-self:flex-start;
    width:190px;height:190px;
    border-radius:16px;
    overflow:hidden;
    border:1px solid var(--border);
    box-shadow:0 2px 8px rgba(0,0,0,0.06);
    animation:pop .25s ease;
  }
  .msg-image svg{width:100%;height:100%;display:block;}
  .typing{
    align-self:flex-start;
    display:flex;gap:4px;
    padding:12px 14px;
    background:var(--card-bg);
    border-radius:16px;
    border-bottom-left-radius:4px;
  }
  .typing span{
    width:6px;height:6px;border-radius:50%;
    background:var(--muted);
    animation:blink 1.2s infinite ease-in-out;
  }
  .typing span:nth-child(2){animation-delay:.2s;}
  .typing span:nth-child(3){animation-delay:.4s;}
  @keyframes blink{0%,80%,100%{opacity:.25;}40%{opacity:1;}}

  .product-card{
    align-self:flex-start;
    max-width:88%;
    background:var(--white);
    border:1px solid var(--border);
    border-radius:14px;
    padding:14px 16px;
    box-shadow:0 2px 10px rgba(0,0,0,0.05);
    animation:pop .25s ease;
  }
  .product-card + .product-card{margin-top:2px;}
  .product-card .p-top{display:flex;gap:12px;align-items:flex-start;margin-bottom:10px;}
  .product-card .p-image{
    width:60px;height:60px;flex-shrink:0;
    border-radius:12px;overflow:hidden;
    background:var(--card-bg);
    border:1px solid var(--border);
  }
  .product-card .p-image svg{width:100%;height:100%;display:block;}
  .product-card .p-meta{flex:1;min-width:0;}
  .product-card .p-name{font-size:13.5px;font-weight:700;margin:0 0 6px;}
  .product-card .p-tags{display:flex;gap:5px;flex-wrap:wrap;}
  .product-card .p-tag{
    font-size:10px;color:var(--primary-dark);
    background:var(--primary-tint);
    border-radius:10px;padding:2px 8px;
  }
  .product-card .p-desc{font-size:12px;color:var(--muted);margin:0 0 10px;line-height:1.6;}
  .product-card .p-bottom{display:flex;align-items:center;justify-content:space-between;gap:8px;}
  .product-card .p-price{font-size:13px;font-weight:700;color:var(--text);}
  .product-card .p-link{
    font-size:11.5px;font-weight:600;color:var(--white);
    background:var(--primary);
    border:none;border-radius:10px;
    padding:7px 12px;cursor:pointer;
    transition:background .2s;
  }
  .product-card .p-link:hover{background:var(--primary-dark);}
  .product-note{font-size:10.5px;color:var(--muted);align-self:flex-start;padding:0 4px;}

  /* ---------- Footer / input ---------- */
  .input-bar{
    flex-shrink:0;
    background:var(--white);
    border-top:1px solid var(--border);
    padding:10px 14px calc(10px + env(safe-area-inset-bottom));
    display:flex;flex-direction:column;gap:8px;
  }
  .next-btn{
    width:100%;
    padding:11px;
    border:none;
    border-radius:14px;
    font-size:13px;
    font-weight:700;
    background:var(--border);
    color:var(--muted);
    cursor:not-allowed;
    transition:all .25s;
  }
  .next-btn.active{
    background:var(--primary);
    color:#fff;
    cursor:pointer;
    box-shadow:0 6px 16px rgba(200,16,46,0.35);
    animation:pulse 1.8s infinite;
  }
  @keyframes pulse{
    0%,100%{transform:scale(1);}
    50%{transform:scale(1.015);}
  }
  .input-row{display:flex;gap:8px;align-items:center;}
  .chat-text-input{
    flex:1;
    padding:11px 14px;
    border-radius:20px;
    border:1px solid var(--border);
    background:var(--card-bg);
    font-size:13.5px;
    outline:none;
    color:var(--text);
  }
  .chat-text-input:focus{border-color:var(--primary);}
  .send-btn{
    width:40px;height:40px;flex-shrink:0;
    border-radius:50%;
    border:none;
    background:var(--primary);
    color:#fff;
    cursor:pointer;
    display:flex;align-items:center;justify-content:center;
    padding:0;
    transition:background .2s;
  }
  .send-btn svg{
    width:16px;height:16px;
    display:block;
    margin-left:1px;
  }
  .send-btn:hover{background:var(--primary-dark);}
  .send-btn:disabled{background:var(--border);cursor:not-allowed;}

  /* ---------- Toast ---------- */
  .toast{
    position:absolute;
    bottom:90px;left:50%;
    transform:translateX(-50%) translateY(10px);
    background:var(--text);
    color:#fff;
    padding:10px 18px;
    border-radius:20px;
    font-size:12.5px;
    opacity:0;
    pointer-events:none;
    transition:all .3s;
    white-space:nowrap;
  }
  .toast.show{opacity:1;transform:translateX(-50%) translateY(0);}

  @media (max-width:380px){
    .brand p{display:none;}
  }
</style>
</head>
<body>

<div class="app">
  <div class="topbar">
    <div class="brand">
      <div class="brand-logo">🍎</div>
      <div>
        <h1>코스미맥스로</h1>
        <p>대화로 찾는 내 피부 솔루션</p>
      </div>
    </div>
    <div class="progress" id="progressWrap">
      <div class="progress-dots" id="progressDots"></div>
      <span class="progress-label" id="progressLabel">0/8</span>
    </div>
  </div>

  <div class="screen active" id="screenDiagnosis">
    <div class="chat-banner">
      <div class="avatar">
        <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
          <rect x="0" y="0" width="100" height="100" fill="#F0F0F0"/>
          <circle cx="50" cy="37" r="17" fill="#D6D6D6"/>
          <path d="M18 100 C18 67 33 58 50 58 C67 58 82 67 82 100 Z" fill="#D6D6D6"/>
        </svg>
      </div>
      <div class="banner-text">
        <strong>이수지 실장</strong>
        <span class="badge">SNL 스마일클리닉</span>
      </div>
    </div>

    <div class="chat-wrap">
      <div class="chat-scroll" id="chatScroll"></div>
    </div>

    <div class="input-bar">
      <button class="next-btn" id="nextBtn" disabled>제품 추천 받으러 가기 →</button>
      <div class="input-row">
        <input type="text" class="chat-text-input" id="chatInput" placeholder="편하게 이야기해주세요..." autocomplete="off">
        <button class="send-btn" id="sendBtn" aria-label="전송">
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M4 12L20 12M20 12L13 5M20 12L13 19" stroke="#fff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>
      </div>
    </div>
  </div>

  <div class="screen" id="screenProduct">
    <div class="chat-banner">
      <div class="avatar">
        <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
          <rect x="0" y="0" width="100" height="100" fill="#F0F0F0"/>
          <circle cx="50" cy="37" r="17" fill="#D6D6D6"/>
          <path d="M18 100 C18 67 33 58 50 58 C67 58 82 67 82 100 Z" fill="#D6D6D6"/>
        </svg>
      </div>
      <div class="banner-text">
        <strong>이수지 실장</strong>
        <span class="badge">제품 추천 중</span>
      </div>
    </div>

    <div class="chat-wrap">
      <div class="chat-scroll" id="chatScroll2"></div>
    </div>

    <div class="input-bar">
      <div class="input-row">
        <input type="text" class="chat-text-input" id="chatInput2" placeholder="편하게 이야기해주세요..." autocomplete="off">
        <button class="send-btn" id="sendBtn2" aria-label="전송">
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M4 12L20 12M20 12L13 5M20 12L13 19" stroke="#fff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>
      </div>
    </div>
  </div>

  <div class="toast" id="toast"></div>
</div>

<script>
  const chatScroll = document.getElementById('chatScroll');
  const chatInput = document.getElementById('chatInput');
  const sendBtn = document.getElementById('sendBtn');
  const nextBtn = document.getElementById('nextBtn');
  const progressWrap = document.getElementById('progressWrap');
  const progressDots = document.getElementById('progressDots');
  const progressLabel = document.getElementById('progressLabel');
  const toast = document.getElementById('toast');

  const screenDiagnosis = document.getElementById('screenDiagnosis');
  const screenProduct = document.getElementById('screenProduct');
  const chatScroll2 = document.getElementById('chatScroll2');
  const chatInput2 = document.getElementById('chatInput2');
  const sendBtn2 = document.getElementById('sendBtn2');

  // ---------- 자유 대화 슬롯필링 상태 ----------
  // 사용자는 객관식이 아니라 자유 텍스트로 말하고, 여기서 내부적으로 슬롯을 채워나간다.
  let diagnosisSlots = {
    "유분감": null,
    "건조감": null,
    "세안_후_당김": null,
    "T존_번들거림": null,
    "U존_건조함": null,
    "각질": null,
    "민감_따가움_홍조": null,
    "여드름_트러블_위치": null,
    "사용_중인_제품": null,
    "피해야_할_성분": null,
    "선호_제형": null
  };
  const askedSlots = new Set();
  let diagnosisResult = null;

  // 피부 타입(건성/지성/복합성/수부지) 판별에 실제로 쓰이는 슬롯만 모음
  // 민감성/여드름은 피부 타입이 아니라 concerns로 별도 분리됨
  const DIAGNOSTIC_SLOTS = ["유분감", "건조감", "세안_후_당김", "T존_번들거림", "U존_건조함", "각질", "민감_따가움_홍조", "여드름_트러블_위치"];

  const SLOT_KEYWORDS = {
    "유분감": ["번들", "기름", "유분", "미끌"],
    "건조감": ["건조", "푸석", "메마"],
    "세안_후_당김": ["당기", "땡기", "당김"],
    "각질": ["각질", "거칠"],
    "민감_따가움_홍조": ["예민", "민감", "따갑", "화끈", "붉어지", "홍조", "가렵", "자극"],
    "여드름_트러블_위치": ["여드름", "뾰루지", "트러블", "좁쌀", "화농"],
    "사용_중인_제품": ["토너", "에센스", "세럼", "크림", "로션", "클렌저", "스킨"],
    "피해야_할_성분": ["레티놀", "AHA", "BHA", "알코올", "향료"],
    "선호_제형": ["가볍", "산뜻", "촉촉", "밀착", "묵직", "젤"]
  };
  // T존/U존은 "부위 단어"와 "유분/건조 단어"가 같이 나와야 신뢰도 있는 신호로 취급
  const T_ZONE_WORDS = ["티존", "T존", "t존", "이마", "코"];
  const U_ZONE_WORDS = ["볼", "유존", "U존", "u존"];
  const OILY_WORDS = ["번들", "기름", "유분", "미끌"];
  const DRY_WORDS = ["당기", "땡기", "당김", "건조", "푸석"];

  function hasAny(text, words){
    return words.some((w) => text.includes(w));
  }

  // 자유 텍스트에서 슬롯 정보를 추출한다. 이미 채워진 슬롯은 덮어쓰지 않는다.
  function extractSlots(text, slots){
    const filled = [];
    if(!slots["T존_번들거림"] && hasAny(text, T_ZONE_WORDS) && hasAny(text, OILY_WORDS)){
      slots["T존_번들거림"] = text;
      filled.push("T존_번들거림");
    }
    if(!slots["U존_건조함"] && hasAny(text, U_ZONE_WORDS) && hasAny(text, DRY_WORDS)){
      slots["U존_건조함"] = text;
      filled.push("U존_건조함");
    }
    for(const slot in SLOT_KEYWORDS){
      if(slots[slot]) continue;
      if(hasAny(text, SLOT_KEYWORDS[slot])){
        slots[slot] = text;
        filled.push(slot);
      }
    }
    return filled;
  }

  // 부족한 정보를 자연스러운 순서로 물어보기 위한 질문 은행
  // topic: 엉뚱한 답변을 자연스럽게 다음 질문으로 넘길 때 쓰는 짧은 표현
  // ask: 직접 물어볼 때 쓰는 완전한 질문 문장
  const SLOT_QUESTIONS = [
    { slot: "세안_후_당김", topic: "세안 후 당김이 있는지", ask: "세안하고 나서 얼굴이 당기는 느낌이 있으세요, 없으세요?" },
    { slot: "유분감", topic: "번들거림이나 유분기가 있는지", ask: "그럼 반대로 번들거리거나 기름지는 느낌은 어느 정도세요?" },
    { slot: "T존_번들거림", topic: "이마나 코(T존)가 번들거리는지", ask: "오오, 그럼 이마나 코 쪽(T존)이 유독 번들거리는 편이세요?" },
    { slot: "U존_건조함", topic: "볼 쪽이 당기는지", ask: "볼 쪽은 어때요? 거긴 오히려 당기고 건조한 편인가요?" },
    { slot: "각질", topic: "각질이 있는지", ask: "각질은 어떠세요? 손으로 만졌을 때 까슬까슬한 부위 있으세요?" },
    { slot: "민감_따가움_홍조", topic: "새 제품 쓸 때 따갑거나 붉어지는지", ask: "새로운 제품 쓰면 따갑거나 붉어지는 편이세요?" },
    { slot: "여드름_트러블_위치", topic: "여드름이나 트러블이 어디에 나는지", ask: "여드름이나 트러블은 주로 어디에 잘 나는 편이세요? (턱, 볼, 이마 등)" },
    { slot: "사용_중인_제품", topic: "지금 쓰고 계신 제품", ask: "지금 쓰고 계신 스킨케어 제품 있으면 편하게 말씀해주세요!" }
  ];

  function pickNextQuestionItem(slots, asked){
    for(const item of SLOT_QUESTIONS){
      if(!slots[item.slot] && !asked.has(item.slot)){
        asked.add(item.slot);
        return item;
      }
    }
    return null;
  }

  function filledCount(slots, list){
    return list.filter((s) => slots[s]).length;
  }

  function isReadyForDiagnosis(slots, asked){
    if(filledCount(slots, DIAGNOSTIC_SLOTS) >= 4) return true;
    if(asked.size >= SLOT_QUESTIONS.length) return true;
    return false;
  }

  const EVIDENCE_LABELS = {
    "유분감": "번들거림/유분기",
    "건조감": "건조함",
    "세안_후_당김": "세안 후 당김",
    "T존_번들거림": "T존 번들거림",
    "U존_건조함": "볼(U존) 건조함",
    "각질": "각질",
    "민감_따가움_홍조": "따가움/홍조",
    "여드름_트러블_위치": "여드름/트러블"
  };

  // 채워진 슬롯을 근거로 피부 타입(건성/지성/복합성/수부지)과 고민(민감/여드름 등)을 계산한다.
  // diagnosis_result 형식: { primary_skin_type, secondary_skin_type, concerns, evidence, confidence }
  function computeDiagnosis(slots){
    const oilScore = (slots["유분감"] ? 1 : 0) + (slots["T존_번들거림"] ? 1 : 0);
    const dryScore = (slots["건조감"] ? 1 : 0) + (slots["세안_후_당김"] ? 1 : 0) + (slots["U존_건조함"] ? 1 : 0) + (slots["각질"] ? 1 : 0);
    const hasAreaSplit = Boolean(slots["T존_번들거림"] && slots["U존_건조함"]);

    let primary;
    if(hasAreaSplit) primary = "복합성";
    else if(oilScore > 0 && dryScore > 0) primary = "수부지";
    else if(oilScore > dryScore) primary = "지성";
    else if(dryScore > oilScore) primary = "건성";
    else primary = "복합성";

    const typeScores = {
      "건성": dryScore,
      "지성": oilScore,
      "복합성": hasAreaSplit ? oilScore + dryScore : 0,
      "수부지": (oilScore > 0 && dryScore > 0) ? Math.min(oilScore, dryScore) : 0
    };
    delete typeScores[primary];
    let secondary = null;
    let secondBest = 0;
    for(const type in typeScores){
      if(typeScores[type] > secondBest){ secondBest = typeScores[type]; secondary = type; }
    }

    const concerns = [];
    if(slots["민감_따가움_홍조"]) concerns.push("민감");
    if(slots["여드름_트러블_위치"]) concerns.push("여드름");
    if(slots["세안_후_당김"] && slots["민감_따가움_홍조"]) concerns.push("장벽약화");

    const evidence = DIAGNOSTIC_SLOTS.filter((s) => slots[s]).map((s) => EVIDENCE_LABELS[s]);
    const confidence = Math.round(Math.min(0.95, 0.4 + filledCount(slots, DIAGNOSTIC_SLOTS) * 0.1) * 100) / 100;

    return {
      primary_skin_type: primary,
      secondary_skin_type: secondary,
      concerns: concerns,
      evidence: evidence,
      confidence: confidence
    };
  }

  const AVATAR_IMAGE_SVG =
    '<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">' +
    '<rect x="0" y="0" width="100" height="100" fill="#F8F8F8"/>' +
    '<circle cx="16" cy="16" r="12" fill="#F3D9BE"/>' +
    '<circle cx="84" cy="16" r="12" fill="#F3D9BE"/>' +
    '<path d="M2 100 Q2 66 50 63 Q98 66 98 100 Z" fill="#FFFFFF" stroke="#DCDCDC" stroke-width="2"/>' +
    '<path d="M30 63 L50 80 L70 63" fill="none" stroke="#C8102E" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>' +
    '<circle cx="50" cy="36" r="36" fill="#F8D9BB"/>' +
    '<circle cx="24" cy="44" r="5" fill="#F5A9A0" opacity="0.6"/>' +
    '<circle cx="76" cy="44" r="5" fill="#F5A9A0" opacity="0.6"/>' +
    '<circle cx="33" cy="34" r="4" fill="#2B2B2B"/>' +
    '<circle cx="67" cy="34" r="4" fill="#2B2B2B"/>' +
    '<ellipse cx="50" cy="42" rx="3" ry="2.2" fill="#EFC49E"/>' +
    '<path d="M32 48 Q50 60 68 48" fill="none" stroke="#2B2B2B" stroke-width="3" stroke-linecap="round"/>' +
    '</svg>';

  // 처음 인사: 이미지 먼저 보내고, 그 다음 텍스트 인사
  window.addEventListener('DOMContentLoaded', () => {
    renderDots();
    showTyping(chatScroll);
    setTimeout(() => {
      removeTyping(chatScroll);
      addImageMessage(chatScroll, AVATAR_IMAGE_SVG);
      setTimeout(() => {
        typeAndSend(
          chatScroll,
          "은능흐스으 스므을클르늑 읍느드으?! 스마일클리닉 실장이자 얼굴인 이수지 실장입니돠아 😎\n요즘 피부 때문에 고민 있으셨죠? 편하게 다 말해보세요.",
          500
        );
      }, 500);
    }, 400);
  });

  function renderDots(){
    const filled = filledCount(diagnosisSlots, DIAGNOSTIC_SLOTS);
    const total = DIAGNOSTIC_SLOTS.length;
    progressDots.innerHTML = '';
    for(let i=0;i<total;i++){
      const d = document.createElement('div');
      d.className = 'dot' + (i < filled ? ' filled' : '');
      progressDots.appendChild(d);
    }
    progressLabel.textContent = `${filled}/${total}`;
  }

  function addImageMessage(scroll, svgMarkup){
    const el = document.createElement('div');
    el.className = 'msg-image';
    el.innerHTML = svgMarkup;
    scroll.appendChild(el);
    scroll.scrollTop = scroll.scrollHeight;
  }

  function addMessage(scroll, text, sender){
    const row = document.createElement('div');
    row.className = 'msg-row ' + sender;

    let deleteBtn = null;
    if(sender === 'user'){
      deleteBtn = document.createElement('button');
      deleteBtn.type = 'button';
      deleteBtn.className = 'msg-delete';
      deleteBtn.setAttribute('aria-label', '삭제');
      deleteBtn.textContent = '×';
      row.appendChild(deleteBtn);
    }

    const bubble = document.createElement('div');
    bubble.className = 'msg ' + sender;
    bubble.textContent = text;
    row.appendChild(bubble);

    if(sender === 'user'){
      bubble.addEventListener('dblclick', (e) => {
        e.stopPropagation();
        document.querySelectorAll('.msg-row.selected').forEach((r) => {
          if(r !== row) r.classList.remove('selected');
        });
        row.classList.toggle('selected');
      });
      deleteBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        row.remove();
      });
    }

    scroll.appendChild(row);
    scroll.scrollTop = scroll.scrollHeight;
  }

  document.addEventListener('click', (e) => {
    document.querySelectorAll('.msg-row.selected').forEach((r) => {
      if(!r.contains(e.target)) r.classList.remove('selected');
    });
  });

  function showTyping(scroll){
    const el = document.createElement('div');
    el.className = 'typing';
    el.innerHTML = '<span></span><span></span><span></span>';
    scroll.appendChild(el);
    scroll.scrollTop = scroll.scrollHeight;
  }

  function removeTyping(scroll){
    const el = scroll.querySelector('.typing');
    if(el) el.remove();
  }

  function typeAndSend(scroll, text, delay){
    showTyping(scroll);
    return new Promise((resolve) => {
      setTimeout(() => {
        removeTyping(scroll);
        addMessage(scroll, text, 'bot');
        resolve();
      }, delay);
    });
  }

  function handleSend(){
    const text = chatInput.value.trim();
    if(!text) return;
    addMessage(chatScroll, text, 'user');
    chatInput.value = '';

    if(diagnosisResult){
      typeAndSend(chatScroll, "네에, 그 얘기도 참고할게요! 아래 '제품 추천 받으러 가기' 눌러서 결과 보러 가실까요? 😊", 500);
      return;
    }

    const newlyFilled = extractSlots(text, diagnosisSlots);
    renderDots();

    if(isReadyForDiagnosis(diagnosisSlots, askedSlots)){
      diagnosisResult = computeDiagnosis(diagnosisSlots);
      typeAndSend(chatScroll, "네에, 이 정도면 피부 상태가 딱 파악됐어용! 아래 '제품 추천 받으러 가기' 눌러서 결과 보러 가실까요? 👇", 500);
      unlockNextButton();
      return;
    }

    const item = pickNextQuestionItem(diagnosisSlots, askedSlots);
    if(newlyFilled.length === 0){
      // 슬롯과 무관한 엉뚱한 답변 - 자연스럽게 받아넘기고 다음 필요한 정보로 유도
      const topic = item ? item.topic : "조금 더 자세한 피부 상태";
      typeAndSend(chatScroll, `좋아요, 그 얘기도 참고할게요~ 피부 상태를 더 정확히 보려면 ${topic}도 알려주세요!`, 500 + Math.random()*300);
    } else {
      typeAndSend(chatScroll, item ? item.ask : "조으음 더 자세히 말씀해주시겠어용?", 500 + Math.random()*300);
    }
  }

  function unlockNextButton(){
    nextBtn.disabled = false;
    nextBtn.classList.add('active');
  }

  sendBtn.addEventListener('click', handleSend);
  chatInput.addEventListener('keydown', (e) => {
    if(e.key === 'Enter') handleSend();
  });

  const DIAGNOSIS_DETAILS = {
    "건성": {
      summary: "건조성 피부에 가까운 것 같아요 😊\n세안 후에 땡기는 느낌이 있고 각질도 종종 올라오는 편이라, 수분과 유분이 함께 부족한 상태일 가능성이 높아요.",
      bullets: [
        "🔹 세라마이드·히알루론산처럼 수분을 꽉 채워주는 고보습 제품",
        "🔹 유수분 밸런스를 잡아주는 장벽 강화 크림",
        "🔹 폼클렌저보다는 저자극 크림/오일 타입 세안제"
      ],
      procedure: "피부과 시술은 수분을 채워주는 스킨부스터/필링 계열을 추천드릴게요! 각질 제거 위주의 강한 박피는 지금 피부엔 좀 자극적일 수 있어요."
    },
    "지성": {
      summary: "지성 피부에 가까운 것 같아요 😊\n세안하고 나서도 금방 번들거리는 편이라, 피지 분비가 활발하고 모공이 넓어지기 쉬운 상태일 가능성이 높아요.",
      bullets: [
        "🔹 티트리·살리실산처럼 피지·모공 관리에 도움되는 성분",
        "🔹 산뜻하게 스며드는 가벼운 젤/워터 타입 제품",
        "🔹 무거운 고보습 크림이나 오일 함량 높은 제품은 당분간 가볍게"
      ],
      procedure: "피부과 시술은 모공·피지 조절에 도움되는 필링/레이저 계열을 추천드릴게요! 과도한 오일 마사지는 오히려 자극이 될 수 있어요."
    },
    "복합성": {
      summary: "복합성 피부에 가까운 것 같아요 😊\nT존은 번들거리고 볼 쪽은 당기는 느낌이 있는 걸 보니, 부위별로 유·수분 상태가 다른 편일 가능성이 높아요.",
      bullets: [
        "🔹 T존·볼 부위 상관없이 무난한 저자극 보습 제품",
        "🔹 가볍게 스며들면서도 당김은 잡아주는 밸런싱 제품",
        "🔹 부위별 자극이 다를 수 있으니 향료·알코올 최소화 제품"
      ],
      procedure: "피부과 시술은 피지·모공과 수분 밸런스를 함께 잡아주는 스킨부스터 계열을 추천드릴게요! 강한 박피는 볼 쪽엔 자극적일 수 있어요."
    },
    "수부지": {
      summary: "수분부족지성(수부지) 피부에 가까운 것 같아요 😊\n번들거리는 느낌과 당기는 느낌이 같이 나타나는 걸 보니, 겉은 기름지지만 속은 수분이 부족한 상태일 가능성이 높아요.",
      bullets: [
        "🔹 저분자+고분자 히알루론산으로 속수분부터 채워주는 제품",
        "🔹 산뜻하면서도 보습력 있는 워터젤 타입",
        "🔹 과도한 오일 컷 클렌저나 강한 필링은 당분간 피하는 게 좋아요"
      ],
      procedure: "피부과 시술은 속수분을 채워주는 스킨부스터 계열을 추천드릴게요! 피지 제거 위주의 강한 필링은 오히려 자극이 될 수 있어요."
    }
  };

  // diagnosis_result(primary_skin_type, concerns 등)를 기반으로 진단 메시지를 만든다.
  function buildDiagnosisMessage(result){
    const d = DIAGNOSIS_DETAILS[result.primary_skin_type] || DIAGNOSIS_DETAILS["복합성"];
    let concernNote = "";
    if(result.concerns.includes("민감")){
      concernNote += "\n\n거기에 자극에도 좀 예민하게 반응하시는 편이라, 향료·알코올 없는 저자극 제품 위주로 고르시는 게 좋아요.";
    }
    if(result.concerns.includes("여드름")){
      concernNote += "\n\n트러블도 종종 올라오는 편이니, 살리실산이나 티트리처럼 트러블 케어 성분도 같이 봐드릴게요.";
    }
    return (
      "자아, 말씀 다 들어봤어용! 종합해보니 고객님은 " + d.summary + concernNote + "\n\n" +
      "그래서 제품은 이런 방향으로 고르시는 게 좋아요:\n" +
      d.bullets.join("\n") + "\n\n" +
      d.procedure + "\n\n" +
      "이제 이 방향에 맞는 코스맥스 제품, 구체적으로 골라드릴까요?"
    );
  }

  let screenSwitched = false;
  nextBtn.addEventListener('click', () => {
    if(nextBtn.disabled || screenSwitched) return;
    screenSwitched = true;
    if(!diagnosisResult){ diagnosisResult = computeDiagnosis(diagnosisSlots); }
    screenDiagnosis.classList.remove('active');
    screenProduct.classList.add('active');
    progressWrap.style.display = 'none';
    typeAndSend(chatScroll2, buildDiagnosisMessage(diagnosisResult), 500);
  });

  /* ---------- 제품 추천 화면 (키워드 슬롯필링) ---------- */
  const CATEGORY_KEYWORDS = {
    "스킨":"스킨/토너", "토너":"스킨/토너", "로션":"로션", "에센스":"에센스",
    "세럼":"세럼", "크림":"크림", "클렌저":"클렌저", "선크림":"선크림"
  };
  const TEXTURE_KEYWORDS = {
    "가벼":"가볍고 산뜻한 타입", "산뜻":"가볍고 산뜻한 타입",
    "촉촉":"촉촉한 밀착 타입", "밀착":"촉촉한 밀착 타입", "묵직":"묵직한 타입"
  };
  const EFFECT_KEYWORDS = {
    "진정":"진정", "보습":"보습", "장벽":"장벽강화",
    "미백":"미백", "탄력":"탄력", "트러블":"트러블 개선", "각질":"각질 케어",
    "피지":"피지조절", "모공":"모공케어"
  };

  // 피부 타입별 기본 효과/제형 — 사용자가 직접 고르지 않고 "네가 알아서/맞는 걸로" 위임할 때 씀
  const SKIN_TYPE_PROFILE = {
    "건성": { effect: "보습, 장벽강화", texture: "촉촉한 밀착 타입" },
    "지성": { effect: "피지조절, 트러블 개선", texture: "가볍고 산뜻한 타입" },
    "복합성": { effect: "보습, 피지조절", texture: "가볍고 산뜻한 타입" },
    "수부지": { effect: "보습, 피지조절", texture: "가볍고 산뜻한 타입" }
  };
  const DELEGATE_KEYWORDS = ["맞는", "적합", "알아서", "너가 골라", "니가 골라", "정해줘", "추천해줘", "골라줘", "아무거나", "다 좋아"];

  const productSlots = { category:null, texture:null, effect:null };
  let effectFromDelegation = false;

  // diagnosis_result.concerns(민감/여드름)을 위임 시 기본 효과에 추가로 반영
  function buildDelegatedEffect(){
    const profile = SKIN_TYPE_PROFILE[diagnosisResult.primary_skin_type] || SKIN_TYPE_PROFILE["복합성"];
    const effects = profile.effect.split(", ");
    if(diagnosisResult.concerns.includes("민감") && !effects.includes("진정")) effects.push("진정");
    if(diagnosisResult.concerns.includes("여드름") && !effects.includes("트러블 개선")) effects.push("트러블 개선");
    return effects.join(", ");
  }

  function detectSlots(text){
    if(!productSlots.category){
      for(const k in CATEGORY_KEYWORDS){ if(text.includes(k)){ productSlots.category = CATEGORY_KEYWORDS[k]; break; } }
    }
    if(!productSlots.texture){
      for(const k in TEXTURE_KEYWORDS){ if(text.includes(k)){ productSlots.texture = TEXTURE_KEYWORDS[k]; break; } }
    }
    if(!productSlots.effect){
      for(const k in EFFECT_KEYWORDS){ if(text.includes(k)){ productSlots.effect = EFFECT_KEYWORDS[k]; break; } }
    }

    // 명시적 키워드가 없는데 "위임" 표현이면, 아까 진단 결과(피부타입+고민) 기준으로 대신 채워줌
    const delegated = DELEGATE_KEYWORDS.some((k) => text.includes(k));
    if(delegated){
      const profile = SKIN_TYPE_PROFILE[diagnosisResult.primary_skin_type] || SKIN_TYPE_PROFILE["복합성"];
      if(!productSlots.effect){ productSlots.effect = buildDelegatedEffect(); effectFromDelegation = true; }
      if(!productSlots.texture){ productSlots.texture = profile.texture; }
    }
  }

  function nextProductQuestion(){
    if(!productSlots.category) return "어떤 제품 종류가 필요하세요? 로션, 세럼, 크림, 클렌저 중에 골라주시겠어요?";
    if(!productSlots.texture) return `오오, ${productSlots.category} 찾고 계시는구나~! 사용감은 어떤 스타일이 좋으세요? 가볍고 산뜻한 타입 vs 촉촉하게 밀착되는 타입, 어느 쪽이세요?`;
    if(!productSlots.effect) return "조아용~ 제일 원하시는 효과가 뭐예요? 예를 들면 진정, 보습, 장벽강화, 미백, 탄력 이런 것 중에서요!";
    return null;
  }

  function handleProductSend(){
    const text = chatInput2.value.trim();
    if(!text) return;
    addMessage(chatScroll2, text, 'user');
    chatInput2.value = '';
    detectSlots(text);

    const question = nextProductQuestion();
    if(question){
      typeAndSend(chatScroll2, question, 500 + Math.random()*300);
    } else {
      const closing = effectFromDelegation
        ? `네에, 아까 진단해드린 ${diagnosisResult.primary_skin_type} 피부 타입 기준으로 ${productSlots.effect} 중심으로 딱 골라드릴게용! 👇`
        : `네에, ${diagnosisResult.primary_skin_type} 피부에 맞는 제품으로 딱 골라드렸어용! 👇`;
      typeAndSend(chatScroll2, closing, 500).then(renderProductCards);
    }
  }

  const CREAM_IMAGE_SVG =
    '<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">' +
    '<rect x="8" y="22" width="48" height="36" rx="12" fill="#FFFFFF" stroke="#E5E5E5" stroke-width="2"/>' +
    '<rect x="10" y="14" width="44" height="10" rx="5" fill="#EADFC8"/>' +
    '<rect x="16" y="8" width="32" height="8" rx="4" fill="#DDD0B4"/>' +
    '<ellipse cx="32" cy="42" rx="11" ry="6.5" fill="#8FBF6B" transform="rotate(-35 32 42)"/>' +
    '<path d="M25 46 L39 36" stroke="#5E9142" stroke-width="1.6" stroke-linecap="round"/>' +
    '</svg>';

  const SERUM_IMAGE_SVG =
    '<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">' +
    '<rect x="24" y="2" width="16" height="6" rx="3" fill="#8FB9B4"/>' +
    '<rect x="20" y="6" width="24" height="14" rx="4" fill="#BFD9D6"/>' +
    '<path d="M18 20 L46 20 L42 58 Q42 60 40 60 L24 60 Q22 60 22 58 Z" fill="#FFFFFF" stroke="#E5E5E5" stroke-width="2"/>' +
    '<path d="M32 30c-4 4-6 8-6 12 0 3.5 2.7 6 6 6s6-2.5 6-6c0-4-2-8-6-12z" fill="#7FB8D9"/>' +
    '<circle cx="29" cy="40" r="1.6" fill="#FFFFFF" opacity="0.6"/>' +
    '</svg>';

  const TEATREE_IMAGE_SVG =
    '<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">' +
    '<rect x="8" y="22" width="48" height="36" rx="12" fill="#FFFFFF" stroke="#E5E5E5" stroke-width="2"/>' +
    '<rect x="10" y="14" width="44" height="10" rx="5" fill="#BFE3DC"/>' +
    '<rect x="16" y="8" width="32" height="8" rx="4" fill="#8FCFC2"/>' +
    '<path d="M32 30c-4 4-6 9-6 13 0 3.8 2.7 6.5 6 6.5s6-2.7 6-6.5c0-4-2-9-6-13z" fill="#5FB6A6"/>' +
    '<circle cx="30" cy="42" r="1.6" fill="#FFFFFF" opacity="0.6"/>' +
    '</svg>';

  const BRIGHT_IMAGE_SVG =
    '<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">' +
    '<rect x="24" y="2" width="16" height="6" rx="3" fill="#E3B23C"/>' +
    '<rect x="20" y="6" width="24" height="14" rx="4" fill="#F3D48A"/>' +
    '<path d="M18 20 L46 20 L42 58 Q42 60 40 60 L24 60 Q22 60 22 58 Z" fill="#FFFFFF" stroke="#E5E5E5" stroke-width="2"/>' +
    '<path d="M32 30c-4 4-6 8-6 12 0 3.5 2.7 6 6 6s6-2.5 6-6c0-4-2-8-6-12z" fill="#F0C24B"/>' +
    '<circle cx="29" cy="40" r="1.6" fill="#FFFFFF" opacity="0.6"/>' +
    '</svg>';

  const PINK_CREAM_IMAGE_SVG =
    '<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">' +
    '<rect x="8" y="22" width="48" height="36" rx="12" fill="#FFFFFF" stroke="#E5E5E5" stroke-width="2"/>' +
    '<rect x="10" y="14" width="44" height="10" rx="5" fill="#F3D2D8"/>' +
    '<rect x="16" y="8" width="32" height="8" rx="4" fill="#E8A9B6"/>' +
    '<path d="M32 44 C28 39 22 41 22 46 C22 51 32 56 32 56 C32 56 42 51 42 46 C42 41 36 39 32 44 Z" fill="#E8879A"/>' +
    '</svg>';

  const CLEANSER_IMAGE_SVG =
    '<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">' +
    '<rect x="26" y="2" width="6" height="10" rx="2" fill="#9BB7D4"/>' +
    '<path d="M20 12 L38 12 L34 8 L24 8 Z" fill="#9BB7D4"/>' +
    '<rect x="18" y="12" width="8" height="10" rx="2" fill="#BFD3E8"/>' +
    '<rect x="16" y="20" width="32" height="38" rx="10" fill="#FFFFFF" stroke="#E5E5E5" stroke-width="2"/>' +
    '<path d="M24 38c0-4 3.5-7 8-7s8 3 8 7-3.5 9-8 9-8-5-8-9z" fill="#7FA9D9" opacity="0.85"/>' +
    '</svg>';

  const PRODUCT_CATALOG = [
    {
      name: "리페어 시카 크림 (예시)",
      category: "크림",
      skinTypes: ["건성"],
      textures: ["촉촉한 밀착 타입", "묵직한 타입"],
      effects: ["보습", "장벽강화", "진정"],
      tags: ["저자극", "장벽강화"],
      desc: "세라마이드·판테놀 함유로 진정 + 보습, 촉촉한 밀착 타입. 코스맥스 제조 예시 제품이에요.",
      price: "₩18,000대 (예시가)",
      image: CREAM_IMAGE_SVG,
      searchQuery: "시카크림"
    },
    {
      name: "판테놀 수딩 세럼 (예시)",
      category: "세럼",
      skinTypes: ["건성", "수부지"],
      textures: ["가볍고 산뜻한 타입"],
      effects: ["진정", "보습"],
      tags: ["저자극", "보습"],
      desc: "가볍게 스며드는 산뜻한 타입, 붉은기 진정에 도움. 코스맥스 제조 예시 제품이에요.",
      price: "₩22,000대 (예시가)",
      image: SERUM_IMAGE_SVG,
      searchQuery: "판테놀 세럼"
    },
    {
      name: "티트리 퓨어 젤크림 (예시)",
      category: "크림",
      skinTypes: ["지성", "복합성", "수부지"],
      textures: ["가볍고 산뜻한 타입"],
      effects: ["피지조절", "트러블 개선", "각질 케어"],
      tags: ["피지조절", "산뜻한 젤 타입"],
      desc: "티트리·살리실산 함유로 피지·트러블 케어, 가볍게 스며드는 젤 타입. 코스맥스 제조 예시 제품이에요.",
      price: "₩17,000대 (예시가)",
      image: TEATREE_IMAGE_SVG,
      searchQuery: "티트리 젤크림"
    },
    {
      name: "나이아신 브라이트닝 에센스 (예시)",
      category: "에센스",
      skinTypes: ["복합성", "지성", "건성"],
      textures: ["가볍고 산뜻한 타입"],
      effects: ["미백", "모공케어"],
      tags: ["미백", "모공케어"],
      desc: "나이아신아마이드 함유로 톤 개선 + 모공 케어, 산뜻하게 스며드는 타입. 코스맥스 제조 예시 제품이에요.",
      price: "₩24,000대 (예시가)",
      image: BRIGHT_IMAGE_SVG,
      searchQuery: "나이아신아마이드 에센스"
    },
    {
      name: "콜라겐 탄력 크림 (예시)",
      category: "크림",
      skinTypes: ["건성", "복합성"],
      textures: ["묵직한 타입", "촉촉한 밀착 타입"],
      effects: ["탄력", "보습"],
      tags: ["탄력", "고보습"],
      desc: "콜라겐 함유로 탄력 + 보습 케어, 묵직하게 밀착되는 타입. 코스맥스 제조 예시 제품이에요.",
      price: "₩26,000대 (예시가)",
      image: PINK_CREAM_IMAGE_SVG,
      searchQuery: "콜라겐 탄력크림"
    },
    {
      name: "약산성 저자극 클렌저 (예시)",
      category: "클렌저",
      skinTypes: ["지성", "복합성", "건성", "수부지"],
      textures: ["가볍고 산뜻한 타입"],
      effects: ["진정", "트러블 개선"],
      tags: ["저자극", "약산성"],
      desc: "약산성 포뮬러로 자극 없이 산뜻하게 세안, 트러블 진정에 도움. 코스맥스 제조 예시 제품이에요.",
      price: "₩15,000대 (예시가)",
      image: CLEANSER_IMAGE_SVG,
      searchQuery: "약산성 클렌저"
    }
  ];

  // 고민(concern)이 제품 효과(effect) 태그와 매칭되도록 하는 매핑
  const CONCERN_TO_EFFECT = { "민감": "진정", "여드름": "트러블 개선", "각질": "각질 케어" };

  function scoreProduct(p, ctx){
    let score = 0;
    if(ctx.category && p.category === ctx.category) score += 4;
    if(p.skinTypes.includes(ctx.primarySkinType)) score += 3;
    if(ctx.secondarySkinType && p.skinTypes.includes(ctx.secondarySkinType)) score += 1.5;
    if(ctx.texture && p.textures.includes(ctx.texture)) score += 2;
    if(ctx.effect){
      ctx.effect.split(/,\s*/).forEach((e) => { if(p.effects.includes(e.trim())) score += 2; });
    }
    ctx.concerns.forEach((c) => {
      const mappedEffect = CONCERN_TO_EFFECT[c];
      if(mappedEffect && p.effects.includes(mappedEffect)) score += 1;
    });
    return score;
  }

  function renderProductCards(){
    const ctx = {
      primarySkinType: diagnosisResult.primary_skin_type,
      secondarySkinType: diagnosisResult.secondary_skin_type,
      concerns: diagnosisResult.concerns,
      category: productSlots.category,
      texture: productSlots.texture,
      effect: productSlots.effect
    };
    const products = PRODUCT_CATALOG
      .map((p) => ({ p: p, score: scoreProduct(p, ctx) }))
      .sort((a, b) => b.score - a.score)
      .slice(0, 2)
      .map((s) => s.p);

    products.forEach((p) => {
      const card = document.createElement('div');
      card.className = 'product-card';
      card.innerHTML =
        '<div class="p-top">' +
          '<div class="p-image">' + p.image + '</div>' +
          '<div class="p-meta">' +
            '<p class="p-name">' + p.name + '</p>' +
            '<div class="p-tags">' + p.tags.map((t) => '<span class="p-tag">' + t + '</span>').join('') + '</div>' +
          '</div>' +
        '</div>' +
        '<p class="p-desc">' + p.desc + '</p>' +
        '<div class="p-bottom">' +
          '<span class="p-price">' + p.price + '</span>' +
          '<button class="p-link" type="button">올리브영에서 보기 →</button>' +
        '</div>';
      card.querySelector('.p-link').addEventListener('click', () => {
        const url = 'https://www.oliveyoung.co.kr/store/search/getSearchMain.do?query=' + encodeURIComponent(p.searchQuery);
        window.open(url, '_blank', 'noopener');
        showToast('올리브영 "' + p.searchQuery + '" 검색결과로 이동해요 🙂');
      });
      chatScroll2.appendChild(card);
    });

    const note = document.createElement('div');
    note.className = 'product-note';
    note.textContent = '* 위 제품은 예시이며, 실제 코스맥스 제조 올리브영 제품 DB 연동 후 교체됩니다.';
    chatScroll2.appendChild(note);

    chatScroll2.scrollTop = chatScroll2.scrollHeight;
  }

  sendBtn2.addEventListener('click', handleProductSend);
  chatInput2.addEventListener('keydown', (e) => {
    if(e.key === 'Enter') handleProductSend();
  });

  function showToast(msg){
    toast.textContent = msg;
    toast.classList.add('show');
    setTimeout(() => toast.classList.remove('show'), 2200);
  }
</script>

</body>
</html>

"""

components.html(HTML_CONTENT, height=900, scrolling=False)
