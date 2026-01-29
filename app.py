import streamlit as st

# ===============================
# 기본 설정
# ===============================
st.set_page_config(page_title="🔥 배당 전문 분석", layout="centered")

# ===============================
# CSS (다크모드 + 흰글씨 오류 해결)
# ===============================
st.markdown("""
<style>
body { background-color:#0f172a; color:#e5e7eb; }
input, select {
    background-color:#ffffff !important;
    color:#111827 !important;
}
label { color:#e5e7eb !important; }
.card {
    background:#020617;
    border:2px solid #334155;
    border-radius:14px;
    padding:16px;
    margin-top:16px;
}
.pass { color:#f87171; font-weight:bold; }
.mid { color:#facc15; font-weight:bold; }
.strong { color:#22c55e; font-weight:bold; }
.log { color:#94a3b8; font-size:14px; }
</style>
""", unsafe_allow_html=True)

st.title("🔥 배당 전문 분석")

# ===============================
# 입력 영역
# ===============================
with st.expander("📥 경기 정보 입력", expanded=True):
    sport = st.selectbox("종목 선택", ["축구", "농구", "하키"])

    home = st.text_input("홈팀", placeholder="홈팀")
    away = st.text_input("원정팀", placeholder="원정팀")

    odd_home = st.number_input("홈 배당", min_value=1.01, step=0.01)
    odd_draw = None
    if sport in ["축구", "하키"]:
        odd_draw = st.number_input("무 배당", min_value=1.01, step=0.01)
    odd_away = st.number_input("원정 배당", min_value=1.01, step=0.01)

# ===============================
# 분석 로직
# ===============================
def analyze_match(sport, home, away, oh, od, oa):
    logs = []

    # 공통 배당 필터
    if min(oh, oa) < 1.63:
        logs.append("배당 1.63 미만 경기 → PASS")
        return "PASS", None, logs

    diff = abs(oh - oa)

    # 종목별 PASS 기준
    if sport == "농구" and diff < 0.20:
        logs.append("농구 박빙 배당 → PASS")
        return "PASS", None, logs

    if sport in ["축구", "하키"] and diff < 0.25:
        logs.append("축구/하키 변동성 구간 → PASS")
        return "PASS", None, logs

    # 메인픽 선택
    if oh < oa:
        pick = f"{home} 승"
        base = oh
    else:
        pick = f"{away} 승"
        base = oa

    # 강승 / 중승 판정
    if diff >= 0.40 and 1.70 <= base <= 1.95:
        logs.append("배당 차이 충분 + 적정 배당")
        return "강승", pick, logs
    else:
        logs.append("조건 일부 부족 → 중승")
        return "중승", pick, logs

# ===============================
# 실행
# ===============================
if st.button("🔍 분석 실행"):
    grade, pick, logs = analyze_match(
        sport,
        home or "홈팀",
        away or "원정팀",
        odd_home,
        odd_draw,
        odd_away
    )

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    if grade == "PASS":
        st.markdown("<div class='pass'>❌ PASS</div>", unsafe_allow_html=True)
    else:
        color = "strong" if grade == "강승" else "mid"
        st.markdown(f"<div class='{color}'>✅ 메인픽: {pick}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='{color}'>🔥 등급: {grade}</div>", unsafe_allow_html=True)

    st.markdown("### 📋 분석 로그")
    for l in logs:
        st.markdown(f"<div class='log'>• {l}</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
