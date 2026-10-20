
from pathlib import Path
import json

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer

OUT = Path("model_outputs")
OUT.mkdir(exist_ok=True)

# Reproducible SYNTHETIC data only.
# These rules define a demo label, not a medical definition.
rng = np.random.default_rng(42)
n = 5000

age = rng.integers(18, 86, n)
baseline_glucose = rng.normal(105, 18, n).clip(65, 180)
hba1c = rng.normal(5.8, 0.9, n).clip(4.0, 10.5)
previous_diabetes = rng.binomial(1, 0.22, n)
carbs_g = rng.gamma(2.2, 22, n).clip(0, 150)
steps_last_hour = rng.integers(0, 1800, n)
sleep_hours = rng.normal(6.8, 1.3, n).clip(2, 10)
stress_score = rng.integers(1, 11, n)

# Dynamic sensor-like readings at the current time.
current_glucose = (
    baseline_glucose
    + 0.18 * carbs_g
    - 0.012 * steps_last_hour
    + rng.normal(0, 12, n)
).clip(55, 280)

heart_rate = rng.normal(76, 12, n).clip(45, 140)
hrv_ms = rng.normal(42, 14, n).clip(8, 100)

data = pd.DataFrame({
    "age": age,
    "baseline_glucose": baseline_glucose,
    "hba1c": hba1c,
    "previous_diabetes": previous_diabetes,
    "carbs_g": carbs_g,
    "steps_last_hour": steps_last_hour,
    "sleep_hours": sleep_hours,
    "stress_score": stress_score,
    "current_glucose": current_glucose,
    "heart_rate": heart_rate,
    "hrv_ms": hrv_ms,
})

# Synthetic future value used only to create a demo target.
future_glucose = (
    current_glucose
    + 0.25 * carbs_g
    - 0.015 * steps_last_hour
    + 1.5 * stress_score
    + 1.5 * (7 - sleep_hours)
    + rng.normal(0, 15, n)
).clip(50, 350)

# Demo event: future synthetic glucose >= 180 mg/dL.
# This threshold is an illustrative label for this simulation,
# not a clinical prediction rule or medical advice.
data["synthetic_spike_event"] = (future_glucose >= 180).astype(int)

features = [
    "age",
    "baseline_glucose",
    "hba1c",
    "previous_diabetes",
    "carbs_g",
    "steps_last_hour",
    "sleep_hours",
    "stress_score",
    "current_glucose",
    "heart_rate",
    "hrv_ms",
]
X = data[features]
y = data["synthetic_spike_event"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

model = make_pipeline(
    SimpleImputer(strategy="median"),
    RandomForestClassifier(
        n_estimators=200,
        max_depth=10,
        class_weight="balanced",
        random_state=42,
    ),
)
model.fit(X_train, y_train)

pred = model.predict(X_test)
proba = model.predict_proba(X_test)[:, 1]

metrics = {
    "dataset": "synthetic demonstration data",
    "samples_total": int(len(data)),
    "samples_train": int(len(X_train)),
    "samples_test": int(len(X_test)),
    "positive_event_rate": float(y.mean()),
    "accuracy": float(accuracy_score(y_test, pred)),
    "roc_auc": float(roc_auc_score(y_test, proba)),
    "confusion_matrix_tn_fp_fn_tp": confusion_matrix(
        y_test, pred, labels=[0, 1]
    ).ravel().tolist(),
    "classification_report": classification_report(
        y_test, pred, output_dict=True, zero_division=0
    ),
    "warning": (
        "Synthetic data and synthetic labels only. "
        "Metrics do not indicate clinical performance."
    ),
}

joblib.dump({"model": model, "features": features}, OUT / "glucotwin_model.joblib")
data.to_csv(OUT / "synthetic_training_data.csv", index=False)
(OUT / "evaluation.json").write_text(json.dumps(metrics, indent=2))
(OUT / "classification_report.txt").write_text(
    classification_report(y_test, pred, zero_division=0)
)

print("\nMODEL TRAINING COMPLETE")
print("Training rows:", len(X_train))
print("Test rows:", len(X_test))
print("Synthetic event rate:", round(y.mean(), 3))
print("Accuracy:", round(metrics["accuracy"], 3))
print("ROC-AUC:", round(metrics["roc_auc"], 3))
print("\nConfusion matrix [TN, FP, FN, TP]:")
print(metrics["confusion_matrix_tn_fp_fn_tp"])
print("\n", classification_report(y_test, pred, zero_division=0))
print("\nFiles saved in:", OUT.resolve())
print("Reminder: these are synthetic demonstration metrics, not clinical evidence.")
