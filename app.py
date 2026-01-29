import streamlit as st
from datetime import datetime, timedelta
import uuid
import streamlit.components.v1 as components

# =========================
# 🎨 프로 UI 스타일 + selectbox 박스 제거 (강력 적용)
# =========================
st.markdown("""
<style>
html, body, [class*="css"] {
    background-color:#0e1117;
    color:#e6e6e6;
    font-family:'Arial', sans-serif;
}
.block-container { padding:2rem; max-width:980px; margin:auto; }

/* === SELECTBOX 주변 박스(남색 등) 강력 제거 ===
   여러 Streamlit 버전/클래스명에 대응하도록 다양한 선택자 조합 사용
*/
[data-testid="stSelectbox"], 
[data-testid="stSelectbox"] > div,
.stSelectbox, .stSelectbox > div,
div[class*="stSelectbox"], 
div[class*="css-"][class*="select"], 
.css-1kyxreq.egzxvld0, .css-1kyxreq, .css-1f6l0j1, select {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
    margin: 0 !important;
}

/* 때에 따라 select 자체가 감싸진 label/div를 덮어야 하는 경우 */
div[role="listbox"], div[role="combobox"] {
    background: transparent !important;
    box-shadow: none !important;
}

/* 배당 입력 카드 */
.input-card {
    background-color:#161b22;
    border-radius:22px;
    padding:28px 34px;
    margin-bottom:30px;
    border:2px solid #2a2f3a;
    box-shadow:0 8px 24px rgba(0,0,0,0.55);
}

/* 입력 필드 */
input, .stNumberInput>div>div>input {
    background-color:#0e1117 !important;
    color:#ffffff !important;
    padding:0.7rem !important;
    font-size:1.02rem !important;
}

/* 분석 버튼 */
.stButton>button {
    background:linear-gradient(90deg,#ff9800,#ff5722);
    color:#0d47a1;
    font-weight:900 !important;
    padding:16px 36px;
    border-radius:20px;
    font-size:1.3rem;
    display:block;
    margin:24px auto;
    width:54%;
    min-width:220px;
    transition: transform 0.2s, box-shadow 0.2s;
    box-shadow:0 8px 22px rgba(0,0,0,0.45);
}
.stButton>button:hover { transform:scale(1.04); box-shadow:0 12px 30px rgba(0,0,0,0.6); }

/* 결과 카드 */
.card {
    background-color:#161b22;
    border-radius:20px;
    padding:26px;
    margin-top:22px;
    border:2px solid #2a2f3a;
    text-align:center;
    box-shadow:0 8px 24px rgba(0,0,0,0.55);
}
.result-text { font-size:2rem; font-weight:900; }
.super { color:#ff4d4d; }
.strong { color:#ff9800; }
.mid { color:#ffd54f; }
.pass { color:#9e9e9e; }

/* 광고 컨테이너 */
.ad-container {
    display:flex !important;
    flex-direction:row !important;
    justify-content:center;
    gap:28px;
    flex-wrap:wrap;
    margin-top:38px;
    margin-bottom:40px;
}

/* 광고 버튼 (프로) */
.ad-button {
    display:flex;
    justify-content:center;
    align-items:center;
    width:240px;
    height:98px;
    border-radius:22px;
    font-weight:900 !important;
    font-size:1.28rem !important;
    background-color:white;
    text-decoration:none;
    box-shadow:0 12px 28px rgba(0,0,0,0.55);
    transition: transform 0.22s, box-shadow 0.22s;
}
.ad-button:hover { transform:translateY(-4px) scale(1.05); box-shadow:0 16px 36px rgba(0,0,0,0.6); }
.ad-button.ad1 { color:#ff5722; }
.ad-button.ad2 { color:#4caf50; }
.ad-button.ad3 { color:#2196f3; }

/* 모바일 대응 */
@media (max-width:768px) {
    .ad-container { flex-direction:column !important; align-items:center; gap:18px; }
    .ad-button { width:86% !important; height:76px !important; font-size:1.15rem !important; }
    .stButton>button { width:82% !important; font-size:1.22rem !important; padding:15px 28px !important; }
    .input-card { padding:20px 22px !important; margin-bottom:24px !important; }
}

/* Streamlit 로고/Arch/툴바 숨김 */
header, footer, #MainMenu, [data-testid="stToolbar"], [data-testid="stDecoration"],
[data-testid="collapsedControl"], [data-testid="stVerticalBlock"] > div:first-child {
    display:none !important;
    visibility:hidden !important;
    height:0 !important;
    width:0 !important;
    overflow:hidden !important;
}
</style>
""", unsafe_allow_html=True)

# =========================
# 앱 UI
# =========================
st.title("⚽🏀🏒 전종목 배당 분석기")

sport = st.selectbox("종목 선택", ["축구", "농구", "하키"])

st.markdown('<div class="input-card">', unsafe_allow_html=True)
if sport in ["축구", "하키"]:
    home = st.number_input("홈 배당", min_value=1.01, step=0.01, format="%.2f")
    draw = st.number_input("무 배당", min_value=1.01, step=0.01, format="%.2f")
    away = st.number_input("원정 배당", min_value=1.01, step=0.01, format="%.2f")
else:
    home = st.number_input("홈 배당", min_value=1.01, step=0.01, format="%.2f")
    away = st.number_input("원정 배당", min_value=1.01, step=0.01, format="%.2f")
    draw = 0
st.markdown('</div>', unsafe_allow_html=True)

# 클릭 제한
if "last_click" not in st.session_state: st.session_state.last_click = datetime.min
def check_rate_limit():
    now = datetime.now()
    if now - st.session_state.last_click < timedelta(seconds=3):
        st.warning("3초에 한 번만 클릭 가능")
        st.stop()
    st.session_state.last_click = now

# 분석 로직
def analyze_odds(home, draw, away, sport="축구"):
    fav = min(home, away)
    fav_side = "홈" if home < away else "원정"
    gap = abs(home-away)
    if min(home,away)<1.60: return "PASS","pass"
    if sport in ["축구","하키"] and gap<0.25 and draw<3.4: return "PASS","pass"
    if fav<=1.85 and (draw>=3.6 or sport!="축구") and gap>=1.0: return f"초강승 ({fav_side} 승)","super"
    if fav<=2.05 and (draw>=3.4 or sport!="축구") and gap>=0.7: return f"강승 ({fav_side} 승)","strong"
    if fav<=2.40: return f"중승 ({fav_side} 승)","mid"
    return "PASS","pass"

# 분석 버튼 + 결과
if st.button("분석하기"):
    check_rate_limit()
    result_text, result_class = analyze_odds(home, draw, away, sport)
    st.markdown(f'<div class="card"><div class="result-text {result_class}">{result_text}</div></div>', unsafe_allow_html=True)

# 광고
ads = [
    {"id":"AD_001","label":"B WIN","url":"https://uzu59.netlify.app/","alert":False,"class":"ad1"},
    {"id":"AD_002","label":"BETZY","url":"https://b88-et.com","alert":True,"message":"⚠ 안내: 도메인명: 벳지 가입코드 : BANGU 담당자:@UZU59","class":"ad2"},
    {"id":"AD_003","label":"CAPS","url":"https://caps-22.com","alert":True,"message":"⚠ 안내: 도메인명: 캡스 가입코드 : RUST 담당자:@UZU59","class":"ad3"}
]

ad_html = '<div class="ad-container">'
for ad in ads:
    token = str(uuid.uuid4())
    ad_url = f"{ad['url']}?ad={ad['id']}&token={token}"
    if ad["alert"]:
        msg = ad["message"].replace("'","\\'")
        ad_html += f"""<a href="#" onclick="alert('{msg}'); window.open('{ad_url}','_blank'); return false;" class="ad-button {ad['class']}">{ad['label']}</a>"""
    else:
        ad_html += f"""<a href="{ad_url}" target="_blank" class="ad-button {ad['class']}">{ad['label']}</a>"""
ad_html += '</div>'

components.html(ad_html, height=260, scrolling=False)
