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

<br/>

![Best Model](https://img.shields.io/badge/Best%20Model-XGBoost%20Tuned-EA4335?style=flat-square)
![AUC](https://img.shields.io/badge/ROC--AUC-97.92%25-00D4FF?style=flat-square)
![F1](https://img.shields.io/badge/F1%20Weighted-92.01%25-7C3AED?style=flat-square)
![Accuracy](https://img.shields.io/badge/Accuracy-92.01%25-0F3460?style=flat-square)
![Students](https://img.shields.io/badge/Students-32%2C593-1a0533?style=flat-square)
![Models](https://img.shields.io/badge/Models%20Trained-9%20%2B%20Tuning%20%2B%20Ensemble-00D4FF?style=flat-square)

</div>

---

## What is UNI-AI?

UNI-AI is a full-stack machine learning platform built on the **OULAD dataset** (32,593 students, 28 engineered features across 7 tables). It trains and compares **9 classifiers**, tunes the top models with **Optuna**, builds a **soft-voting Ensemble**, and explains every prediction using **SHAP** — all wrapped in a polished interactive Streamlit dashboard.

---

## Run Locally

```bash
git clone https://github.com/hagerbayoumi11/UNI-AI.git
cd UNI-AI
pip install -r requirements.txt
streamlit run app.py
```

> Download OULAD CSV files from [analyse.kmi.open.ac.uk/open-dataset](https://analyse.kmi.open.ac.uk/open-dataset) and place them in the root directory.

---

## Platform Overview

### Dashboard
Real-time overview of all 32,593 students — pass rates, withdrawal rates, risk distribution, engagement heatmap, top at-risk students, model leaderboard, and AI-generated insights.

![Dashboard](dashboard.png)

---

### Student Risk Prediction
Enter any student profile across 4 dimensions (Demographics, VLE Engagement, Assessment Performance, Registration Timing) and get an instant dropout probability with SHAP feature contributions and personalized recommendations.

![Prediction](prediction.png)

---

### Model Performance
Full comparison of 9 classifiers + Optuna-tuned variants + Soft-voting Ensemble — visualized as bar charts, ROC curves, and radar plots.

![Model Performance](model_perf.png)

---

### EDA & Insights
Exploratory analysis across all 7 OULAD tables — result distribution, pass rate by education level, gender breakdown, IMD band impact, VLE engagement patterns, and feature importance.

![EDA](eda.png)

---

### SHAP Explainability
Global beeswarm plots, single-student waterfall charts, and dependence plots — showing exactly which features drive each prediction.

![SHAP](shap.png)

---

## Model Results

| Rank | Model | Accuracy | F1 Weighted | ROC-AUC | CV F1 |
|------|-------|----------|-------------|---------|-------|
| 1 | **XGBoost (Tuned)** | **92.01%** | **92.01%** | **97.92%** | **92.16%** |
| 2 | LightGBM (Tuned) | 91.61% | 91.61% | 97.87% | 91.80% |
| 3 | Ensemble (Top 3) | — | 88.80% | 93.10% | — |
| 4 | Gradient Boosting | 91.41% | 91.41% | 97.78% | 91.59% |
| 5 | XGBoost | 91.09% | 91.09% | 97.73% | 91.28% |
| 6 | Random Forest | 91.00% | 91.00% | 97.53% | 91.15% |
| 7 | SVM | 90.98% | 90.99% | 96.84% | 91.04% |
| 8 | Decision Tree | 90.96% | 90.97% | 97.02% | 91.33% |
| 9 | LightGBM | 90.75% | 90.76% | 97.64% | 90.91% |
| 10 | KNN | 89.88% | 89.88% | 96.21% | 89.49% |
| 11 | Logistic Regression | 89.78% | 89.79% | 95.89% | 89.90% |
| 12 | MLP Neural Net | 88.56% | 88.56% | 96.45% | 89.24% |

> Tuning: Optuna TPE — 25 trials LightGBM + 25 trials XGBoost

---

## Tech Stack

| Layer | Tools |
|-------|-------|
| Data Processing | Python, Pandas, NumPy |
| Feature Engineering | 28 features across 7 OULAD tables |
| ML Models | XGBoost, LightGBM, Random Forest, Gradient Boosting, SVM, KNN, MLP Neural Net, Logistic Regression, Decision Tree |
| Hyperparameter Tuning | Optuna TPE (50 trials) |
| Ensemble | Soft-voting Top-3 + optimal threshold |
| Explainability | SHAP (Beeswarm, Waterfall, Dependence) |
| Frontend | Streamlit multi-page app |
| Visualization | Plotly, Matplotlib, Seaborn |

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

## Dataset

**OULAD — Open University Learning Analytics Dataset**
- 32,593 students | 28 engineered features | 7 relational tables
- Download: [analyse.kmi.open.ac.uk/open-dataset](https://analyse.kmi.open.ac.uk/open-dataset)

---

## Author

**Hager Bayoumi** — Data Scientist & ML Engineer

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/hagar-mohamed-9bb768261)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/hagerbayoumi11)
[![Gmail](https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:hagerbayoumi11@gmail.com)

<div align="center">
<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0f3460,50:1a0533,100:0d0221&height=120&section=footer" />
</div>
