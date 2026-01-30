import streamlit as st
from datetime import datetime, timedelta
import uuid
import random
import streamlit.components.v1 as components

# =========================
# Page config
# =========================
st.set_page_config(page_title=" 88 ", layout="centered")

# =========================
# GLOBAL UI + FINAL CSS
# =========================
st.markdown("""
<style>
/* ===== 기본 배경 ===== */
[data-testid="stAppViewContainer"] { background:#0e1117; }
html, body, .stApp {
    background:#0e1117 !important;
    color:#e6e6e6 !important;
    font-family: Arial, sans-serif;
}

/* 레이아웃 */
.block-container { padding:2.2rem 1.2rem; max-width:980px; margin:0 auto; }

/* Streamlit 기본 UI 제거 */
[data-testid="stHeader"], header, footer, #MainMenu,
[data-testid="stToolbar"], [data-testid="stDecoration"], [data-testid="collapsedControl"] {
    display:none !important;
    height:0 !important;
}

/* ===== 제목 ===== */
.main-title {
    text-align:center;
    font-size:2.5rem;
    font-weight:900;
    margin:0.4rem 0 0.8rem 0;
}

/* ===== 종목 선택 스타일 ===== */
[data-testid="stSelectbox"] > div {
    background:transparent !important;
    border:none !important;
    box-shadow:none !important;
}

/* 종목선택 아래 이상한 남색 바 제거 */
div[data-testid="stSelectbox"] + div:empty { display:none !important; }
div[data-testid="stSelectbox"] + div > div:empty { display:none !important; }
div[data-testid="stSelectbox"] + div:has(> div:empty) { display:none !important; }

/* ===== 배당 입력 카드 ===== */
.input-card {
    background:#161b22;
    border:1px solid #2a2f3a;
    border-radius:20px;
    padding:22px;
    margin:14px 0 18px 0;
    box-shadow:0 8px 22px rgba(0,0,0,0.45);
}

/* ===== 결과 카드 ===== */
.result-card {
    background:#161b22;
    border:1px solid #2a2f3a;
    border-radius:18px;
    padding:22px;
    margin-top:14px;
    text-align:center;
    box-shadow:0 8px 22px rgba(0,0,0,0.45);
}
.result-text { font-size:2rem; font-weight:900; }
.super { color:#ff4d4d; }
.strong { color:#ff9800; }
.mid { color:#ffd54f; }
.pass { color:#9e9e9e; }

/* ===== 폼 글자 크기/폰트 ===== */
label {
    font-size:1.05rem !important;
    font-weight:800 !important;
    color:#d8d8d8 !important;
}
div[data-testid="stSelectbox"] * {
    font-size:1.15rem !important;
    font-weight:800 !important;
}
div[data-testid="stNumberInput"] input {
    font-size:1.25rem !important;
    font-weight:900 !important;
}
div[data-testid="stNumberInput"] input,
div[data-testid="stSelectbox"] div[role="combobox"] {
    min-height:52px !important;
    border-radius:14px !important;
}

/* =========================
   ✅ 분석 버튼 PRO UI (안 깨지게)
   - 핵심: .stButton>button 타겟
   - 줄바꿈 방지
   ========================= */
.stButton > button {
    width: 100% !important;             /* 가운데 컬럼에서 꽉 차게 */
    max-width: 520px !important;
    height: 66px !important;
    padding: 0 22px !important;

    display: flex !important;
    align-items: center !important;
    justify-content: center !important;

    border-radius: 18px !important;     /* pill 말고 둥근 사각(더 안정적) */
    border: 1px solid rgba(255,255,255,0.14) !important;

    background:
      radial-gradient(120% 180% at 20% 0%, rgba(255,255,255,0.18) 0%, rgba(255,255,255,0) 45%),
      linear-gradient(90deg,#ff9800 0%, #ff6a00 45%, #ff2d55 100%) !important;

    color: #0b0b0b !important;
    font-size: 1.45rem !important;
    font-weight: 1000 !important;
    letter-spacing: 0.02em !important;

    white-space: nowrap !important;     /* ✅ '분석하기' 줄바꿈 방지 */
    line-height: 1 !important;

    box-shadow:
      0 14px 34px rgba(0,0,0,0.50),
      inset 0 1px 0 rgba(255,255,255,0.25) !important;

    transition: transform .16s ease, box-shadow .16s ease, filter .16s ease !important;
}
.stButton > button:hover {
    transform: translateY(-2px) scale(1.02) !important;
    filter: brightness(1.02) !important;
    box-shadow:
      0 18px 42px rgba(0,0,0,0.58),
      inset 0 1px 0 rgba(255,255,255,0.28) !important;
}
.stButton > button:active {
    transform: translateY(0px) scale(0.995) !important;
    filter: brightness(0.99) !important;
}

/* 모바일 */
@media (max-width:768px){
    .block-container { padding:1.6rem 1rem; }
    .stButton > button{
        height:62px !important;
        font-size:1.28rem !important;
    }
}
</style>
""", unsafe_allow_html=True)

# =========================
# TITLE
# =========================
st.markdown('<div class="main-title">🦋 88 🦋</div>', unsafe_allow_html=True)

# =========================
# SPORT SELECT
# =========================
sport = st.selectbox("종목 선택", ["축구", "농구", "하키"])

# =========================
# INPUT CARD
# =========================
st.markdown('<div class="input-card">', unsafe_allow_html=True)
if sport in ["축구", "하키"]:
    home = st.number_input("홈 배당", min_value=1.01, step=0.01, format="%.2f")
    draw = st.number_input("무 배당", min_value=1.01, step=0.01, format="%.2f")
    away = st.number_input("원정 배당", min_value=1.01, step=0.01, format="%.2f")
else:
    home = st.number_input("홈 배당", min_value=1.01, step=0.01, format="%.2f")
    away = st.number_input("원정 배당", min_value=1.01, step=0.01, format="%.2f")
    draw = 0.0
st.markdown('</div>', unsafe_allow_html=True)

# =========================
# RATE LIMIT
# =========================
if "last_click" not in st.session_state:
    st.session_state.last_click = datetime.min

def check_rate_limit():
    now = datetime.now()
    if now - st.session_state.last_click < timedelta(seconds=3):
        st.warning("⏳ 3초에 한 번만 가능합니다")
        st.stop()
    st.session_state.last_click = now

# =========================
# ANALYSIS LOGIC (유지)
# =========================
def analyze_odds(home, draw, away, sport="축구"):
    fav = min(home, away)
    fav_side = "홈" if home < away else "원정"
    gap = abs(home - away)

    if fav < 1.60:
        return "PASS", "pass"
    if sport in ["축구", "하키"] and gap < 0.25 and draw < 3.4:
        return "PASS", "pass"
    if fav <= 1.85 and (draw >= 3.6 or sport != "축구") and gap >= 1.0:
        return f"초강승 ({fav_side} 승)", "super"
    if fav <= 2.05 and (draw >= 3.4 or sport != "축구") and gap >= 0.7:
        return f"강승 ({fav_side} 승)", "strong"
    if fav <= 2.40:
        return f"중승 ({fav_side} 승)", "mid"
    return "PASS", "pass"

# =========================
# ✅ 분석 버튼: 레이아웃으로 "완전 중앙" 강제
# =========================
left, center, right = st.columns([1, 2, 1])
with center:
    clicked = st.button("분석하기")

if clicked:
    check_rate_limit()
    text, cls = analyze_odds(home, draw, away, sport)
    st.markdown(
        f'<div class="result-card"><div class="result-text {cls}">{text}</div></div>',
        unsafe_allow_html=True
    )

# =========================
# ADS (버튼 3개 + 모달 + 모바일 세로 / PC 가로)
# =========================
today_users = random.randint(72, 128)

ads = [
    {"id": "AD_001", "label": "B WIN",  "color": "#ff5722", "url": "https://uzu59.netlify.app/",
     "need_modal": False, "message": ""},
    {"id": "AD_002", "label": "BETZY",  "color": "#4caf50", "url": "https://b88-et.com",
     "need_modal": True,  "message": "도메인: BETZY\\n가입코드: BANGU\\n담당자: @UZU59"},
    {"id": "AD_003", "label": "CAPS",   "color": "#2196f3", "url": "https://caps-22.com",
     "need_modal": True,  "message": "도메인: CAPS\\n가입코드: RUST\\n담당자: @UZU59"},
]

buttons_html = ""
for ad in ads:
    token = str(uuid.uuid4())
    ad_url = f"{ad['url']}?ad={ad['id']}&token={token}"

    if ad["need_modal"]:
        buttons_html += f"""
        <button class="ad-btn" style="border-color:{ad['color']};"
                title="공식 보증업체"
                onclick="openModal('{ad_url}', `{ad['message']}`)">
            <div class="ad-name" style="color:{ad['color']};">{ad['label']}</div>
            <div class="ad-sub">공식 보증업체</div>
        </button>
        """
    else:
        buttons_html += f"""
        <a class="ad-link" href="{ad_url}" target="_blank" style="border-color:{ad['color']};" title="공식 보증업체">
            <div class="ad-name" style="color:{ad['color']};">{ad['label']}</div>
            <div class="ad-sub">공식 보증업체</div>
        </a>
        """

ads_html = f"""
<div class="ads-wrap">
  <div class="line">──────────────</div>
  <div class="ads-title">🦋 88 🦋 보증업체</div>
  <div class="ads-desc">✔ 고액 환전 OK · 실시간 검증 완료</div>
  <div class="ads-visit">👥 오늘 방문자 <b>{today_users}명</b> 이용</div>
  <div class="line">──────────────</div>

  <div class="ads-row">
    {buttons_html}
  </div>
</div>

<div class="modal-bg" id="modalBg">
  <div class="modal">
    <div class="modal-title">⚠ 공식 보증업체 안내</div>
    <div class="modal-text" id="modalText"></div>
    <div class="modal-actions">
      <button class="m-btn cancel" onclick="closeModal()">취소</button>
      <button class="m-btn ok" onclick="goAd()">확인 후 이동</button>
    </div>
  </div>
</div>

<style>
  body {{ margin:0; padding:0; background:transparent; font-family: Arial, sans-serif; }}

  .ads-wrap {{ margin-top: 34px; text-align:center; }}
  .line {{ color:#7a7a7a; font-weight:800; margin: 6px 0; }}
  .ads-title {{ color:#e6e6e6; font-weight:900; font-size: 1.55rem; margin-top: 8px; }}
  .ads-desc {{ margin-top: 6px; color:#bdbdbd; font-weight:700; font-size: 0.95rem; }}
  .ads-visit {{ margin-top: 6px; color:#a9a9a9; font-size: 0.9rem; }}
  .ads-visit b {{ color:#ffd54f; font-weight:900; }}

  .ads-row {{
    display:flex;
    justify-content:center;
    gap:16px;
    flex-wrap:wrap;
    margin: 18px 0 4px;
  }}

  .ad-btn, .ad-link {{
    width: 220px;
    height: 86px;
    border-radius: 18px;
    border: 2px solid #ffffff20;
    background: #ffffff;
    box-shadow: 0 10px 26px rgba(0,0,0,0.20);
    display:flex;
    flex-direction:column;
    align-items:center;
    justify-content:center;
    cursor:pointer;
    text-decoration:none;
    transition: transform .18s ease, box-shadow .18s ease;
  }}
  .ad-btn:hover, .ad-link:hover {{
    transform: translateY(-3px) scale(1.03);
    box-shadow: 0 16px 34px rgba(0,0,0,0.26);
  }}
  .ad-name {{ font-weight: 900; font-size: 1.22rem; line-height: 1.1; }}
  .ad-sub {{ margin-top: 6px; font-size: 0.78rem; font-weight: 900; color:#000000a8; }}

  /* 모바일: 세로형 */
  @media (max-width: 720px) {{
    .ads-row {{ flex-direction: column; align-items: center; }}
    .ad-btn, .ad-link {{ width: 86vw; max-width: 360px; height: 76px; }}
  }}

  .modal-bg {{
    position: fixed; inset: 0;
    background: rgba(0,0,0,0.65);
    display:none;
    align-items:center;
    justify-content:center;
    z-index: 9999;
  }}
  .modal {{
    width: min(92vw, 420px);
    background: #161b22;
    border: 1px solid #2a2f3a;
    border-radius: 18px;
    padding: 18px 18px 16px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.45);
    color: #e6e6e6;
    text-align: left;
  }}
  .modal-title {{ font-size: 1.15rem; font-weight: 900; margin-bottom: 10px; }}
  .modal-text {{
    font-size: 0.98rem;
    color: #d6d6d6;
    line-height: 1.55;
    white-space: pre-line;
    margin-bottom: 14px;
  }}
  .modal-actions {{ display:flex; gap:10px; justify-content:flex-end; }}
  .m-btn {{ border:none; border-radius: 12px; padding: 10px 14px; font-weight: 900; cursor:pointer; }}
  .m-btn.cancel {{ background: #2a2f3a; color: #fff; }}
  .m-btn.ok {{ background: linear-gradient(90deg,#ff9800,#ff5722); color:#111; }}
</style>

<script>
  let __target = "";
  function openModal(url, msg) {{
    __target = url;
    document.getElementById("modalText").innerText = msg;
    document.getElementById("modalBg").style.display = "flex";
  }}
  function closeModal() {{
    document.getElementById("modalBg").style.display = "none";
    __target = "";
  }}
  function goAd() {{
    if (__target) window.open(__target, "_blank");
    closeModal();
  }}
</script>
"""

# ✅ 모바일에서도 광고 3개가 다 보이도록 충분한 높이
components.html(ads_html, height=640, scrolling=False)
