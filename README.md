\# GlucoTwin AI — Healthcare Digital Twin Prototype



\## Project Overview



GlucoTwin AI is an educational proof of concept for a patient-specific digital twin focused on exploring glucose trends and potential glucose elevation. It provides a dashboard that combines simulated patient information with synthetic time-series glucose readings and lifestyle inputs.



\## Problem Statement



Glucose-related health changes can be influenced by several factors, including meals, physical activity, sleep, and stress. A dashboard that brings these signals together can help demonstrate how a digital twin might represent a patient's changing health state.



\## Proposed Solution



The prototype provides:

\- A virtual patient profile with adjustable demographic and baseline glucose values.

\- Synthetic glucose time-series readings.

\- Simulated carbohydrate intake, physical activity, sleep, and stress inputs.

\- An illustrative estimate based on a transparent heuristic.

\- A chart of simulated glucose readings.

\- CSV export for further analysis.



\## Data Sources



\*\*Historical/static stream:\*\* User-configured demo age and baseline glucose.



\*\*Dynamic stream:\*\* Generated synthetic glucose readings and simulated lifestyle inputs.



All values are synthetic or user-configured demonstration values. No real patient records are included.



\## Technical Stack



\- Python

\- Streamlit

\- Pandas

\- NumPy

\- Plotly



\## Algorithm



The current version generates synthetic glucose readings and calculates an illustrative estimate using a rule-based heuristic based on selected inputs.



This is not a trained machine-learning model. No clinical validation or predictive accuracy claim is made.



\## Running the Project



1\. Install Python 3.13 or a compatible Python version.

2\. Open a terminal in the project directory.

3\. Install dependencies:



&#x20;  `python -m pip install streamlit pandas numpy plotly`



4\. Start the dashboard:



&#x20;  `python -m streamlit run app.py`



5\. Open the local URL shown in the terminal.



\## Privacy and Safety



This is an educational prototype, not a medical device. It must not be used for diagnosis, treatment, or medical decisions. The synthetic readings and illustrative estimate are not clinically validated.



\## Future Improvements



\- Add a structured synthetic historical health record with previous diagnoses and laboratory results.

\- Add a distinct wearable-data stream with timestamps and additional sensor features.

\- Train and evaluate a suitable model on an appropriate synthetic or open dataset.

\- Evaluate performance on held-out data and document limitations.

\- Add clinician-oriented explanations and privacy safeguards.



\## License



Released under the MIT License. See the LICENSE file.



\## Team and Institution



\- Team name: AI Alchemists

\- Team leader: Mahitha Katragadda

\- Team members:

&#x20; 1. Venkata Tejaswini Maturi — Vel Tech Rangarajan Dr. Sagunthala R\&D Institute of Science and Technology, Morai, Tamil Nadu

&#x20; 2.Sai Aamani Gunturi — Shanmugha Arts, Science, Technology \& Research Academy (SASTRA), Thanjavur

&#x20; 3.Mahitha Katragadda — Anil Neerukonda Institute of Technology and Sciences (ANITS), Visakhapatnam

\- Incubator: N/A

## Machine Learning Model

GlucoTwin AI includes a Random Forest classifier trained on synthetically generated health and lifestyle data. The prototype combines baseline health information with manually entered readings and lifestyle inputs to demonstrate a digital-twin workflow.

**Demo model evaluation on synthetic test data:**
- Accuracy: 97.3%
- ROC-AUC: 0.979
- Precision for the positive class: 0.42
- Recall for the positive class: 0.71
- F1-score for the positive class: 0.53

These results are from synthetic data and do not establish clinical accuracy or real-world health risk prediction. The current prototype does not connect to live wearable devices and is not intended for diagnosis or treatment.

### Current Limitations and Future Work
- Integrate real, appropriately consented health datasets.
- Connect supported wearable devices or sensor APIs for continuous readings.
- Validate predictions with appropriate clinical expertise and independent data.
- Improve event prediction and evaluate false alarms before considering real-world use.
- Add privacy, consent, and secure health-data handling mechanisms.
