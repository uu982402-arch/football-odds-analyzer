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
.card {
    background-color: #161b22;
    border-radius: 16px;
    padding: 24px;
    margin-top: 20px;
    border: 2px solid #2a2f3a;
    text-align: center;
}
.result-text { font-size: 1.8rem; font-weight: 800; }
.super { color: #ff4d4d; }
.strong { color: #ff9800; }
.mid { color: #ffd54f; }
.pass { color: #9e9e9e; }
button { border-radius: 10px !important; font-weight: 700 !important; }
input { background-color: #0e1117 !important; color: #ffffff !important; }
@media (max-width: 768px) {
  .block-container { padding: 1rem; }
  h1 { font-size: 1.6rem; text-align: center; }
  input { font-size: 1rem; padding: 0.6rem; }
  button { width: 100%; font-size: 1.05rem; }
}
/* 로고/Arch/툴바 강제 숨김 */
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
    fav = min(home, away)
    fav_side = "홈" if home < away else "원정"
    gap = abs(home - away)

    # PASS 기준
    if min(home, away) < 1.60:
        return "PASS", "pass"

    # 혼전
    if sport in ["축구", "하키"] and gap < 0.25 and draw < 3.4:
        return "PASS", "pass"

    # 초강승
    if fav <= 1.85 and (draw >= 3.6 or sport != "축구") and gap >= 1.0:
        return f"초강승 ({fav_side} 승)", "super"

    # 강승
    if fav <= 2.05 and (draw >= 3.4 or sport != "축구") and gap >= 0.7:
        return f"강승 ({fav_side} 승)", "strong"

    # 중승
    if fav <= 2.40:
        return f"중승 ({fav_side} 승)", "mid"

    # 그 외
    return "PASS", "pass"

# =========================
# 분석 버튼 + 결과 카드
# =========================
if st.button("분석하기"):
    check_rate_limit()
    result_text, result_class = analyze_odds(home, draw, away, sport=sport)
    st.markdown(f'<div class="card"><div class="result-text {result_class}">{result_text}</div></div>', unsafe_allow_html=True)

# =========================
# 하단 광고 버튼
# =========================
ad_id = "AD_001"
click_token = str(uuid.uuid4())
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
