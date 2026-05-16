import streamlit as st
import joblib
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="AQI Intelligence",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------- LOAD MODELS ----------------

model = joblib.load("models/aqi_model.pkl")
scaler = joblib.load("models/scaler.pkl")
encoder = joblib.load("models/encoder.pkl")

# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>

/* MAIN BACKGROUND */

.stApp {
    background: linear-gradient(to right, #0f172a, #111827);
    color: white;
}

/* REMOVE TOP SPACE */

.block-container {
    padding-top: 1rem;
    padding-bottom: 0rem;
    padding-left: 2rem;
    padding-right: 2rem;
}

/* TITLE */

.main-title {
    font-size: 42px;
    font-weight: bold;
    color: white;
}

.subtitle {
    color: #94a3b8;
    font-size: 18px;
}

/* CARDS */

.card {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 20px;
    border: 1px solid rgba(255,255,255,0.1);
    box-shadow: 0px 4px 20px rgba(0,0,0,0.3);
}

/* KPI */

.kpi-title {
    color: #94a3b8;
    font-size: 15px;
}

.kpi-value {
    color: white;
    font-size: 30px;
    font-weight: bold;
}

/* PREDICTION */

.prediction-box {
    padding: 25px;
    border-radius: 20px;
    text-align: center;
    font-size: 28px;
    font-weight: bold;
    margin-top: 20px;
}

/* BUTTON */

.stButton > button {
    width: 100%;
    height: 55px;
    border-radius: 14px;
    border: none;
    background: linear-gradient(to right, #2563eb, #7c3aed);
    color: white;
    font-size: 18px;
    font-weight: bold;
}

/* SLIDER */

.stSlider {
    padding-top: 10px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------

st.markdown("""
<div class="main-title">🌍 AQI Intelligence Dashboard</div>
<div class="subtitle">
AI-Powered Air Quality Monitoring & Prediction System
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------- KPI ROW ----------------

k1, k2, k3, k4 = st.columns(4)

cards = [
    ("CO AQI", "1"),
    ("OZONE", "30"),
    ("NO2", "2"),
    ("PM2.5", "50")
]

for col, card in zip([k1, k2, k3, k4], cards):

    with col:
        st.markdown(f"""
        <div class="card">
            <div class="kpi-title">{card[0]}</div>
            <div class="kpi-value">{card[1]}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------- MAIN SECTION ----------------

left, center, right = st.columns([1.1, 1.2, 1])

# ---------------- INPUT CARD ----------------

with left:

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("📥 Pollution Inputs")

    co = st.slider("CO AQI", 0, 150, 1)

    ozone = st.slider("Ozone AQI", 0, 250, 30)

    no2 = st.slider("NO2 AQI", 0, 100, 2)

    pm25 = st.slider("PM2.5 AQI", 0, 500, 50)

    predict_btn = st.button("🚀 Predict AQI")

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- GAUGE ----------------

with center:

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("📍 Live AQI Meter")

    gauge_value = min(pm25, 500)

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=gauge_value,
        number={'font': {'size': 45}},
        gauge={
            'axis': {'range': [0, 500]},
            'bar': {'color': "#ef4444"},
            'steps': [
                {'range': [0, 50], 'color': "#22c55e"},
                {'range': [50, 100], 'color': "#eab308"},
                {'range': [100, 200], 'color': "#f97316"},
                {'range': [200, 500], 'color': "#ef4444"},
            ],
        }
    ))

    fig.update_layout(
        template="plotly_dark",
        height=350,
        margin=dict(l=20, r=20, t=30, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- PREDICTION ----------------

with right:

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("🤖 AI Prediction")

    predicted_category = "Waiting..."

    if predict_btn:

        input_data = np.array([[co, ozone, no2, pm25]])

        input_scaled = scaler.transform(input_data)

        prediction = model.predict(input_scaled)

        predicted_category = encoder.inverse_transform(prediction)[0]

    # COLORS

    if predicted_category == "Good":
        color = "#22c55e"

    elif predicted_category == "Moderate":
        color = "#eab308"

    elif predicted_category == "Unhealthy":
        color = "#ef4444"

    else:
        color = "#f97316"

    st.markdown(f"""
    <div class="prediction-box"
    style="background:{color};">
        {predicted_category}
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.metric("Predicted AQI", predicted_category)

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- CHARTS ----------------

st.markdown("<br>", unsafe_allow_html=True)

chart1, chart2 = st.columns(2)

data = pd.DataFrame({
    "Pollutant": ["CO", "Ozone", "NO2", "PM2.5"],
    "Value": [co, ozone, no2, pm25]
})

# ---------------- BAR CHART ----------------

with chart1:

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("📊 Pollution Levels")

    fig1 = px.bar(
        data,
        x="Pollutant",
        y="Value",
        template="plotly_dark",
        text_auto=True
    )

    fig1.update_layout(
        height=320,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(fig1, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- DONUT CHART ----------------

with chart2:

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("🧪 Pollutant Contribution")

    fig2 = px.pie(
        data,
        names="Pollutant",
        values="Value",
        hole=0.6,
        template="plotly_dark"
    )

    fig2.update_layout(
        height=320,
        paper_bgcolor="rgba(0,0,0,0)",
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- FOOTER ----------------

st.markdown("<br>", unsafe_allow_html=True)

st.caption("🚀 AQI Intelligence System | Streamlit + ML + Plotly")