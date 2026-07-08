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
      <span class="progress-label" id="progressLabel">0/10</span>
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

  const TOTAL_TURNS = 10;
  let turnCount = 0;

  const followUps = [
    "오오, 그러쉬구놔~ 세안하고 나면 얼굴이 땡기는 편이세요, 아니면 좀 번들거리는 편이세요?",
    "혹시 새 제품 쓰셨다가 트러블이 확 올라온 적 있으세요? 그때 어떤 제품 쓰셨는지 기억나세요?",
    "여드름 나면 좁쌀처럼 오돌토돌한 편이세요, 아니면 빨갛게 염증성으로 올라오는 편이세요?",
    "각질은 어떠세요? 손으로 만졌을 때 까슬까슬한 부위 있으세요?",
    "햇빛 좀 쬐면 금방 벌게지거나 화끈거리는 편이세요?",
    "요즘 잠이 부족하거나 스트레스 받는 시기이셨나요? 피부는 생활 패턴이랑도 정말 연결돼있거든요",
    "계절 바뀔 때 피부 컨디션이 많이 달라지시나요? 여름이랑 겨울 비교하면 어떠세요?",
    "지금 쓰고 계신 스킨케어, 순서대로 말씀해주시겠어요? (토너, 에센스, 크림 이런 거요)",
    "마지막 질문이에요! 요즘 제일 신경쓰이는 피부 고민, 딱 하나만 뽑으면 뭔가요?"
  ];

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
    progressDots.innerHTML = '';
    for(let i=0;i<TOTAL_TURNS;i++){
      const d = document.createElement('div');
      d.className = 'dot' + (i < turnCount ? ' filled' : '');
      progressDots.appendChild(d);
    }
    progressLabel.textContent = `${Math.min(turnCount,TOTAL_TURNS)}/${TOTAL_TURNS}`;
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
    turnCount++;
    renderDots();

    if(turnCount >= TOTAL_TURNS){
      typeAndSend(chatScroll, "네에, 이 정도면 피부 상태가 딱 파악됐어용! 아래 '제품 추천 받으러 가기' 눌러서 결과 보러 가실까요? 👇\n(더 이야기하고 싶으시면 계속 말씀해주셔도 돼요, 더 정확해져요!)", 500);
      unlockNextButton();
    } else {
      const next = followUps[turnCount - 1] || "조으음 더 자세히 말씀해주시겠어용? 어떤 느낌인지 궁금하네용!";
      typeAndSend(chatScroll, next, 500 + Math.random()*300);
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

  const DIAGNOSIS_MESSAGE =
    "자아, 말씀 다 들어봤어용! 종합해보니 고객님은 수분 부족형 민감성 피부에 가까운 것 같아요 😊\n" +
    "세안 후에 땡기는 느낌 있으시고, 새 제품 쓰면 트러블이 잘 올라오는 편이라 피부 장벽이 살짝 약해진 상태일 가능성이 높아요.\n\n" +
    "그래서 제품은 이런 방향으로 고르시는 게 좋아요:\n" +
    "🔹 저자극 순한 제품 (향료·알코올 최소화)\n" +
    "🔹 세라마이드처럼 장벽 강화해주는 기능성 제품\n" +
    "🔹 고농도 산(AHA/BHA)이 들어간 자극적인 제품은 당분간 피하시는 게 좋아요\n\n" +
    "피부과 시술은 수분을 채워주는 스킨부스터/필링 계열을 추천드릴게요! 각질 제거 위주의 강한 박피나 압출은 지금 피부엔 좀 자극적일 수 있어요.\n\n" +
    "이제 이 방향에 맞는 코스맥스 제품, 구체적으로 골라드릴까요?";

  let screenSwitched = false;
  nextBtn.addEventListener('click', () => {
    if(nextBtn.disabled || screenSwitched) return;
    screenSwitched = true;
    screenDiagnosis.classList.remove('active');
    screenProduct.classList.add('active');
    progressWrap.style.display = 'none';
    typeAndSend(chatScroll2, DIAGNOSIS_MESSAGE, 500);
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
    "미백":"미백", "탄력":"탄력", "트러블":"트러블 개선", "각질":"각질 케어"
  };

  // 진단 결과("수분 부족형 민감성 피부")에 근거한 기본값 — 사용자가 직접 고르지 않고 "네가 알아서/맞는 걸로" 위임할 때 씀
  const DELEGATE_KEYWORDS = ["맞는", "적합", "알아서", "너가 골라", "니가 골라", "정해줘", "추천해줘", "골라줘", "아무거나", "다 좋아"];
  const DIAGNOSIS_DEFAULT_EFFECT = "보습, 장벽강화";
  const DIAGNOSIS_DEFAULT_TEXTURE = "촉촉한 밀착 타입";

  const productSlots = { category:null, texture:null, effect:null };
  let effectFromDelegation = false;

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

    // 명시적 키워드가 없는데 "위임" 표현이면, 아까 진단 결과 기준으로 대신 채워줌
    const delegated = DELEGATE_KEYWORDS.some((k) => text.includes(k));
    if(delegated){
      if(!productSlots.effect){ productSlots.effect = DIAGNOSIS_DEFAULT_EFFECT; effectFromDelegation = true; }
      if(!productSlots.texture){ productSlots.texture = DIAGNOSIS_DEFAULT_TEXTURE; }
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
        ? "네에, 아까 진단해드린 대로 보습 + 장벽강화 중심으로 딱 골라드릴게용! 👇"
        : "네에, 딱 맞는 제품 골라드렸어용! 👇";
      typeAndSend(chatScroll2, closing, 500).then(renderProductCards);
    }
  }

  function renderProductCards(){
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

    const products = [
      {
        name: "리페어 시카 크림 (예시)",
        tags: ["저자극", "장벽강화"],
        desc: "세라마이드·판테놀 함유로 진정 + 보습, 촉촉한 밀착 타입. 코스맥스 제조 예시 제품이에요.",
        price: "₩18,000대 (예시가)",
        image: CREAM_IMAGE_SVG,
        searchQuery: "시카크림"
      },
      {
        name: "판테놀 수딩 세럼 (예시)",
        tags: ["저자극", "보습"],
        desc: "가볍게 스며드는 산뜻한 타입, 붉은기 진정에 도움. 코스맥스 제조 예시 제품이에요.",
        price: "₩22,000대 (예시가)",
        image: SERUM_IMAGE_SVG,
        searchQuery: "판테놀 세럼"
      }
    ];

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
