import streamlit as st

# ===============================
# PAGE
# ===============================
st.set_page_config(
    page_title="🔥 전종목 진심모드 FINAL",
    layout="centered"
)

# ===============================
# CSS – 완전 고정판
# ===============================
st.markdown("""
<style>
html, body, [class*="css"] {
    background-color: #0f172a !important;
    color: #e5e7eb !important;
}
input, select, textarea {
    background-color: #ffffff !important;
    color: #111827 !important;
    border-radius: 6px !important;
}
div[data-baseweb="select"] * {
    background-color: #ffffff !important;
    color: #111827 !important;
}
label {
    color: #e5e7eb !important;
    font-weight: 600;
}
.card {
    background-color: #020617;
    border: 2px solid #334155;
    border-radius: 14px;
    padding: 18px;
    margin-top: 18px;
}
.pass { color: #f87171; font-weight: 800; }
.mid { color: #facc15; font-weight: 800; }
.strong { color: #22c55e; font-weight: 800; }
.super { color: #38bdf8; font-weight: 900; }
.log {
    color: #94a3b8;
    font-size: 14px;
    margin-top: 4px;
}
</style>
""", unsafe_allow_html=True)

st.title("🔥 전종목 진심모드 FINAL")

# ===============================
# INPUT
# ===============================
with st.expander("📥 경기 정보 입력", expanded=True):
    sport = st.selectbox("종목", ["축구", "농구", "하키"])

    home = st.text_input("홈팀", placeholder="홈팀")
    away = st.text_input("원정팀", placeholder="원정팀")

    oh = st.number_input("홈 배당", min_value=1.01, step=0.01)
    od = None
    if sport != "농구":
        od = st.number_input("무 배당", min_value=1.01, step=0.01)
    oa = st.number_input("원정 배당", min_value=1.01, step=0.01)

# ===============================
# CORE LOGIC
# ===============================
def analyze(sport, oh, od, oa):
    logs = []

    # 1️⃣ 최소 배당 필터
    if min(oh, oa) < 1.70:
        logs.append("배당 1.70 미만 → 제외")
        return "PASS", None, logs

    diff = abs(oh - oa)

    # 2️⃣ 종목별 박빙 컷
    if sport == "농구" and diff < 0.20:
        logs.append("농구 박빙 배당 → PASS")
        return "PASS", None, logs
    if sport != "농구" and diff < 0.25:
        logs.append("축구/하키 혼전 구간 → PASS")
        return "PASS", None, logs

    # 3️⃣ 메인픽
    if oh < oa:
        pick = "홈팀 승"
        base = oh
        draw = od
    else:
        pick = "원정팀 승"
        base = oa
        draw = od

    # 4️⃣ 정배 과신 컷
    if sport != "농구" and draw is not None and draw <= 3.40:
        logs.append("무 배당 방어선 낮음 → 강승 불가")
        return "중승", pick, logs

    # 5️⃣ 초강승
    if (
        1.70 <= base <= 1.85 and
        diff >= 1.30 and
        (sport == "농구" or draw >= 3.60)
    ):
        logs.append("단폴급 구조 → 초강승")
        return "초강승", pick, logs

    # 6️⃣ 강승
    if (
        1.70 <= base <= 1.95 and
        diff >= 0.60 and
        (sport == "농구" or draw >= 3.30)
    ):
        logs.append("안정 정배 구조 → 강승")
        return "강승", pick, logs

    # 7️⃣ 중승
    logs.append("우세는 있으나 확신 부족")
    return "중승", pick, logs

# ===============================
# RUN
# ===============================
if st.button("🔍 분석 실행"):
    grade, pick, logs = analyze(sport, oh, od, oa)

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    if grade == "PASS":
        st.markdown("<div class='pass'>❌ PASS</div>", unsafe_allow_html=True)
    else:
        cls = {
            "초강승": "super",
            "강승": "strong",
            "중승": "mid"
        }[grade]

        st.markdown(f"<div class='{cls}'>✅ 메인픽: {pick}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='{cls}'>등급: {grade}</div>", unsafe_allow_html=True)

    st.markdown("### 📋 분석 로그")
    for l in logs:
        st.markdown(f"<div class='log'>• {l}</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
