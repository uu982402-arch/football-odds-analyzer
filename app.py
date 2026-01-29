import streamlit as st
from datetime import datetime, timedelta
import uuid
import streamlit.components.v1 as components

# =========================
# 🎨 GLOBAL PRO UI STYLE
# =========================
st.set_page_config(layout="centered")

st.markdown("""
<style>
html, body {
    background-color:#0e1117;
    color:#e6e6e6;
    font-family:'Arial', sans-serif;
}
.block-container { padding:2.2rem; }

/* ---------- TITLE ---------- */
.main-title {
    text-align:center;
    font-size:2.4rem;
    font-weight:900;
    margin-bottom:10px;
}

/* ---------- INPUT CARD ---------- */
.input-card {
    background:#161b22;
    border-radius:20px;
    padding:26px;
    margin-top:15px;
    margin-bottom:25px;
    border:1px solid #2a2f3a;
}

/* ---------- BUTTON ---------- */
.stButton>button {
    background:linear-gradient(90deg,#ff9800,#ff5722);
    color:#0d47a1;
    font-weight:900;
    font-size:1.25rem;
    padding:15px 36px;
    border-radius:18px;
    display:block;
    margin:22px auto;
    width:55%;
    min-width:220px;
}
.stButton>button:hover { transform:scale(1.05); }

/* ---------- RESULT CARD ---------- */
.card {
    background:#161b22;
    border-radius:16px;
    padding:24px;
    margin-top:18px;
    text-align:center;
    border:1px solid #2a2f3a;
}
.result-text { font-size:2rem; font-weight:900; }
.super { color:#ff4d4d; }
.strong { color:#ff9800; }
.mid { color:#ffd54f; }
.pass { color:#9e9e9e; }

/* ---------- AD SECTION ---------- */
.ad-divider {
    margin:40px 0 12px;
    text-align:center;
    color:#bdbdbd;
    font-weight:700;
}
.ad-title {
    font-size:1.6rem;
    font-weight:900;
}
.ad-sub {
    font-size:0.9rem;
    color:#9e9e9e;
    margin-top:4px;
}

.ad-container {
    display:flex;
    justify-content:center;
    gap:22px;
    flex-wrap:wrap;
    margin-top:20px;
}

.ad-button {
    width:210px;
    height:82px;
    border-radius:18px;
    background:#ffffff;
    display:flex;
    align-items:center;
    justify-content:center;
    font-weight:900;
    font-size:1.2rem;
    text-decoration:none;
    box-shadow:0 8px 18px rgba(0,0,0,0.45);
    cursor:pointer;
}
.ad1 { color:#ff5722; }
.ad2 { color:#4caf50; }
.ad3 { color:#2196f3; }

/* ---------- MODAL ---------- */
.modal-bg {
    position:fixed;
    top:0; left:0;
    width:100%; height:100%;
    background:rgba(0,0,0,0.65);
    display:none;
    justify-content:center;
    align-items:center;
    z-index:9999;
}
.modal {
    background:#161b22;
    padding:26px;
    border-radius:18px;
    width:90%;
    max-width:360px;
    text-align:center;
    border:1px solid #2a2f3a;
}
.modal h3 { margin-bottom:10px; }
.modal p { font-size:0.95rem; color:#ccc; }
.modal-btn {
    margin-top:16px;
    background:#ff9800;
    color:#000;
    padding:10px 20px;
    border-radius:14px;
    font-weight:900;
    cursor:pointer;
}

/* ---------- MOBILE ---------- */
@media (max-width:768px){
    .ad-container { flex-direction:column; }
    .stButton>button { width:80%; }
}

/* ---------- STREAMLIT HIDE ---------- */
header, footer, #MainMenu { display:none !important; }
</style>
""", unsafe_allow_html=True)

# =========================
# 🪽 TITLE
# =========================
st.markdown('<div class="main-title">🪽 88 🪽</div>', unsafe_allow_html=True)

# =========================
# SPORT SELECT (NO CARD)
# =========================
sport = st.selectbox("종목 선택", ["축구", "농구", "하키"])

# =========================
# INPUT CARD
# =========================
st.markdown('<div class="input-card">', unsafe_allow_html=True)

if sport in ["축구", "하키"]:
    home = st.number_input("홈 배당", 1.01, step=0.01, format="%.2f")
    draw = st.number_input("무 배당", 1.01, step=0.01, format="%.2f")
    away = st.number_input("원정 배당", 1.01, step=0.01, format="%.2f")
else:
    home = st.number_input("홈 배당", 1.01, step=0.01, format="%.2f")
    away = st.number_input("원정 배당", 1.01, step=0.01, format="%.2f")
    draw = 0

st.markdown('</div>', unsafe_allow_html=True)

# =========================
# RATE LIMIT
# =========================
if "last_click" not in st.session_state:
    st.session_state.last_click = datetime.min

def check_limit():
    if datetime.now() - st.session_state.last_click < timedelta(seconds=3):
        st.warning("⏳ 잠시만 기다려 주세요")
        st.stop()
    st.session_state.last_click = datetime.now()

# =========================
# ANALYSIS
# =========================
def analyze(home, draw, away, sport):
    fav = min(home, away)
    gap = abs(home-away)
    if fav < 1.6: return "PASS","pass"
    if sport in ["축구","하키"] and gap < 0.25 and draw < 3.4: return "PASS","pass"
    if fav <= 1.85 and gap >= 1.0: return "초강승","super"
    if fav <= 2.05 and gap >= 0.7: return "강승","strong"
    if fav <= 2.4: return "중승","mid"
    return "PASS","pass"

if st.button("분석하기"):
    check_limit()
    text, cls = analyze(home, draw, away, sport)
    st.markdown(f'<div class="card"><div class="result-text {cls}">{text}</div></div>', unsafe_allow_html=True)

# =========================
# AD SECTION
# =========================
st.markdown("""
<div class="ad-divider">
──────────────<br>
<span class="ad-title">🪽 88 🪽 보증업체</span><br>
<span class="ad-sub">✔ 고액 환전 OK · 실시간 검증 완료</span><br>
──────────────
</div>
""", unsafe_allow_html=True)

ads = [
    ("B WIN","https://uzu59.netlify.app/","ad1","도메인: BWIN<br>담당자: @UZU59"),
    ("BETZY","https://b88-et.com","ad2","도메인: BETZY<br>가입코드: BANGU"),
    ("CAPS","https://caps-22.com","ad3","도메인: CAPS<br>가입코드: RUST"),
]

html = '<div class="ad-container">'
for name,url,cls,msg in ads:
    token = uuid.uuid4()
    html += f"""
    <div class="ad-button {cls}" onclick="openModal('{url}?t={token}','{msg}')">{name}</div>
    """
html += '</div>'

html += """
<div class="modal-bg" id="modal">
  <div class="modal">
    <h3>⚠ 공식 보증업체 안내</h3>
    <p id="modal-text"></p>
    <div class="modal-btn" onclick="go()">확인 후 이동</div>
  </div>
</div>

<script>
let target='';
function openModal(url,text){
  target=url;
  document.getElementById("modal-text").innerHTML=text;
  document.getElementById("modal").style.display="flex";
}
function go(){
  window.open(target,'_blank');
  document.getElementById("modal").style.display="none";
}
</script>
"""

components.html(html, height=420)
