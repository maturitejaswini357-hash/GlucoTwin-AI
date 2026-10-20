

\# GlucoTwin AI — Architecture



\## Current Prototype



```mermaid

flowchart TD

&#x20;   A\["Virtual Patient Inputs"] --> C\["Synthetic Data Generation"]

&#x20;   B\["Lifestyle Inputs: Meals, Activity, Sleep, Stress"] --> C

&#x20;   C --> D\["Glucose Time-Series"]

&#x20;   D --> E\["Rule-Based Estimate"]

&#x20;   E --> F\["Status Indicator"]

&#x20;   D --> G\["Plotly Glucose Chart"]

&#x20;   F --> H\["Streamlit Dashboard"]

&#x20;   G --> H

&#x20;   D --> I\["Download CSV"]

&#x20;   

&#x20;   J\["Python + NumPy + Pandas"] --> C

&#x20;   K\["Streamlit + Plotly"] --> H

```



\## Future Enhancements



\- Integrate genuine wearable or sensor data.

\- Combine historical health records with time-series data.

\- Develop and evaluate a trained prediction model.

\- Add validation, privacy controls, and clinical review.



\*\*Safety:\*\* All current readings are synthetic. The estimate is heuristic-based and is not clinically validated.



