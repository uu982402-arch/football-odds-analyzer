import streamlit as st
from datetime import datetime, timedelta
import uuid
import random
import streamlit.components.v1 as components

st.set_page_config(page_title=" 88 ", layout="centered")

st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background: #0e1117; }
html, body, .stApp {
    background-color:#0e1117 !important;
    color:#e6e6e6 !important;
    font-family: Arial, sans-serif;
}
.block-container { padding: 2.2rem 1.2rem; max-width: 980px; margin: 0 auto; }

[data-testid="stHeader"], header,
footer, #MainMenu,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="collapsedControl"] {
    display:none !important;
    height:0 !important;
}

/* 제목 */
.main-title {
    text-align:center;
    font-size:2.4rem;
    font-weight:900;
    margin: 0.2rem 0 0.6rem 0;
}

/* 종목 선택 카드 느낌 제거 */
[data-testid="stSelectbox"] > div {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}

/* ✅ 종목선택-홈배당 사이 남색 긴 바 제거 */
div[data-testid="stSelectbox"] + div:empty { display:none !important; }
div[data-testid="stSelectbox"] + div > div:empty { display:none !important; }
div[data-testid="stSelectbox"] + div:has(> div:empty) { display:none !important; }

/* 배당 입력 카드 */
.input-card {
    background:#161b22;
    border:1px solid #2a2f3a;
    border-radius:20px;
    padding: 22px 22px;
    margin-top: 14px;
    margin-bottom: 18px;
    box-shadow: 0 8px 22px rgba(0,0,0,0.45);
}

/* ✅ 분석 버튼 완전 중앙 */
div[data-testid="stButton"] {
  display:flex !important;
  justify-content:center !important;
}
.stButton > button {
    background: linear-gradient(90deg,#ff9800,#ff5722) !important;
    color: #111111 !important;
    font-weight: 900 !important;
    border-radius: 18px !important;
    padding: 15px 34px !important;
    font-size: 1.18rem !important;
    border: none !important;
    box-shadow: 0 10px 26px rgba(0,0,0,0.45) !important;
    width: min(420px, 80%) !important;
    margin: 18px auto 10px auto !important;
}
.stButton > button:hover { transform: scale(1.02); }

/* 결과 카드 */
.result-card {
    background:#161b22;
    border:1px solid #2a2f3a;
    border-radius:18px;
    padding: 22px;
    margin-top: 14px;
    text-align:center;
    box-shadow: 0 8px 22px rgba(0,0,0,0.45);
}
.result-text { font-size: 2rem; font-weight: 900; }
.super { color:#ff4d4d; }
.strong { color:#ff9800; }
.mid { color:#ffd54f; }
.pass { color:#9e9e9e; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🦋 88 🦋</div>', unsafe_allow_html=True)

sport = st.selectbox("종목 선택", ["축구", "농구", "하키"])

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

if "last_click" not in st.session_state:
    st.session_state.last_click = datetime.min

def check_rate_limit():
    now = datetime.now()
    if now - st.session_state.last_click < timedelta(seconds=3):
        st.warning("⏳ 3초에 한 번만 가능합니다")
        st.stop()
    st.session_state.last_click = now

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

if st.button("분석하기"):
    check_rate_limit()
    result_text, result_class = analyze_odds(home, draw, away, sport)
    st.markdown(
        f'<div class="result-card"><div class="result-text {result_class}">{result_text}</div></div>',
        unsafe_allow_html=True
    )

today_users = random.randint(72, 128)

ads = [
    {"id": "AD_001", "label": "B WIN", "color": "#ff5722", "url": "https://uzu59.netlify.app/", "need_modal": False,
     "message": ""},
    {"id": "AD_002", "label": "BETZY", "color": "#4caf50", "url": "https://b88-et.com", "need_modal": True,
     "message": "도메인: BETZY\\n가입코드: BANGU\\n담당자: @UZU59"},
    {"id": "AD_003", "label": "CAPS", "color": "#2196f3", "url": "https://caps-22.com", "need_modal": True,
     "message": "도메인: CAPS\\n가입코드: RUST\\n담당자: @UZU59"},
]

buttons_html = ""
for ad in ads:
    token = str(uuid.uuid4())
    ad_url = f"{ad['url']}?ad={ad['id']}&token={token}"
    if ad["need_modal"]:
        buttons_html += f"""
        <button class="ad-btn" style="border-color:{ad['color']};" 
            onclick="openModal('{ad_url}', `{ad['message']}`)">
            <span class="ad-name" style="color:{ad['color']};">{ad['label']}</span>
            <span class="ad-tip">공식 보증업체</span>
        </button>
        """
    else:
        buttons_html += f"""
        <a class="ad-link" href="{ad_url}" target="_blank" style="border-color:{ad['color']};">
            <span class="ad-name" style="color:{ad['color']};">{ad['label']}</span>
            <span class="ad-tip">공식 보증업체</span>
        </a>
        """

ads_html = f"""
<div class="ads-wrap">
  <div class="ads-divider">──────────────</div>
  <div class="ads-title">🦋 88 🦋 보증업체</div>
  <div class="ads-sub">✔ 고액 환전 OK · 실시간 검증 완료</div>
  <div class="ads-sub2">👥 오늘 방문자 <b>{today_users}명</b> 이용</div>
  <div class="ads-divider">──────────────</div>

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
  :root {{
    --card:#161b22; --border:#2a2f3a; --text:#e6e6e6;
  }}
  body {{ margin:0; padding:0; background:transparent; font-family: Arial, sans-serif; }}
  .ads-wrap {{ margin-top: 34px; text-align:center; }}
  .ads-divider {{ color:#7a7a7a; font-weight:700; margin: 8px 0; }}
  .ads-title {{ color:var(--text); font-weight:900; font-size: 1.55rem; margin-top: 10px; }}
  .ads-sub {{ color:#bdbdbd; font-weight:700; font-size: 0.95rem; margin-top:6px; }}
  .ads-sub2 {{ color:#a9a9a9; font-size: 0.9rem; margin-top: 6px; }}
  .ads-sub2 b {{ color:#ffd54f; }}

  .ads-row {{
    display:flex; gap:16px; justify-content:center; flex-wrap:wrap;
    margin-top: 18px; margin-bottom: 8px;
  }}

  .ad-btn, .ad-link {{
    width: 220px; height: 86px;
    border-radius: 18px;
    border: 2px solid #ffffff20;
    background: #ffffff;
    box-shadow: 0 10px 26px rgba(0,0,0,0.20);
    display:flex; flex-direction:column;
    align-items:center; justify-content:center;
    cursor:pointer;
    text-decoration:none;
    position: relative;
    transition: transform .18s ease, box-shadow .18s ease;
  }}
  .ad-btn:hover, .ad-link:hover {{
    transform: translateY(-3px) scale(1.03);
    box-shadow: 0 16px 34px rgba(0,0,0,0.26);
  }}
  .ad-name {{ font-weight: 900; font-size: 1.22rem; line-height: 1.1; }}
  .ad-tip {{ margin-top: 6px; font-size: 0.78rem; font-weight: 800; color:#000000a8; }}

  @media (max-width: 720px) {{
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
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 18px 18px 16px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.45);
    color: var(--text);
    text-align: left;
  }}
  .modal-title {{ font-size: 1.15rem; font-weight: 900; margin-bottom: 10px; }}
  .modal-text {{
    font-size: 0.95rem;
    color: #d6d6d6;
    line-height: 1.5;
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

components.html(ads_html, height=420, scrolling=False)
