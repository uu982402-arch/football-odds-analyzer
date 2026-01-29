import streamlit as st
from datetime import datetime, timedelta
import uuid

# =========================
# 🎨 GLOBAL STYLE + UI 업그레이드 + 로고/Arch/툴바 강제 숨김
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
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
}
.result-text { font-size: 1.9rem; font-weight: 800; }

/* 결과 색상 */
.super { color: #ff4d4d; }
.strong { color: #ff9800; }
.mid { color: #ffd54f; }
.pass { color: #9e9e9e; }

/* 분석 버튼 */
.stButton>button {
    background: linear-gradient(90deg, #ff9800, #ff5722);
    color: white;
    font-weight: 700;
    padding: 12px 25px;
    border-radius: 12px;
    font-size: 1.1rem;
    transition: transform 0.2s;
    width: 100%;
}
.stButton>button:hover { transform: scale(1.05); }

/* 종목 선택 */
.css-1f6l0j1 { background-color: #161b22; border-radius: 10px; padding: 8px 12px; color: #ffffff; }

/* 입력 필드 */
input { background-color: #0e1117 !important; color: #ffffff !important; }

/* 광고 버튼 */
.ad-button { padding:12px 24px; border-radius:12px; font-weight:bold; font-size:1.05rem; text-decoration:none; color:white; margin:5px; display:inline-block; }

/* 모바일 대응 */
@media (max-width: 768px) {
  .block-container { padding: 1rem; }
  h1 { font-size: 1.6rem; text-align: center; }
  input { font-size: 1rem; padding: 0.6rem; }
  .stButton>button { font-size: 1.05rem; width: 100%; }
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
# 배당 입력 UI
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
# 광고 버튼 3개 (광고 B만 안내창)
# =========================
ads = [
    {"id": "AD_001", "label": "✅ 비윈코리아 ", "color": "#ff9800", "url": "https://uzu59.netlify.app/", "alert": False},
    {"id": "AD_002", "label": "✅ 벳지", "color": "#4caf50", "url": "https://b88-et.com", 
     "alert": True, "message": "⚠ 안내: 도메인명: 벳지 가입코드 : BANGU 담당자:@UZU59"},
    {"id": "AD_003", "label": "✅ 캡스", "color": "#2196f3", "url": "https://caps-22.com", 
     "alert": True, "message": "⚠ 안내: 도메인명: 캡스 가입코드 : RUST 담당자:@UZU59"}
]

ad_html = '<div style="text-align:center; margin-top: 30px;">'

for ad in ads:
    token = str(uuid.uuid4())
    ad_url = f"{ad['url']}?ad={ad['id']}&token={token}"
    
    if ad["alert"]:
        message = ad["message"].replace("'", "\\'").replace("\n", "\\n")
        ad_html += f"""
        <a href="#" onclick="
            alert('{message}');
            window.open('{ad_url}', '_blank');
            return false;"
           class="ad-button"
           style="background-color:{ad['color']}">
           {ad['label']}
        </a>
        """
    else:
        ad_html += f"""
        <a href="{ad_url}" target="_blank" class="ad-button" style="background-color:{ad['color']}">
           {ad['label']}
        </a>
        """

ad_html += '</div>'

st.markdown(ad_html, unsafe_allow_html=True)

