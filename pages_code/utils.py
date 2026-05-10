import plotly.graph_objects as go

# ── Color helpers (no string manipulation bugs) ───────────────
COLORS = {
    'blue':   '#4361EE',
    'cyan':   '#4CC9F0',
    'pink':   '#F72585',
    'purple': '#7209B7',
    'green':  '#06D6A0',
    'amber':  '#FFD166',
    'gray':   '#6B7280',
}

RESULT_COLORS = {
    'Pass':        '#4CC9F0',
    'Distinction': '#4361EE',
    'Fail':        '#F72585',
    'Withdrawn':   '#7209B7',
}

# Pre-computed rgba strings (no runtime hex conversion)
RGBA = {
    'blue_25':   'rgba(67,97,238,0.25)',
    'blue_15':   'rgba(67,97,238,0.15)',
    'blue_08':   'rgba(67,97,238,0.08)',
    'cyan_25':   'rgba(76,201,240,0.25)',
    'cyan_08':   'rgba(76,201,240,0.08)',
    'pink_25':   'rgba(247,37,133,0.25)',
    'pink_08':   'rgba(247,37,133,0.08)',
    'purple_25': 'rgba(114,9,183,0.25)',
    'purple_08': 'rgba(114,9,183,0.08)',
    'green_08':  'rgba(6,214,160,0.08)',
    'amber_08':  'rgba(255,209,102,0.08)',
}

RESULT_RGBA = {
    'Pass':        'rgba(76,201,240,0.25)',
    'Distinction': 'rgba(67,97,238,0.25)',
    'Fail':        'rgba(247,37,133,0.25)',
    'Withdrawn':   'rgba(114,9,183,0.25)',
}

PALETTE = ['#4361EE','#4CC9F0','#F72585','#7209B7','#06D6A0',
           '#FFD166','#F3722C','#90E0EF','#9B5DE5','#00BBF9']

PALETTE_RGBA = [
    'rgba(67,97,238,0.15)',  'rgba(76,201,240,0.15)',
    'rgba(247,37,133,0.15)', 'rgba(114,9,183,0.15)',
    'rgba(6,214,160,0.15)',  'rgba(255,209,102,0.15)',
]

# ── Plotly dark theme ─────────────────────────────────────────
def dark_layout(height=320, margin=None):
    m = margin or dict(l=10, r=10, t=30, b=10)
    return dict(
        height=height,
        margin=m,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter, sans-serif', color='#6B7280', size=11),
        xaxis=dict(
            gridcolor='rgba(255,255,255,0.05)',
            zerolinecolor='rgba(255,255,255,0.05)',
            tickfont=dict(size=10, color='#6B7280'),
            linecolor='rgba(255,255,255,0.05)',
        ),
        yaxis=dict(
            gridcolor='rgba(255,255,255,0.05)',
            zerolinecolor='rgba(255,255,255,0.05)',
            tickfont=dict(size=10, color='#6B7280'),
            linecolor='rgba(255,255,255,0.05)',
        ),
        legend=dict(
            bgcolor='rgba(0,0,0,0)',
            font=dict(size=10, color='#9CA3AF'),
        ),
        hoverlabel=dict(
            bgcolor='#1F2937',
            font=dict(size=12, color='#E8EAF0'),
            bordercolor='rgba(67,97,238,0.4)',
        ),
    )

# ── Card header ───────────────────────────────────────────────
def card_header(title, subtitle=''):
    import streamlit as st
    sub = f'<p style="color:#6B7280;font-size:11px;margin:2px 0 0">{subtitle}</p>' if subtitle else ''
    st.markdown(f'''
    <div style="margin-bottom:.8rem">
        <p style="color:#E8EAF0;font-size:13px;font-weight:600;margin:0">{title}</p>
        {sub}
    </div>''', unsafe_allow_html=True)

# ── Risk helper ───────────────────────────────────────────────
def risk_info(prob):
    if prob >= 0.70:
        return '#F72585', 'rgba(247,37,133,0.15)', '🔴 High Risk'
    elif prob >= 0.40:
        return '#FFD166', 'rgba(255,209,102,0.15)', '🟡 Medium Risk'
    else:
        return '#06D6A0', 'rgba(6,214,160,0.15)',   '🟢 Low Risk'

# ── Model results (simulated — replace with joblib.load) ──────
MODEL_RESULTS = {
    'LightGBM (Tuned)':   {'Accuracy':88.3,'F1':88.2,'AUC':92.4,'AvgP':90.1,'CV':87.8,'Prec':88.1,'Rec':88.3},
    'XGBoost (Tuned)':    {'Accuracy':87.9,'F1':87.8,'AUC':91.8,'AvgP':89.4,'CV':87.3,'Prec':87.7,'Rec':87.9},
    'Ensemble (Top3)':    {'Accuracy':88.9,'F1':88.8,'AUC':93.1,'AvgP':91.0,'CV':0.0, 'Prec':88.7,'Rec':88.9},
    'Random Forest':      {'Accuracy':86.1,'F1':86.0,'AUC':89.2,'AvgP':87.1,'CV':85.5,'Prec':85.9,'Rec':86.1},
    'Gradient Boosting':  {'Accuracy':85.7,'F1':85.6,'AUC':88.7,'AvgP':86.3,'CV':85.0,'Prec':85.5,'Rec':85.7},
    'MLP Neural Net':     {'Accuracy':84.2,'F1':84.1,'AUC':87.5,'AvgP':84.8,'CV':83.6,'Prec':84.0,'Rec':84.2},
    'SVM':                {'Accuracy':83.5,'F1':83.3,'AUC':86.4,'AvgP':83.7,'CV':82.9,'Prec':83.2,'Rec':83.5},
    'Logistic Regression':{'Accuracy':80.1,'F1':79.9,'AUC':83.1,'AvgP':80.5,'CV':79.4,'Prec':79.8,'Rec':80.1},
    'KNN':                {'Accuracy':77.3,'F1':77.1,'AUC':79.8,'AvgP':76.9,'CV':76.5,'Prec':77.0,'Rec':77.3},
    'Decision Tree':      {'Accuracy':75.8,'F1':75.6,'AUC':76.2,'AvgP':74.3,'CV':75.0,'Prec':75.5,'Rec':75.8},
}

TOP_FEATURES = [
    ('avg_score',          0.142, 'Assessment'),
    ('on_schedule_ratio',  0.118, 'VLE'),
    ('clicks_per_week',    0.097, 'VLE'),
    ('fail_ratio',         0.089, 'Assessment'),
    ('early_click_ratio',  0.082, 'VLE'),
    ('score_momentum',     0.071, 'Assessment'),
    ('active_day_ratio',   0.068, 'VLE'),
    ('avg_reg_timing',     0.061, 'Registration'),
    ('click_consistency',  0.058, 'VLE'),
    ('min_score',          0.054, 'Assessment'),
    ('total_clicks',       0.049, 'VLE'),
    ('edu_num',            0.041, 'Demographics'),
    ('registered_early',   0.038, 'Registration'),
    ('imd_num',            0.034, 'Demographics'),
    ('n_assessments',      0.029, 'Assessment'),
]

CAT_COLORS = {
    'VLE':          '#4361EE',
    'Assessment':   '#4CC9F0',
    'Registration': '#FFD166',
    'Demographics': '#7209B7',
}
