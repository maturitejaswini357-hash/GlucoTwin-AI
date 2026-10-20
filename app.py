
from pathlib import Path
from datetime import datetime, timedelta

import joblib
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="GlucoTwin AI",
    page_icon="🩺",
    layout="wide",
)

MODEL_PATH = Path("model_outputs/glucotwin_model.joblib")

st.title("🩺 GlucoTwin AI")
st.subheader("Healthcare Digital Twin — Experimental Prototype")

st.warning(
    "Research demonstration only. The model uses synthetic training data "
    "and synthetic event labels. Its probability is NOT a real patient's "
    "medical risk and must not guide diagnosis or treatment."
)

if not MODEL_PATH.exists():
    st.error("Model file not found. Run `python train_model.py` first.")
    st.stop()

saved = joblib.load(MODEL_PATH)
model = saved["model"]
features = saved["features"]

with st.sidebar:
    st.header("Virtual Patient")

    patient_id = st.text_input("Demo Patient ID", "DEMO-001")
    age = st.slider("Age", 18, 85, 42)
    baseline = st.slider("Baseline glucose (mg/dL)", 65, 180, 105)
    hba1c = st.slider("HbA1c (%) — synthetic input", 4.0, 10.5, 5.8, 0.1)
    previous_diabetes = st.selectbox(
        "Previous diabetes diagnosis (demo)",
        ["No", "Yes"],
    )

    st.header("Dynamic Sensor / Lifestyle Inputs")
    current_glucose = st.slider(
        "Current glucose (mg/dL)", 55, 280, 125
    )
    carbs = st.slider("Carbohydrate intake (g)", 0, 150, 45, 5)
    steps = st.slider("Steps in the last hour", 0, 1800, 500, 50)
    heart_rate = st.slider("Heart rate (bpm)", 45, 140, 76)
    hrv = st.slider("Heart-rate variability (ms)", 8, 100, 42)
    sleep = st.slider("Sleep (hours)", 2.0, 10.0, 7.0, 0.5)
    stress = st.slider("Stress score (1–10)", 1, 10, 4)

activity = (
    "High" if steps >= 1000
    else "Moderate" if steps >= 400
    else "Low"
)

inputs = {
    "age": age,
    "baseline_glucose": baseline,
    "hba1c": hba1c,
    "previous_diabetes": int(previous_diabetes == "Yes"),
    "carbs_g": carbs,
    "steps_last_hour": steps,
    "sleep_hours": sleep,
    "stress_score": stress,
    "current_glucose": current_glucose,
    "heart_rate": heart_rate,
    "hrv_ms": hrv,
}

input_df = pd.DataFrame([inputs], columns=features)

probability = float(model.predict_proba(input_df)[0][1])
predicted_event = int(model.predict(input_df)[0])

col1, col2, col3 = st.columns(3)
col1.metric("Virtual Patient", patient_id)
col2.metric("Current Demo Glucose", f"{current_glucose} mg/dL")
col3.metric(
    "Model Output",
    "Synthetic event flagged" if predicted_event else "Synthetic event not flagged",
)

st.markdown("### Experimental Model Output")
st.progress(probability)
st.write(f"Model probability for the **synthetic event label**: {probability:.1%}")

st.caption(
    "This is a model output on user-entered demonstration inputs, "
    "not a validated medical risk estimate. It does not predict a "
    "clinically established outcome."
)

st.markdown("### Synthetic Glucose Trend")

rng = np.random.default_rng(21)
now = datetime.now()
times = [
    now - timedelta(minutes=15 * (23 - i))
    for i in range(24)
]

readings = []
for i in range(24):
    wave = 7 * np.sin(i / 3) + rng.normal(0, 4)
    meal_wave = carbs * 0.12 * np.exp(-((i - 18) / 3.5) ** 2)
    value = current_glucose + wave + meal_wave
    readings.append(round(float(np.clip(value, 50, 300)), 1))

history = pd.DataFrame({
    "Time": times,
    "Synthetic glucose (mg/dL)": readings,
})

fig = px.line(
    history,
    x="Time",
    y="Synthetic glucose (mg/dL)",
    markers=True,
    title="Illustrative synthetic time series",
)
st.plotly_chart(fig, width="stretch")

st.markdown("### Inputs Supplied to the Model")
st.dataframe(
    pd.DataFrame({
        "Feature": list(inputs.keys()),
        "Value": list(inputs.values()),
    }),
    hide_index=True,
    width="stretch",
)

st.download_button(
    "Download synthetic glucose CSV",
    data=history.to_csv(index=False).encode("utf-8"),
    file_name="glucotwin_synthetic_history.csv",
    mime="text/csv",
)

st.info(
    "The current prototype combines historical-style demo inputs with "
    "simulated dynamic readings. It does not connect to a real wearable, "
    "medical record, or live sensor. Clinical use would require real, "
    "appropriately governed data and independent validation."
)
