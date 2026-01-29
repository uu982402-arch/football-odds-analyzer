import streamlit as st
from datetime import datetime, timedelta
import uuid

# =========================
# 🎨 프로페셔널 UI 스타일
# =========================
st.markdown("""
<style>
html, body, [class*="css"] {
    background-color:#0e1117; 
    color:#e6e6e6; 
    font-family:'Arial', sans-serif;
    margin:0;
    padding:0;
}
.block-container { padding:2.5rem; max-width:980px; margin:auto; }

/* 종목 선택 박스 배경/테두리 제거 */
.css-1kyxreq.egzxvld1 {
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
    margin: 0 !important;
}

/* 배당 입력 카드 */
.input-card {
    background-color:#161b22;
    border-radius:24px;
    padding:32px 40px;
    margin-bottom:40px;
    border:2px solid #2a2f3a;
    box-shadow:0 10px 28px rgba(0,0,0,0.55);
}

/* 입력 필드 */
input { 
    background-color:#0e1117 !important; 
    color:#ffffff !important; 
    padding:0.8rem; 
    font-size:1.05rem; 
}

/* 분석 버튼 */
.stButton>button {
    background:linear-gradient(90deg,#ff9800,#ff5722);
    color:#0d47a1;
    font-weight:900 !important;
    padding:18px 40px;
    border-radius:22px;
    font-size:1.35rem;
    display:block;
    margin:30px auto;
    width:55%;
    min-width:220px;
    box-shadow:0 8px 20px rgba(0,0,0,0.5);
    transition: transform 0.25s, box-shadow 0.25s;
}
.stButton>button:hover { transform:scale(1.06); box-shadow:0 12px 28px rgba(0,0,0,0.6); }

/* 결과 카드 */
.card {
    background-color:#161b22;
    border-radius:22px;
    padding:28px;
    margin-top:30px;
    border:2px solid #2a2f3a;
    text-align:center;
    box-shadow:0 10px 28px rgba(0,0,0,0.55);
}
.result-text { font-size:2.2rem; font-weight:900; }
.super { color:#ff4d4d; }
.strong { color:#ff9800; }
.mid { color:#ffd54f; }
.pass { color:#9e9e9e; }

/* 광고 컨테이너 */
.ad-container {
    display:flex !important;
    flex-direction:row !important;
    justify-content:center;
    gap:32px;
    flex-wrap:wrap;
    margin-top:50px;
    margin-bottom:50px;
}

/* 광고 버튼 */
.ad-button {
    display:flex;
    justify-content:center;
    align-items:center;
    width:240px;
    height:100px;
    border-radius:24px;
    font-weight:900 !important;
    font-size:1.35rem !important;
    background-color:white;
    text-decoration:none;
    box-shadow:0 12px 30px rgba(0,0,0,0.55);
    transition:transform 0.25s, box-shadow 0.25s;
}
.ad-button:hover { transform:translateY(-4px) scale(1.07); box-shadow:0 16px 36px rgba(0,0,0,0.6); }

/* 광고 글자색 */
.ad-button.ad1 { color:#ff5722; }
.ad-button.ad2 { color:#4caf50; }
.ad-button.ad3 { color:#2196f3; }

/* 모바일 대응 */
@media (max-width:768px) {
    .ad-container { flex-direction:column !important; align-items:center; gap:20px; }
    .ad-button { width:85%; height:80px; font-size:1.2rem !important; }
    .stButton>button { width:80%; font-size:1.25rem; padding:16px 30px; }
    .input-card { padding:25px 30px; margin-bottom:30px; }
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
# 종목 선택
# =========================
st.markdown("## ⚽🏀🏒 전종목 배당 분석기")
sport = st.selectbox("종목 선택", ["축구", "농구", "하키"])

# =========================
# 배당 입력 카드
# =========================
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
    gap = abs(home-away)
    if min(home,away)<1.60: return "PASS","pass"
    if sport in ["축구","하키"] and gap<0.25 and draw<3.4: return "PASS","pass"
    if fav<=1.85 and (draw>=3.6 or sport!="축구") and gap>=1.0: return f"초강승 ({fav_side} 승)","super"
    if fav<=2.05 and (draw>=3.4 or sport!="축구") and gap>=0.7: return f"강승 ({fav_side} 승)","strong"
    if fav<=2.40: return f"중승 ({fav_side} 승)","mid"
    return "PASS","pass"

# =========================
# 분석 버튼 + 결과 카드
# =========================
if st.button("분석하기"):
    check_rate_limit()
    result_text,result_class = analyze_odds(home, draw, away, sport)
    st.markdown(f'<div class="card"><div class="result-text {result_class}">{result_text}</div></div>', unsafe_allow_html=True)

# =========================
# 광고 버튼 3개
# =========================
ads = [
    {"id":"AD_001","label":"B WIN","url":"https://uzu59.netlify.app/","alert":False,"class":"ad1"},
    {"id":"AD_002","label":"BETZY","url":"https://b88-et.com","alert":True,"message":"⚠ 안내: 도메인명: 벳지 가입코드 : BANGU 담당자:@UZU59","class":"ad2"},
    {"id":"AD_003","label":"CAPS","url":"https://caps-22.com","alert":True,"message":"⚠ 안내: 도메인명: 캡스 가입코드 : RUST 담당자:@UZU59","class":"ad3"}
]

st.markdown('<div class="ad-container">', unsafe_allow_html=True)
for ad in ads:
    token = str(uuid.uuid4())
    ad_url = f"{ad['url']}?ad={ad['id']}&token={token}"
    if ad["alert"]:
        msg = ad["message"].replace("'","\\'")
        st.markdown(f"""
        <a href="#" onclick="alert('{msg}'); window.open('{ad_url}','_blank'); return false;"
           class="ad-button {ad['class']}">{ad['label']}</a>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <a href="{ad_url}" target="_blank" class="ad-button {ad['class']}">{ad['label']}</a>
        """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
