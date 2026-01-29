import streamlit as st

# =========================
# 🎨 GLOBAL STYLE + 로고/Arch 숨김 (모바일 포함)
# =========================
st.markdown("""
<style>
/* ===== 기본 스타일 ===== */
html, body, [class*="css"] {
    background-color: #0e1117;
    color: #e6e6e6;
}

/* 컨테이너 */
.block-container { padding: 2rem; }

/* 카드 */
.card {
    background-color: #161b22;
    border-radius: 14px;
    padding: 18px;
    margin-top: 16px;
    border: 1px solid #2a2f3a;
}

/* 등급 강조 */
.super { color: #ff4d4d; font-weight: 800; }
.strong { color: #ff9800; font-weight: 700; }
.mid { color: #ffd54f; font-weight: 600; }
.pass { color: #9e9e9e; font-weight: 600; }

/* 버튼 */
button { border-radius: 10px !important; font-weight: 700 !important; }

/* 입력 */
input { background-color: #0e1117 !important; color: #ffffff !important; }

/* 로그 */
.log { font-size: 0.85rem; color: #b0b0b0; margin-top: 6px; }

/* 모바일 */
@media (max-width: 768px) {
  .block-container { padding: 1rem; }
  h1 { font-size: 1.6rem; text-align: center; }
  input { font-size: 1rem; padding: 0.6rem; }
  button { width: 100%; font-size: 1.05rem; }
}

/* =========================
   Streamlit 로고 및 Arch/톱니바 숨기기
========================= */
footer, #MainMenu, [data-testid="stToolbar"], [data-testid="stDecoration"] {
    display: none !important;
}

/* 모바일 전용도 동일하게 숨김 */
@media (max-width: 768px) {
    footer, #MainMenu, [data-testid="stToolbar"], [data-testid="stDecoration"] {
        display: none !important;
    }
}
</style>
""", unsafe_allow_html=True)

# =========================
# 🧠 분석 로직
# =========================
def analyze_odds(home, draw, away):
    logs = []

    if min(home, away) < 1.60:
        logs.append("배당 1.60 미만 → 기준 미달")
        return "PASS", logs

    fav = min(home, away)
    fav_side = "홈" if home < away else "원정"
    gap = abs(home - away)

    if gap < 0.25 and draw < 3.4:
        logs.append("홈/원정 배당 차이 미미 + 무 배당 낮음 → 혼전")
        return "PASS", logs
    if fav <= 1.85 and draw >= 3.6 and gap >= 1.0:
        logs.append("저배당 안정 정배 + 무 방어 충분")
        return f"초강승 ({fav_side} 승)", logs
    if fav <= 2.05 and draw >= 3.4 and gap >= 0.7:
        logs.append("안정 정배 구조")
        return f"강승 ({fav_side} 승)", logs
    if fav <= 2.40:
        logs.append("중배당 구간 → 변동성 존재")
        return f"중승 ({fav_side} 승)", logs

    logs.append("구조 불명확")
    return "PASS", logs

# =========================
# UI
# =========================
st.title("⚽ 88 배당 분석기 ")
st.markdown("### 배당 입력")

home = st.number_input("홈 배당", min_value=1.01, step=0.01, format="%.2f")
draw = st.number_input("무 배당", min_value=1.01, step=0.01, format="%.2f")
away = st.number_input("원정 배당", min_value=1.01, step=0.01, format="%.2f")

# =========================
# 분석 버튼 + 카드
# =========================
if st.button("분석하기"):
    result, logs = analyze_odds(home, draw, away)

    st.markdown('<div class="card">', unsafe_allow_html=True)

    # 결과 표시
    if "초강승" in result:
        st.markdown(f"<div class='super'>🔥 {result}</div>", unsafe_allow_html=True)
    elif "강승" in result:
        st.markdown(f"<div class='strong'>⚡ {result}</div>", unsafe_allow_html=True)
    elif "중승" in result:
        st.markdown(f"<div class='mid'>⚠ {result}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='pass'>❌ PASS</div>", unsafe_allow_html=True)

    # 로그 접기(expander)
    with st.expander("분석 로그 보기"):
        for l in logs:
            st.markdown(f"• {l}")

    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# 하단 광고 버튼 1개 (SyntaxError 안전)
# =========================
ad_url = "https://uzu59.netlify.app/1"

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

