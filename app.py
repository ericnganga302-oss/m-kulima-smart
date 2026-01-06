# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="M-Kulima Smart",
    page_icon="🌱",
    layout="wide",
)

# -----------------------------
# GLOBAL STYLES (Dark + Farm)
# -----------------------------
st.markdown("""
<style>
body {
    background-color: #0e1117;
}
.metric-card {
    background-color: #161b22;
    padding: 20px;
    border-radius: 16px;
    box-shadow: 0 0 8px rgba(0,255,150,0.15);
}
.metric-title {
    color: #9be7c4;
    font-size: 14px;
}
.metric-value {
    font-size: 28px;
    font-weight: bold;
    color: #e6fff4;
}
.badge-green {color:#00ff9c;}
.badge-yellow {color:#ffd166;}
.badge-red {color:#ff4d4d;}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# MOCK SAFE DATA (Step 2 will replace)
# -----------------------------
def load_weights():
    return pd.DataFrame({
        "date": pd.date_range(end=date.today(), periods=10),
        "weight": [220, 222, 225, 227, 229, 228, 230, 231, 233, 235]
    })

def load_health():
    return {
        "status": "Healthy",
        "temperature": 38.4,
        "activity": "Normal"
    }

# -----------------------------
# SIDEBAR NAVIGATION
# -----------------------------
st.sidebar.title("🌱 M-Kulima Smart")
st.sidebar.caption("Smart Livestock Monitoring")

NAV_PAGES = {
    "📊 Dashboard": "dashboard",
    "🐄 Animal Health": "health",
    "⚖️ Weight Tracking": "weight",
    "📥 Data Ingestion": "ingest",
    "⚙️ Admin": "admin"
}

selection = st.sidebar.radio("Navigate", list(NAV_PAGES.keys()))

# -----------------------------
# DASHBOARD PAGE
# -----------------------------
def page_dashboard():
    st.title("📊 Farm Overview")

    health = load_health()
    weights = load_weights()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Health Status</div>
            <div class="metric-value badge-green">🟢 {health['status']}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Temperature</div>
            <div class="metric-value">{health['temperature']} °C</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Latest Weight</div>
            <div class="metric-value">{weights['weight'].iloc[-1]} kg</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### 📈 Weight Trend")
    fig = px.line(weights, x="date", y="weight", markers=True)
    fig.update_layout(
        template="plotly_dark",
        height=350
    )
    st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# HEALTH PAGE
# -----------------------------
def page_health():
    st.title("🐄 Animal Health Monitor")

    health = load_health()

    if health["status"] == "Healthy":
        st.success("🟢 Animal is healthy")
    else:
        st.warning("🟡 Attention required")

    st.metric("Temperature", f"{health['temperature']} °C")
    st.metric("Activity", health["activity"])

# -----------------------------
# WEIGHT PAGE
# -----------------------------
def page_weight():
    st.title("⚖️ Weight Monitoring")

    weights = load_weights()
    st.dataframe(weights, use_container_width=True)

# -----------------------------
# INGEST PAGE
# -----------------------------
def page_ingest():
    st.title("📥 Data Ingestion")
    st.info("CSV upload & auto-processing (Step 2 upgrade)")

    file = st.file_uploader("Upload CSV", type=["csv"])
    if file:
        df = pd.read_csv(file)
        st.success("Data loaded successfully")
        st.dataframe(df)

# -----------------------------
# ADMIN PAGE
# -----------------------------
def page_admin():
    st.title("⚙️ Admin Panel")
    st.warning("Admin features locked (Step 3: Authentication)")

    if st.button("Retrain Model"):
        st.success("Model retraining triggered (placeholder)")

# -----------------------------
# ROUTER (NO BUGS)
# -----------------------------
ROUTES = {
    "dashboard": page_dashboard,
    "health": page_health,
    "weight": page_weight,
    "ingest": page_ingest,
    "admin": page_admin
}

ROUTES[NAV_PAGES[selection]]()
