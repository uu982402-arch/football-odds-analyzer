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
.block-container {
    padding:2.2rem 1.2rem;
    max-width:980px;
    margin:0 auto;
}

/* Streamlit 기본 UI 제거 */
[data-testid="stHeader"], header, footer, #MainMenu,
[data-testid="stToolbar"], [data-testid="stDecoration"],
[data-testid="collapsedControl"] {
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

/* ===== 종목 선택 박스 스타일 정리 ===== */
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

/* ===== 분석 버튼 (완전 중앙 + 텍스트 정렬) ===== */
div[data-testid="stButton"] { width:100% !important; }
div[data-testid="stButton"] > div {
    width:100% !important;
    display:flex !important;
    justify-content:center !important;
}

div[data-testid="stButton"] button {
    display:flex !important;
    align-items:center !important;
    justify-content:center !important;

    width:min(460px,85%) !important;
    height:62px !important;

    margin:22px auto 14px auto !important;
    padding:0 !important;

    background:linear-gradient(90deg,#ff9800,#ff5722) !important;
    color:#111 !important;

    font-size:1.35rem !important;
    font-weight:900 !important;
    letter-spacing:0.02em !important;

    border:none !important;
    border-radius:20px !important;
    box-shadow:0 10px 26px rgba(0,0,0,0.45) !important;
}

div[data-testid="stButton"] button:hover {
    transform:scale(1.03);
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

/* ===== 폰트/글자 크기 통일 ===== */
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

/* 모바일 미세 조정 */
@media (max-width:768px){
    .block-container { padding:1.6rem 1rem; }
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

    if fav < 1.60: return "PASS", "pass"
    if sport in ["축구", "하키"] and gap < 0.25 and draw < 3.4: return "PASS", "pass"
    if fav <= 1.85 and (draw >= 3.6 or sport != "축구") and gap >= 1.0:
        return f"초강승 ({fav_side} 승)", "super"
    if fav <= 2.05 and (draw >= 3.4 or sport != "축구") and gap >= 0.7:
        return f"강승 ({fav_side} 승)", "strong"
    if fav <= 2.40: return f"중승 ({fav_side} 승)", "mid"
    return "PASS", "pass"

# =========================
# ANALYZE BUTTON
# =========================
if st.button("분석하기"):
    check_rate_limit()
    text, cls = analyze_odds(home, draw, away, sport)
    st.markdown(
        f'<div class="result-card"><div class="result-text {cls}">{text}</div></div>',
        unsafe_allow_html=True
    )

# =========================
# ADS (모바일 3개 보이게 height 넉넉)
# =========================
today_users = random.randint(72, 128)

ads_html = f"""
<div style="text-align:center;margin-top:36px;">
<hr style="border:0;border-top:1px solid #333;width:60%;margin:0 auto 14px;">
<h2 style="margin:0;font-weight:900;">🦋 88 🦋 보증업체</h2>
<div style="margin-top:6px;color:#bbb;font-weight:700;">✔ 고액 환전 OK · 실시간 검증 완료</div>
<div style="margin-top:6px;color:#aaa;">👥 오늘 방문자 <b style="color:#ffd54f;">{today_users}명</b> 이용</div>
</div>
"""

components.html(ads_html, height=220)

