import streamlit as st
from datetime import datetime, timedelta
import uuid

# =========================
# 🎨 GLOBAL STYLE + 로고/Arch/툴바 강제 숨김
# =========================
st.markdown("""
<style>
html, body, [class*="css"] { background-color: #0e1117; color: #e6e6e6; }
.block-container { padding: 2rem; }
.card { background-color: #161b22; border-radius: 14px; padding: 18px; margin-top: 16px; border: 1px solid #2a2f3a; }
.super { color: #ff4d4d; font-weight: 800; }
.strong { color: #ff9800; font-weight: 700; }
.mid { color: #ffd54f; font-weight: 600; }
.pass { color: #9e9e9e; font-weight: 600; }
button { border-radius: 10px !important; font-weight: 700 !important; }
input { background-color: #0e1117 !important; color: #ffffff !important; }
.log { font-size: 0.85rem; color: #b0b0b0; margin-top: 6px; }
@media (max-width: 768px) {
  .block-container { padding: 1rem; }
  h1 { font-size: 1.6rem; text-align: center; }
  input { font-size: 1rem; padding: 0.6rem; }
  button { width: 100%; font-size: 1.05rem; }
}
/* 로고/Arch/톱니바/툴바 강제 숨김 */
header, footer, #MainMenu, [data-testid="stToolbar"], [data-testid="stDecoration"], 
[data-testid="collapsedControl"], [data-testid="stVerticalBlock"] > div:first-child {
    display: none !important;
    visibility: hidden !important;
    height: 0 !important;
    width: 0 !important;
    overflow: hidden !important;
}
@media (max-width: 768px) {
    header, footer, #MainMenu, [data-testid="stToolbar"], [data-testid="stDecoration"],
    [data-testid="collapsedControl"], [data-testid="stVerticalBlock"] > div:first-child {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
        width: 0 !important;
        overflow: hidden !important;
    }
}
</style>
""", unsafe_allow_html=True)

# =========================
# 종목 선택
# =========================
sport = st.selectbox("종목 선택", ["축구", "농구", "하키"])
st.markdown(f"### {sport} 배당 입력")

# =========================
# 배당 입력 UI
# =========================
if sport in ["축구", "하키"]:
    home = st.number_input("홈 배당", min_value=1.01, step=0.01, format="%.2f")
    draw = st.number_input("무 배당", min_value=1.01, step=0.01, format="%.2f")
    away = st.number_input("원정 배당", min_value=1.01, step=0.01, format="%.2f")
else:  # 농구
    home = st.number_input("홈 배당", min_value=1.01, step=0.01, format="%.2f")
    away = st.number_input("원정 배당", min_value=1.01, step=0.01, format="%.2f")
    draw = 0  # 무승부 없음

# =========================
# 분석 버튼 클릭 제한 (3초)
# =========================
if "last_click" not in st.session_state:
    st.session_state.last_click = datetime.min

def check_rate_limit():
    now = datetime.now()
    if now - st.session_state.last_click < timedelta(seconds=3):
        st.warning("3초에 한 번만 클릭 가능")
        st.stop()
    st.session_state.last_click = now

# =========================
# 분석 로직
# =========================
def analyze_odds(home, draw, away, sport="축구"):
    logs = []
    if min(home, away) < 1.60:
        logs.append("배당 1.60 미만 → 기준 미달")
        return "PASS", logs
    fav = min(home, away)
    fav_side = "홈" if home < away else "원정"
    gap = abs(home - away)
    if sport in ["축구", "하키"] and gap < 0.25 and draw < 3.4:
        logs.append("홈/원정 배당 차이 미미 + 무 배당 낮음 → 혼전")
        return "PASS", logs
    if fav <= 1.85 and (draw >= 3.6 or sport != "축구") and gap >= 1.0:
        logs.append("저배당 안정 정배 + 무 방어 충분")
        return f"초강승 ({fav_side} 승)", logs
    if fav <= 2.05 and (draw >= 3.4 or sport != "축구") and gap >= 0.7:
        logs.append("안정 정배 구조")
        return f"강승 ({fav_side} 승)", logs
    if fav <= 2.40:
        logs.append("중배당 구간 → 변동성 존재")
        return f"중승 ({fav_side} 승)", logs
    logs.append("구조 불명확")
    return "PASS", logs

# =========================
# 분석 버튼 + 카드
# =========================
if st.button("분석하기"):
    check_rate_limit()
    result, logs = analyze_odds(home, draw, away, sport=sport)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    if "초강승" in result:
        st.markdown(f"<div class='super'>🔥 {result}</div>", unsafe_allow_html=True)
    elif "강승" in result:
        st.markdown(f"<div class='strong'>⚡ {result}</div>", unsafe_allow_html=True)
    elif "중승" in result:
        st.markdown(f"<div class='mid'>⚠ {result}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='pass'>❌ PASS</div>", unsafe_allow_html=True)
    with st.expander("분석 로그 보기"):
        for l in logs:
            st.markdown(f"• {l}")
    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# 하단 광고 버튼 (클릭 제한 없음, 랜덤 토큰 포함)
# =========================
ad_id = "AD_001"
click_token = str(uuid.uuid4())  # 랜덤 토큰 생성
ad_url = f"https://uzu59.netlify.app/?ad={ad_id}&token={click_token}"

ad_html = f"""
<div style="text-align:center; margin-top: 30px;">
    <a href="{ad_url}" target="_blank"
       style="
       background-color:#ff9800;
       color:white;
       padding:12px 24px;
       border-radius:10px;
       font-weight:bold;
       text-decoration:none;
       font-size:1.05rem;
       display:inline-block;
       ">
       ✅ 보증업체 
    </a>
</div>
"""
st.markdown(ad_html, unsafe_allow_html=True)
