import streamlit as st

st.set_page_config(
    page_title="UNI·AI — OULAD Platform",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }
.stApp { background: #080B14 !important; }
header[data-testid="stHeader"] { background: transparent !important; }
section[data-testid="stSidebar"] {
    background: #0D1117 !important;
    border-right: 1px solid rgba(255,255,255,0.06) !important;
}
.block-container { padding: 1.5rem 2rem 3rem !important; max-width: 1400px !important; }

/* Metrics */
[data-testid="metric-container"] {
    background: #111827 !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    border-radius: 12px !important;
    padding: 1rem 1.2rem !important;
}
[data-testid="metric-container"] label {
    color: #6B7280 !important; font-size: 11px !important;
    font-weight: 600 !important; text-transform: uppercase !important;
    letter-spacing: .06em !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #E8EAF0 !important; font-size: 24px !important; font-weight: 700 !important;
}

/* Buttons */
.stButton > button {
    background: #4361EE !important; color: white !important;
    border: none !important; border-radius: 8px !important;
    font-weight: 600 !important; font-size: 13px !important;
    padding: .5rem 1.4rem !important; transition: all .2s !important;
}
.stButton > button:hover { background: #3451d1 !important; transform: translateY(-1px) !important; }

/* Inputs */
.stSelectbox > div > div, .stNumberInput > div > div > input {
    background: #111827 !important; border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 8px !important; color: #E8EAF0 !important;
}
.stSelectbox label, .stSlider label, .stNumberInput label, .stTextInput label {
    color: #9CA3AF !important; font-size: 11px !important;
    font-weight: 500 !important; text-transform: uppercase !important;
    letter-spacing: .05em !important;
}
.stSlider [data-baseweb="slider"] { padding: 0 !important; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: #111827 !important; border-radius: 8px !important;
    padding: 3px !important; border: 1px solid rgba(255,255,255,0.06) !important;
}
.stTabs [data-baseweb="tab"] {
    color: #6B7280 !important; background: transparent !important;
    border-radius: 6px !important; font-size: 12px !important;
    font-weight: 500 !important; padding: .35rem 1rem !important;
}
.stTabs [aria-selected="true"] { background: #4361EE !important; color: white !important; }

/* Scrollbar */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: #080B14; }
::-webkit-scrollbar-thumb { background: #374151; border-radius: 99px; }

/* Dataframe */
[data-testid="stDataFrame"] iframe { border-radius: 10px !important; }

/* Text inputs */
.stTextInput > div > div > input {
    background: #111827 !important; border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 8px !important; color: #E8EAF0 !important;
}
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:1rem;border-bottom:1px solid rgba(255,255,255,0.06);margin-bottom:.5rem">
        <div style="display:flex;align-items:center;gap:10px">
            <div style="width:36px;height:36px;background:linear-gradient(135deg,#4361EE,#7209B7);
                        border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:18px">🎓</div>
            <div>
                <div style="color:#E8EAF0;font-weight:700;font-size:15px">UNI·AI</div>
                <div style="color:#6B7280;font-size:10px;letter-spacing:.08em">OULAD PLATFORM</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<p style="color:#6B7280;font-size:10px;font-weight:600;letter-spacing:.1em;padding:.8rem 0 .3rem">MENU</p>', unsafe_allow_html=True)

    page = st.radio("nav", [
        "🏠  Dashboard",
        "🔮  Student Prediction",
        "📊  Model Performance",
        "📈  EDA & Insights",
        "🧠  SHAP Explainability",
    ], label_visibility="collapsed")

    st.markdown("""
    <div style="margin-top:1.5rem;background:#111827;border-radius:10px;padding:.9rem 1rem;
                border:1px solid rgba(255,255,255,0.06)">
        <p style="color:#E8EAF0;font-size:11px;font-weight:600;margin:0 0 .5rem">OULAD Dataset</p>
        <div style="display:flex;justify-content:space-between;margin-bottom:.25rem">
            <span style="color:#6B7280;font-size:11px">Students</span>
            <span style="color:#4CC9F0;font-size:11px;font-weight:600">32,593</span>
        </div>
        <div style="display:flex;justify-content:space-between;margin-bottom:.25rem">
            <span style="color:#6B7280;font-size:11px">Features</span>
            <span style="color:#4CC9F0;font-size:11px;font-weight:600">70+</span>
        </div>
        <div style="display:flex;justify-content:space-between">
            <span style="color:#6B7280;font-size:11px">Tables used</span>
            <span style="color:#06D6A0;font-size:11px;font-weight:600">7 / 7 ✓</span>
        </div>
    </div>
    <div style="margin-top:.8rem;background:linear-gradient(135deg,rgba(67,97,238,0.12),rgba(114,9,183,0.12));
                border-radius:10px;padding:.9rem 1rem;border:1px solid rgba(67,97,238,0.25)">
        <p style="color:#4CC9F0;font-size:10px;font-weight:600;margin:0 0 .4rem">⚡ Best Model</p>
        <p style="color:#E8EAF0;font-size:12px;font-weight:600;margin:0 0 .4rem">LightGBM (Tuned)</p>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:.3rem">
            <div style="text-align:center;background:rgba(0,0,0,0.3);border-radius:6px;padding:.3rem">
                <div style="color:#6B7280;font-size:9px">AUC</div>
                <div style="color:#E8EAF0;font-size:13px;font-weight:700">92.4%</div>
            </div>
            <div style="text-align:center;background:rgba(0,0,0,0.3);border-radius:6px;padding:.3rem">
                <div style="color:#6B7280;font-size:9px">F1</div>
                <div style="color:#E8EAF0;font-size:13px;font-weight:700">88.2%</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Route ─────────────────────────────────────────────────────
if   "Dashboard"   in page: from pages_code import dashboard;  dashboard.show()
elif "Prediction"  in page: from pages_code import predict;    predict.show()
elif "Performance" in page: from pages_code import model_perf; model_perf.show()
elif "EDA"         in page: from pages_code import eda;        eda.show()
elif "SHAP"        in page: from pages_code import shap_page;  shap_page.show()
