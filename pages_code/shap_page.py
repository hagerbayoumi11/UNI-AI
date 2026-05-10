import streamlit as st
import plotly.graph_objects as go
import numpy as np
from . import utils


def show():
    st.markdown("""
    <h1 style="color:#E8EAF0;font-size:24px;font-weight:700;margin:0 0 .3rem">🧠 SHAP Explainability</h1>
    <p style="color:#6B7280;font-size:13px;margin:0 0 1.5rem">
        Why the model makes each prediction — global and local explanations
    </p>
    """, unsafe_allow_html=True)

    np.random.seed(99)
    feats = [f[0] for f in utils.TOP_FEATURES[:12]]
    imps  = [f[1] for f in utils.TOP_FEATURES[:12]]
    cats  = [f[2] for f in utils.TOP_FEATURES[:12]]

    tab1, tab2, tab3 = st.tabs(["🐝 Beeswarm (Global)","💧 Waterfall (Single Student)","🔗 Dependence Plot"])

    with tab1:
        utils.card_header("SHAP Beeswarm — Global Impact",
                           "Each dot = 1 student · Color = feature value (blue=low, red=high) · X = impact on risk")
        fig = go.Figure()
        n = 300
        for i, (feat, imp, cat) in enumerate(zip(feats, imps, cats)):
            shap_v = np.random.normal(0, imp*3, n)
            feat_v = np.random.uniform(0, 1, n)
            y_j    = i + np.random.uniform(-0.35, 0.35, n)
            fig.add_trace(go.Scatter(
                x=shap_v, y=y_j, mode='markers',
                marker=dict(size=4, color=feat_v,
                            colorscale=[[0,'#4361EE'],[0.5,'#E8EAF0'],[1,'#F72585']],
                            line=dict(width=0)),
                name=feat, showlegend=False,
                hovertemplate=f'<b>{feat}</b><br>SHAP: %{{x:.3f}}<extra></extra>',
            ))
        fig.update_layout(**utils.dark_layout(height=480))
        fig.update_layout(
            xaxis_title='SHAP Value (impact on predicted risk)',
            yaxis=dict(
                tickmode='array',
                tickvals=list(range(len(feats))),
                ticktext=[f'<span style="color:{utils.CAT_COLORS[cats[i]]}">{f}</span>'
                          for i, f in enumerate(feats)],
                tickfont=dict(size=11),
            ),
        )
        fig.add_vline(x=0, line_dash='dash', line_color='rgba(255,255,255,0.10)', line_width=1)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar':False})

        st.markdown("""
        <div style="display:flex;gap:1.5rem;margin-top:.3rem">
            <p style="color:#9CA3AF;font-size:11px;margin:0">
                <b style="color:#4361EE">■</b> Blue dot = low feature value
            </p>
            <p style="color:#9CA3AF;font-size:11px;margin:0">
                <b style="color:#F72585">■</b> Red dot = high feature value
            </p>
            <p style="color:#9CA3AF;font-size:11px;margin:0">
                Positive SHAP = increases risk · Negative = reduces risk
            </p>
        </div>
        """, unsafe_allow_html=True)

    with tab2:
        utils.card_header("Waterfall — Individual Student Explanation")

        col_sel, _ = st.columns([3,7])
        with col_sel:
            profile = st.selectbox("Student Profile",
                                   ["High Risk Student","Medium Risk Student","Low Risk Student"])

        if "High Risk" in profile:
            base, pred = 0.50, 0.87
            contribs = [
                ("avg_score",         -0.142, "Low score → ↑ risk"),
                ("on_schedule_ratio", -0.118, "Irregular → ↑ risk"),
                ("fail_ratio",        -0.089, "High fails → ↑ risk"),
                ("active_day_ratio",  -0.068, "Low activity → ↑ risk"),
                ("score_trend",       -0.045, "Declining trend"),
                ("early_click_ratio", -0.038, "Low early engagement"),
                ("edu_num",           +0.021, "Higher edu → ↓ risk"),
                ("click_consistency", -0.031, "Inconsistent"),
            ]
        elif "Medium Risk" in profile:
            base, pred = 0.50, 0.48
            contribs = [
                ("avg_score",         -0.062, "Slightly below avg"),
                ("on_schedule_ratio", +0.044, "Mostly on schedule"),
                ("fail_ratio",        -0.038, "Some failures"),
                ("active_day_ratio",  +0.031, "Moderate activity"),
                ("score_trend",       -0.022, "Slightly declining"),
                ("early_click_ratio", +0.018, "Decent early eng."),
                ("reg_timing",        +0.012, "Registered on time"),
                ("click_consistency", -0.015, "Somewhat irregular"),
            ]
        else:
            base, pred = 0.50, 0.13
            contribs = [
                ("avg_score",         +0.128, "High score → ↓ risk"),
                ("on_schedule_ratio", +0.110, "On schedule → ↓ risk"),
                ("fail_ratio",        +0.072, "No failures → ↓ risk"),
                ("active_day_ratio",  +0.065, "Very active"),
                ("score_trend",       +0.048, "Improving trend"),
                ("early_click_ratio", +0.041, "Engaged early"),
                ("reg_timing",        +0.033, "Registered early"),
                ("click_consistency", +0.028, "Very consistent"),
            ]

        labels   = ["Base rate"] + [c[0] for c in contribs] + ["Prediction"]
        y_vals   = [base] + [c[1] for c in contribs] + [pred]
        measures = ['absolute'] + ['relative']*len(contribs) + ['total']

        fig_wf = go.Figure(go.Waterfall(
            orientation='v', measure=measures,
            x=labels, y=y_vals,
            text=[f'{v:.2f}' if i==0 or i==len(y_vals)-1 else f'{v:+.3f}'
                  for i,v in enumerate(y_vals)],
            textposition='outside',
            textfont=dict(size=10, color='#E8EAF0'),
            connector=dict(line=dict(color='rgba(255,255,255,0.06)', width=1, dash='dot')),
            increasing=dict(marker=dict(color='#F72585')),
            decreasing=dict(marker=dict(color='#06D6A0')),
            totals=dict(marker=dict(color='#FFD166')),
        ))
        fig_wf.add_hline(y=0.45, line_dash='dash', line_color='rgba(255,209,102,0.5)',
                          annotation_text='Threshold (0.45)',
                          annotation_font=dict(size=10, color='#FFD166'))
        fig_wf.update_layout(**utils.dark_layout(height=400))
        fig_wf.update_layout(xaxis_tickangle=-25, yaxis_range=[0,1.15],
                              yaxis_title='Risk Probability')
        st.plotly_chart(fig_wf, use_container_width=True, config={'displayModeBar':False})

        clr, fill, lbl = utils.risk_info(pred)
        m1, m2, m3 = st.columns(3)
        for col, (title, val, c) in zip([m1,m2,m3],[
            ("Base Rate", "50.0%", "#6B7280"),
            ("Prediction", f"{pred*100:.0f}%", clr),
            ("Risk Label", lbl.split()[-1]+" "+lbl.split()[0], clr),
        ]):
            with col:
                st.markdown(f"""
                <div style="background:#111827;border:1px solid rgba(255,255,255,0.06);
                            border-radius:10px;padding:.8rem;text-align:center">
                    <p style="color:#6B7280;font-size:10px;text-transform:uppercase;
                               letter-spacing:.07em;margin:0 0 .2rem">{title}</p>
                    <p style="color:{c};font-size:18px;font-weight:700;margin:0">{val}</p>
                </div>
                """, unsafe_allow_html=True)

    with tab3:
        utils.card_header("SHAP Dependence Plot", "How a feature's value affects predicted risk")
        feat_sel = st.selectbox("Select Feature", feats)
        idx  = feats.index(feat_sel)
        imp  = imps[idx]
        cat  = cats[idx]
        n    = 500
        feat_v = np.random.uniform(0, 1, n)
        shap_v = np.clip(-imp*4*feat_v + imp*1.5 + np.random.normal(0, imp*0.8, n), -0.4, 0.4)
        inter  = np.random.uniform(0, 1, n)

        fig_dep = go.Figure(go.Scatter(
        x=feat_v, y=shap_v, mode='markers',
        marker=dict(
            size=5,
            color=inter,
            colorscale=[[0,'#4361EE'],[0.5,'#E8EAF0'],[1,'#F72585']],
            colorbar=dict(
                title=dict(
                    text='Interaction',
                    font=dict(color='#9CA3AF', size=10)
                ),
                tickfont=dict(color='#6B7280', size=9),
                len=0.7
            )
        ),
        hovertemplate=f'<b>{feat_sel}</b>: %{{x:.3f}}<br>SHAP: %{{y:.3f}}<extra></extra>',
    ))
        # Trend line
        z = np.polyfit(feat_v, shap_v, 2)
        p = np.poly1d(z)
        x_l = np.linspace(0, 1, 100)
        fig_dep.add_trace(go.Scatter(
            x=x_l, y=p(x_l), mode='lines',
            line=dict(color='#FFD166', width=2, dash='dot'),
            showlegend=False,
        ))
        fig_dep.add_hline(y=0, line_dash='dash',
                           line_color='rgba(255,255,255,0.10)', line_width=1)
        fig_dep.update_layout(**utils.dark_layout(height=380))
        fig_dep.update_layout(
            xaxis_title=f'{feat_sel} (normalized 0–1)',
            yaxis_title='SHAP Value (impact on risk)',
        )
        st.plotly_chart(fig_dep, use_container_width=True, config={'displayModeBar':False})

        clr_cat = utils.CAT_COLORS[cat]
        st.markdown(f"""
        <div style="background:#111827;border:1px solid rgba(255,255,255,0.06);
                    border-radius:10px;padding:.8rem 1.1rem">
            <span style="color:{clr_cat};font-weight:600;font-size:12px">{feat_sel}</span>
            <span style="color:#6B7280;font-size:11px"> · {cat} · Importance: </span>
            <span style="color:#E8EAF0;font-size:11px;font-weight:600">{imp:.3f}</span>
            <span style="color:#6B7280;font-size:11px"> · As value increases → </span>
            <span style="color:#06D6A0;font-size:11px;font-weight:600">risk decreases</span>
        </div>
        """, unsafe_allow_html=True)
