import streamlit as st
from datetime import datetime, timedelta
import uuid

# =========================
# 🎨 GLOBAL STYLE + UI
# =========================
st.markdown("""
<style>
html, body, [class*="css"] { background-color: #0e1117; color: #e6e6e6; font-family: 'Arial', sans-serif; }
.block-container { padding: 2rem; }

/* 카드 */
.card {
    background-color: #161b22;
    border-radius: 16px;
    padding: 24px;
    margin-top: 20px;
    border: 2px solid #2a2f3a;
    text-align: center;
    box-shadow: 0 4px 16px rgba(0,0,0,0.4);
}
.result-text { font-size: 2rem; font-weight: 900; }

/* 결과 색상 */
.super { color: #ff4d4d; }
.strong { color: #ff9800; }
.mid { color: #ffd54f; }
.pass { color: #9e9e9e; }

/* 분석 버튼 중앙 + 글자 진하게 */
.stButton>button {
    background: linear-gradient(90deg, #ff9800, #ff5722);
    color: #0d47a1;
    font-weight: 900;
    padding: 14px 30px;
    border-radius: 16px;
    font-size: 1.25rem;
    transition: transform 0.2s;
    display: block;
    margin-left:auto;
    margin-right:auto;
    width: 100%;
}
.stButton>button:hover { transform: scale(1.05); }

/* 종목 선택 */
.css-1f6l0j1 { background-color: #161b22; border-radius: 10px; padding: 8px 12px; color: #ffffff; }

/* 입력 필드 */
input { background-color: #0e1117 !important; color: #ffffff !important; }

/* 광고 버튼 컨테이너 */
.ad-container {
    display:flex;
    justify-content: space-around; /* PC 가로형 */
    flex-wrap: wrap;
    margin-top:30px;
}

/* 광고 버튼 카드형 */
.ad-button {
    display:flex;
    justify-content:center;
    align-items:center;
    width:200px;
    height:80px;
    border-radius:18px;
    font-weight:900;
    font-size:1.2rem;
    background-color:white; /* 배경 흰색 */
    text-decoration:none;
    box-shadow: 0 6px 16px rgba(0,0,0,0.5);
    transition: transform 0.2s, box-shadow 0.2s;
}
.ad-button:hover { 
    transform: translateY(-3px) scale(1.05);
    box-shadow: 0 10px 20px rgba(0,0,0,0.6);
}

/* 광고 글자색 눈에 띄게 */
.ad-button:nth-child(1) { color:#ff5722; }  /* 주황 */
.ad-button:nth-child(2) { color:#4caf50; }  /* 초록 */
.ad-button:nth-child(3) { color:#2196f3; }  /* 파랑 */

/* 모바일 대응 */
@media (max-width: 768px) {
  .ad-container { flex-direction: column; align-items:center; }
  .ad-button { width:80%; height:60px; font-size:1rem; margin:5px 0; }
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
</style>
""", unsafe_allow_html=True)

# =========================
# 종목 선택
# =========================
st.markdown("## ⚽🏀🏒 전종목 배당 분석기")
sport = st.selectbox("종목 선택", ["축구", "농구", "하키"])
st.markdown(f"### {sport} 배당 입력")

# =========================
# 배당 입력
# =========================
if sport in ["축구", "하키"]:
    home = st.number_input("홈 배당", min_value=1.01, step=0.01, format="%.2f")
    draw = st.number_input("무 배당", min_value=1.01, step=0.01, format="%.2f")
    away = st.number_input("원정 배당", min_value=1.01, step=0.01, format="%.2f")
else:  # 농구
    home = st.number_input("홈 배당", min_value=1.01, step=0.01, format="%.2f")
    away = st.number_input("원정 배당", min_value=1.01, step=0.01, format="%.2f")
    draw = 0

# =========================
# 클릭 제한
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
    if min(home, away) < 1.60: return "PASS", "pass"
    if sport in ["축구", "하키"] and gap < 0.25 and draw < 3.4: return "PASS", "pass"
    if fav <= 1.85 and (draw >= 3.6 or sport != "축구") and gap >= 1.0: return f"초강승 ({fav_side} 승)", "super"
    if fav <= 2.05 and (draw >= 3.4 or sport != "축구") and gap >= 0.7: return f"강승 ({fav_side} 승)", "strong"
    if fav <= 2.40: return f"중승 ({fav_side} 승)", "mid"
    return "PASS", "pass"

# =========================
# 분석 버튼 + 결과 카드
# =========================
if st.button("분석하기"):
    check_rate_limit()
    result_text, result_class = analyze_odds(home, draw, away, sport=sport)
    st.markdown(f'<div class="card"><div class="result-text {result_class}">{result_text}</div></div>', unsafe_allow_html=True)

# =========================
# 광고 버튼 3개 카드형
# =========================
ads = [
    {"id": "AD_001", "label": " 비윈코리아", "url": "https://uzu59.netlify.app/", "alert": False, "color": "#ff5722"},
    {"id": "AD_002", "label": " 벳지", "url": "https://b88-et.com", "alert": True, 
     "message": "⚠ 안내: 도메인명: 벳지 가입코드 : BANGU 담당자:@UZU59", "color": "#4caf50"},
    {"id": "AD_003", "label": " 캡스", "url": "https://caps-22.com", "alert": True, 
     "message": "⚠ 안내: 도메인명: 캡스 가입코드 : RUST 담당자:@UZU59", "color": "#2196f3"}
]

st.markdown('<div class="ad-container">', unsafe_allow_html=True)

for ad in ads:
    token = str(uuid.uuid4())
    ad_url = f"{ad['url']}?ad={ad['id']}&token={token}"
    if ad["alert"]:
        msg = ad["message"].replace("'", "\\'")
        st.markdown(f"""
        <a href="#" onclick="alert('{msg}'); window.open('{ad_url}', '_blank'); return false;" 
           class="ad-button" style="background-color:white; color:{ad['color']}">{ad['label']}</a>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <a href="{ad_url}" target="_blank" class="ad-button" style="background-color:white; color:{ad['color']}">{ad['label']}</a>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
