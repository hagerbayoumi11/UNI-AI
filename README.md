<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0d0221,50:1a0533,100:0f3460&height=220&section=header&text=UNI-AI&fontSize=70&fontColor=00D4FF&animation=fadeIn&fontAlignY=38&desc=Student%20Risk%20Prediction%20Platform&descAlignY=58&descColor=7C3AED&descSize=22" />

<br/>

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![LightGBM](https://img.shields.io/badge/LightGBM-02569B?style=for-the-badge&logoColor=white)
![XGBoost](https://img.shields.io/badge/XGBoost-EA4335?style=for-the-badge&logoColor=white)
![SHAP](https://img.shields.io/badge/SHAP-Explainability-9333EA?style=for-the-badge)
![Optuna](https://img.shields.io/badge/Optuna-Tuning-00D4FF?style=for-the-badge)

<br/>

> **Predict. Explain. Intervene.**
> An end-to-end AI platform that identifies at-risk university students before it's too late.

</div>

---

## What is UNI-AI?

UNI-AI is a full-stack machine learning platform built on the **OULAD dataset** (32,593 students, 70+ features across 7 tables). It predicts student dropout risk in real time, explains *why* using SHAP, and recommends targeted interventions — all through a polished interactive dashboard.

---

## Live Demo

> Run locally:
```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## Platform Overview

### Dashboard
Real-time overview of all 32,593 students — pass rates, withdrawal rates, risk distribution, engagement heatmap, and AI-generated insights.

![Dashboard](screenshots/dashboard.png)

---

### Student Risk Prediction
Enter any student profile across 4 dimensions (Demographics, VLE Engagement, Assessment Performance, Registration Timing) and get an instant dropout probability with confidence score and personalized recommendations.

![Prediction](screenshots/prediction.png)

---

### Model Performance
Full comparison of 9 ML models + Optuna-tuned variants + Ensemble — visualized as bar charts, ROC curves, and radar plots.

![Model Performance](screenshots/model_perf.png)

---

### EDA & Insights
Exploratory analysis across all 7 OULAD tables — result distribution, pass rate by education level, gender breakdown, IMD band impact, VLE engagement patterns, and feature importance.

![EDA](screenshots/eda.png)

---

### SHAP Explainability
Global beeswarm plots, single-student waterfall charts, and dependence plots — showing exactly which features drive each prediction.

![SHAP](screenshots/shap.png)

---

## Model Results

| Rank | Model | AUC | F1 |
|------|-------|-----|----|
| 1 | **Ensemble (Top 3)** | **93.1%** | **88.8%** |
| 2 | LightGBM (Tuned) | 92.4% | 88.2% |
| 3 | XGBoost (Tuned) | 91.8% | 87.9% |
| 4 | Random Forest | 85.3% | 83.1% |
| 5 | Gradient Boosting | 88.7% | 85.4% |
| 6 | MLP Neural Net | 87.5% | 84.2% |

---

## Tech Stack

| Layer | Tools |
|-------|-------|
| Data Processing | Python, Pandas, NumPy |
| Feature Engineering | 70+ features across 7 OULAD tables |
| ML Models | LightGBM, XGBoost, Random Forest, SVM, KNN, MLP, Logistic Regression, Gradient Boosting, Decision Tree |
| Hyperparameter Tuning | Optuna |
| Explainability | SHAP (Beeswarm, Waterfall, Dependence) |
| Frontend | Streamlit multi-page app |
| Visualization | Plotly, Matplotlib, Seaborn |

---

## Dataset

**OULAD — Open University Learning Analytics Dataset**
- 32,593 students
- 70+ engineered features
- 7 relational tables
- Download: [analyse.kmi.open.ac.uk/open-dataset](https://analyse.kmi.open.ac.uk/open-dataset)

> Place CSV files in the root directory before running.

---

## Project Structure

```
UNI-AI/
├── app.py                  # Main Streamlit entry point
├── project.ipynb           # Full ML pipeline & experiments
└── pages_code/
    ├── dashboard.py        # Overview dashboard
    ├── predict.py          # Student risk prediction
    ├── model_perf.py       # Model leaderboard & comparison
    ├── eda.py              # Exploratory data analysis
    ├── shap_page.py        # SHAP explainability
    └── utils.py            # Shared utilities
```

---

## Author

**Hager Bayoumi** — Data Scientist & ML Engineer

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/hagar-mohamed-9bb768261)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/hagerbayoumi11)
[![Gmail](https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:hagerbayoumi11@gmail.com)

<div align="center">
<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0f3460,50:1a0533,100:0d0221&height=120&section=footer" />
</div>
