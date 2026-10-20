
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta

st.set_page_config(
    page_title="GlucoTwin AI",
    page_icon="🩺",
    layout="wide"
)

st.title("🩺 GlucoTwin AI")
st.subheader("Healthcare Digital Twin Prototype")

st.warning(
    "Educational demo only. All data are synthetic. "
    "Not intended for diagnosis or treatment."
)

with st.sidebar:
    st.header("Virtual Patient Controls")
    patient_id = st.text_input("Demo Patient ID", "DEMO-001")
    age = st.slider("Age", 18, 85, 42)
    baseline = st.slider("Baseline glucose (mg/dL)", 70, 160, 98)
    carbs = st.slider("Simulated carbohydrate intake (g)", 0, 120, 45, 5)
    activity = st.selectbox("Activity", ["Low", "Moderate", "High"])
    sleep = st.slider("Sleep (hours)", 2.0, 10.0, 7.0, 0.5)
    stress = st.selectbox("Stress", ["Low", "Moderate", "High"])

activity_effect = {"Low": 8, "Moderate": 0, "High": -8}[activity]
stress_effect = {"Low": -2, "Moderate": 3, "High": 8}[stress]
sleep_effect = (7 - sleep) * 1.2

rng = np.random.default_rng(21)
now = datetime.now()
times = [
    now - timedelta(minutes=15 * (23 - i))
    for i in range(24)
]

meal_effect = carbs * 0.35
starting_value = (
    baseline
    + meal_effect * 0.45
    + activity_effect * 0.25
    + stress_effect
    + sleep_effect
)

readings = []
for i in range(24):
    wave = 7 * np.sin(i / 3) + rng.normal(0, 4)
    meal_wave = meal_effect * np.exp(-((i - 18) / 3.5) ** 2) * 0.55
    value = starting_value + wave + meal_wave
    readings.append(round(max(60, value), 1))

history = pd.DataFrame({
    "Time": times,
    "Glucose (mg/dL)": readings
})

latest = float(history["Glucose (mg/dL)"].iloc[-1])

estimate = np.clip(
    latest
    + meal_effect * 0.35
    + stress_effect
    + sleep_effect
    + activity_effect * 0.35,
    60,
    300
)

if estimate >= 180:
    status = "Elevated demo alert"
elif estimate >= 140:
    status = "Moderate demo alert"
else:
    status = "Lower demo alert"

col1, col2, col3, col4 = st.columns(4)
col1.metric("Patient Twin", patient_id)
col2.metric("Age", age)
col3.metric("Latest Synthetic Glucose", f"{latest:.0f} mg/dL")
col4.metric("Illustrative Estimate", f"{estimate:.0f} mg/dL")

st.write("### Virtual Patient Status")
st.write(status)

st.caption(
    "The estimate is a simple illustrative heuristic, "
    "not a trained or clinically validated prediction model."
)

st.write("### Synthetic Glucose History")

chart = px.line(
    history,
    x="Time",
    y="Glucose (mg/dL)",
    markers=True,
    title="Simulated glucose readings"
)
chart.add_hline(
    y=180,
    line_dash="dash",
    annotation_text="Illustrative alert threshold"
)
st.plotly_chart(chart, use_container_width=True)

st.write("### Simulated Health Inputs")

st.dataframe(
    pd.DataFrame({
        "Input": [
            "Glucose history",
            "Carbohydrate intake",
            "Activity",
            "Sleep",
            "Stress"
        ],
        "Current demo value": [
            f"{latest:.1f} mg/dL",
            f"{carbs} g",
            activity,
            f"{sleep} hours",
            stress
        ]
    }),
    hide_index=True,
    use_container_width=True
)

st.download_button(
    "Download Synthetic Data CSV",
    data=history.to_csv(index=False).encode("utf-8"),
    file_name="glucotwin_history.csv",
    mime="text/csv"
)

st.info(
    "This is a demonstration using synthetic values. "
    "Real healthcare use would require suitable data, "
    "clinical validation, and privacy safeguards."
)
