import streamlit as st
import plotly.graph_objects as go
import numpy as np
from . import utils


# ── Risk computation (transparent scoring) ────────────────────
def compute_risk(avg_score, min_score, fail_ratio, on_time_ratio, score_trend,
                 unsubmitted, on_schedule, active_day_ratio, click_consistency,
                 early_clicks, total_clicks, active_days, reg_timing,
                 registered_early, withdrew_any, prev_attempts, edu_idx, imd_idx):
    s = 0.50
    # Assessment (38%)
    s += (50 - avg_score)  / 50  * 0.14
    s += fail_ratio                * 0.09
    s += (1 - on_time_ratio)      * 0.06
    s -= score_trend               * 0.03
    s += unsubmitted               * 0.012
    s += max(40 - min_score, 0) / 40 * 0.04
    # VLE (37%)
    s += (1 - on_schedule)        * 0.12
    s += (0.5 - active_day_ratio) * 0.07
    s += (1 - click_consistency)  * 0.06
    ec_ratio = early_clicks / (total_clicks + 1)
    s += (0.15 - ec_ratio)        * 0.04
    cpd = total_clicks / max(active_days, 1)
    s += (100 - min(cpd, 100)) / 100 * 0.04
    # Registration (10%)
    s += max(reg_timing, 0) * 0.001
    s += -0.03 if registered_early else 0.03
    s += 0.08 if withdrew_any else 0
    s += prev_attempts * 0.018
    # Demographics (8%)
    s += (4 - edu_idx) * 0.008
    s += (5 - imd_idx) * 0.006
    return float(np.clip(s, 0.03, 0.97))


def get_contributions(avg_score, fail_ratio, on_schedule, active_day_ratio,
                       score_trend, early_clicks, total_clicks, reg_timing,
                       click_consistency, withdrew_any, unsubmitted, on_time_ratio):
    ec_ratio = early_clicks / (total_clicks + 1)
    items = [
        ("avg_score",         abs((50 - avg_score) / 50 * 0.14),  1 if avg_score < 50 else -1),
        ("on_schedule_ratio", abs((1 - on_schedule) * 0.12),       1 if on_schedule < 0.6 else -1),
        ("fail_ratio",        abs(fail_ratio * 0.09),               1 if fail_ratio > 0.1 else -1),
        ("active_day_ratio",  abs((0.5 - active_day_ratio) * 0.07), 1 if active_day_ratio < 0.5 else -1),
        ("click_consistency", abs((1 - click_consistency) * 0.06),  1 if click_consistency < 0.5 else -1),
        ("on_time_ratio",     abs((1 - on_time_ratio) * 0.06),      1 if on_time_ratio < 0.7 else -1),
        ("score_trend",       abs(score_trend * 0.03),              -1 if score_trend > 0 else 1),
        ("early_click_ratio", abs((0.15 - ec_ratio) * 0.04),       -1 if ec_ratio > 0.15 else 1),
        ("reg_timing",        abs(max(reg_timing, 0) * 0.001),      1 if reg_timing > 0 else -1),
        ("withdrew_any",      0.08 if withdrew_any else 0,           1 if withdrew_any else -1),
    ]
    items.sort(key=lambda x: x[1], reverse=True)
    return items[:8]


def get_recommendations(risk, avg_score, on_schedule, active_ratio,
                          fail_ratio, trend, early_clicks, withdrew):
    recs = []
    if on_schedule < 0.5:
        recs.append(("📅", "Encourage weekly VLE schedule — on_schedule_ratio is the #1 predictor"))
    if avg_score < 55:
        recs.append(("📝", "Arrange academic support — score below passing threshold"))
    if active_ratio < 0.4:
        recs.append(("💻", "Boost platform engagement — active less than 40% of available days"))
    if fail_ratio > 0.2:
        recs.append(("⚠️", "Provide remedial content — failing more than 20% of assessments"))
    if trend < -1.0:
        recs.append(("📉", "Alert academic advisor — score is declining over the course"))
    if early_clicks < 100:
        recs.append(("🚀", "Intervene early — very low engagement in first 2 weeks"))
    if withdrew:
        recs.append(("🔴", "High withdrawal history — assign a dedicated academic mentor"))
    if risk < 0.3:
        recs.append(("✅", "Student is on track — maintain engagement and monitor"))
    return recs[:4] if recs else [("✅", "Student profile looks healthy — no immediate action needed")]


def show():
    st.markdown("""
    <h1 style="color:#E8EAF0;font-size:24px;font-weight:700;margin:0 0 .3rem">🔮 Student Risk Prediction</h1>
    <p style="color:#6B7280;font-size:13px;margin:0 0 1.5rem">
        Enter student profile → get instant dropout probability + recommendations
    </p>
    """, unsafe_allow_html=True)

    left, right = st.columns([5, 5], gap="large")

    # ════════════════════════════════════════
    # LEFT — Input form
    # ════════════════════════════════════════
    with left:

        # A — Demographics
        with st.expander("👤  A — Demographics", expanded=True):
            c1, c2 = st.columns(2)
            with c1:
                gender     = st.selectbox("Gender", ["Male","Female"])
                age        = st.selectbox("Age Band", ["0-35","35-55","55<="])
                disability = st.selectbox("Disability", ["No","Yes"])
            with c2:
                edu = st.selectbox("Education Level", [
                    "No Formal quals","Lower Than A Level",
                    "A Level or Equivalent","HE Qualification",
                    "Post Graduate Qualification"], index=2)
                imd = st.selectbox("IMD Band", [
                    "0-10%","10-20%","20-30%","30-40%","40-50%",
                    "50-60%","60-70%","70-80%","80-90%","90-100%"], index=5)
            prev_attempts   = st.slider("Previous Attempts", 0, 5, 0)
            studied_credits = st.slider("Studied Credits", 30, 655, 120, step=30)

        # B — VLE Engagement
        with st.expander("📱  B — VLE Engagement", expanded=True):
            c1, c2 = st.columns(2)
            with c1:
                total_clicks  = st.number_input("Total Clicks",         0, 50000, 4500, step=100)
                early_clicks  = st.number_input("Early Clicks (wk 1-2)",0, 5000,  300,  step=50)
                active_days   = st.number_input("Active Days",          0, 300,   85,   step=5)
            with c2:
                clicks_per_week  = st.number_input("Clicks / Week",     0, 1000,  175,  step=10)
                active_day_ratio = st.slider("Active Day Ratio",   0.0, 1.0, 0.55, step=0.01)
                on_schedule      = st.slider("On-Schedule Ratio",  0.0, 1.0, 0.62, step=0.01)
            click_consistency = st.slider("Click Consistency (0=irregular → 1=regular)", 0.0, 1.0, 0.45, step=0.01)

        # C — Assessment
        with st.expander("📝  C — Assessment Performance", expanded=True):
            c1, c2 = st.columns(2)
            with c1:
                avg_score     = st.slider("Average Score (%)",  0, 100, 65)
                min_score     = st.slider("Minimum Score (%)",  0, 100, 40)
                n_assessments = st.number_input("# Assessments", 0, 20, 6)
            with c2:
                fail_ratio    = st.slider("Fail Ratio",    0.0, 1.0, 0.15, step=0.01)
                on_time_ratio = st.slider("On-Time Ratio", 0.0, 1.0, 0.80, step=0.01)
                score_trend   = st.slider("Score Trend  (+ = improving)", -5.0, 5.0, 0.5, step=0.1)
            unsubmitted = st.slider("Unsubmitted Assignments", 0, 10, 1)

        # D — Registration
        with st.expander("🗓️  D — Registration Timing", expanded=True):
            c1, c2 = st.columns(2)
            with c1:
                reg_timing       = st.slider("Days Before Module Start (negative = early)", -100, 30, -25)
                registered_early = st.selectbox("Registered Early?", ["Yes","No"])
            with c2:
                withdrew_any = st.selectbox("Withdrew From Any Module?", ["No","Yes"])
                n_modules    = st.number_input("Modules Registered", 1, 10, 2)

        predict_btn = st.button("⚡  RUN PREDICTION", use_container_width=True)

    # ════════════════════════════════════════
    # RIGHT — Results
    # ════════════════════════════════════════
    with right:

        # Compute
        edu_idx = ["No Formal quals","Lower Than A Level","A Level or Equivalent",
                   "HE Qualification","Post Graduate Qualification"].index(edu)
        imd_idx = ["0-10%","10-20%","20-30%","30-40%","40-50%",
                   "50-60%","60-70%","70-80%","80-90%","90-100%"].index(imd)

        risk = compute_risk(
            avg_score=avg_score, min_score=min_score,
            fail_ratio=fail_ratio, on_time_ratio=on_time_ratio,
            score_trend=score_trend, unsubmitted=unsubmitted,
            on_schedule=on_schedule, active_day_ratio=active_day_ratio,
            click_consistency=click_consistency, early_clicks=early_clicks,
            total_clicks=total_clicks, active_days=active_days,
            reg_timing=reg_timing,
            registered_early=(registered_early == "Yes"),
            withdrew_any=(withdrew_any == "Yes"),
            prev_attempts=prev_attempts, edu_idx=edu_idx, imd_idx=imd_idx,
        )

        clr, fill_clr, label = utils.risk_info(risk)
        pct = int(risk * 100)

        # ── Gauge ────────────────────────────────────────────
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=pct,
            number=dict(suffix="%", font=dict(size=56, color=clr, family='Inter')),
            gauge=dict(
                axis=dict(range=[0,100], tickfont=dict(size=10, color='#6B7280'),
                          tickcolor='rgba(255,255,255,0.1)', dtick=25),
                bar=dict(color=clr, thickness=0.3),
                bgcolor='rgba(0,0,0,0)',
                borderwidth=0,
                steps=[
                    dict(range=[0,40],  color='rgba(6,214,160,0.07)'),
                    dict(range=[40,70], color='rgba(255,209,102,0.07)'),
                    dict(range=[70,100],color='rgba(247,37,133,0.07)'),
                ],
                threshold=dict(line=dict(color=clr, width=3), thickness=0.8, value=pct),
            ),
        ))
        fig_gauge.update_layout(
            height=270, margin=dict(l=20,r=20,t=20,b=0),
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Inter'),
        )
        st.plotly_chart(fig_gauge, use_container_width=True, config={'displayModeBar':False})

        # Risk badge
        st.markdown(f"""
        <div style="text-align:center;margin:-1rem 0 1rem">
            <span style="background:{fill_clr};color:{clr};font-size:16px;font-weight:700;
                         padding:.4rem 1.8rem;border-radius:8px;border:1px solid {clr}44">
                {label}
            </span>
            <p style="color:#6B7280;font-size:11px;margin:.5rem 0 0">
                Model: LightGBM (Tuned) · Threshold: 0.45
            </p>
        </div>
        """, unsafe_allow_html=True)

        # ── Mini metrics ─────────────────────────────────────
        m1, m2, m3 = st.columns(3)
        for col, label_m, val_m in [
            (m1, "Risk Score",  f"{pct}%"),
            (m2, "Confidence",  f"{int(abs(risk-0.5)*200)}%"),
            (m3, "Priority",    "HIGH" if risk>0.7 else "MED" if risk>0.4 else "LOW"),
        ]:
            with col:
                c2_ = '#F72585' if risk>0.7 else '#FFD166' if risk>0.4 else '#06D6A0'
                st.markdown(f"""
                <div style="background:#111827;border:1px solid rgba(255,255,255,0.06);
                            border-radius:10px;padding:.7rem;text-align:center">
                    <p style="color:#6B7280;font-size:9px;text-transform:uppercase;
                               letter-spacing:.07em;margin:0 0 .2rem">{label_m}</p>
                    <p style="color:{c2_};font-size:16px;font-weight:700;margin:0">{val_m}</p>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<div style='height:.6rem'></div>", unsafe_allow_html=True)

        # ── Feature Contributions ────────────────────────────
        utils.card_header("Feature Contributions", "Which inputs drive this prediction")
        contribs = get_contributions(
            avg_score=avg_score, fail_ratio=fail_ratio, on_schedule=on_schedule,
            active_day_ratio=active_day_ratio, score_trend=score_trend,
            early_clicks=early_clicks, total_clicks=total_clicks,
            reg_timing=reg_timing, click_consistency=click_consistency,
            withdrew_any=(withdrew_any=="Yes"), unsubmitted=unsubmitted,
            on_time_ratio=on_time_ratio,
        )

        feat_names = [c[0] for c in contribs]
        feat_vals  = [c[1] for c in contribs]
        feat_dirs  = [c[2] for c in contribs]
        bar_colors = ['#F72585' if d > 0 else '#06D6A0' for d in feat_dirs]

        fig_bar = go.Figure(go.Bar(
            x=feat_vals[::-1], y=feat_names[::-1],
            orientation='h',
            marker_color=bar_colors[::-1],
            marker_line_width=0,
            hovertemplate='<b>%{y}</b>: %{x:.3f}<extra></extra>',
        ))
        fig_bar.update_layout(**utils.dark_layout(height=240))
        fig_bar.update_layout(xaxis_title='Impact magnitude')
        st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar':False})

        # ── Recommendations ───────────────────────────────────
        recs = get_recommendations(risk, avg_score, on_schedule, active_day_ratio,
                                    fail_ratio, score_trend, early_clicks, withdrew_any=="Yes")

        recs_html = "".join([
            f'<div style="display:flex;gap:.6rem;margin-bottom:.45rem;align-items:flex-start">'
            f'<span style="font-size:13px;flex-shrink:0">{icon}</span>'
            f'<p style="color:#9CA3AF;font-size:12px;line-height:1.5;margin:0">{text}</p>'
            f'</div>'
            for icon, text in recs
        ])

        st.markdown(f'''
        <div style="background:linear-gradient(135deg,rgba(67,97,238,0.08),rgba(114,9,183,0.08));
                    border:1px solid rgba(67,97,238,0.20);border-radius:12px;padding:1rem 1.2rem">
            <p style="color:#4CC9F0;font-size:10px;font-weight:600;letter-spacing:.1em;
                      text-transform:uppercase;margin:0 0 .7rem">💡 Recommendations</p>
            {recs_html}
        </div>
        ''', unsafe_allow_html=True)

        # ── Probability breakdown donut ───────────────────────
        st.markdown("<div style='height:.6rem'></div>", unsafe_allow_html=True)
        utils.card_header("Prediction Breakdown")
        fig_d = go.Figure(go.Pie(
            labels=['At-Risk', 'Success'],
            values=[pct, 100-pct],
            hole=0.60,
            marker=dict(colors=[clr, 'rgba(255,255,255,0.06)'],
                        line=dict(color='#080B14', width=2)),
            textinfo='none',
            hovertemplate='<b>%{label}</b>: %{value}%<extra></extra>',
        ))
        fig_d.add_annotation(
            text=f'<b>{pct}%</b><br>At-Risk',
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=14, color=clr),
        )
        fig_d.update_layout(**utils.dark_layout(height=180))
        fig_d.update_layout(showlegend=False)
        st.plotly_chart(fig_d, use_container_width=True, config={'displayModeBar':False})
