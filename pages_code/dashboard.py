import streamlit as st
import plotly.graph_objects as go
import numpy as np
from . import utils


def show():
    st.markdown("""
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:1.5rem">
        <div>
            <h1 style="color:#E8EAF0;font-size:24px;font-weight:700;margin:0">Welcome back, Admin 👋</h1>
            <p style="color:#6B7280;font-size:13px;margin:.2rem 0 0">OULAD Academic Intelligence Platform</p>
        </div>
        <div style="background:#111827;border:1px solid rgba(255,255,255,0.06);border-radius:8px;
                    padding:.5rem 1rem;color:#6B7280;font-size:12px">📅 2013–2014 Academic Year</div>
    </div>
    """, unsafe_allow_html=True)

    # ── KPI Row ───────────────────────────────────────────────
    cols = st.columns(6)
    kpis = [
        ("Total Students",   "32,593", "+8.2%",  "#4CC9F0"),
        ("At-Risk Students", "12,841", "39.4%",  "#F72585"),
        ("Pass Rate",        "55.2%",  "+3.1%",  "#06D6A0"),
        ("Distinction Rate", "13.0%",  "+1.4%",  "#4361EE"),
        ("Withdrawal Rate",  "26.7%",  "-2.1%",  "#FFD166"),
        ("Avg Score",        "68.4%",  "+4.3%",  "#7209B7"),
    ]
    for col, (label, value, delta, clr) in zip(cols, kpis):
        with col:
            st.markdown(f"""
            <div style="background:#111827;border:1px solid rgba(255,255,255,0.06);border-radius:12px;
                        padding:1rem;position:relative;overflow:hidden">
                <div style="position:absolute;top:0;left:0;right:0;height:3px;background:{clr}"></div>
                <p style="color:#6B7280;font-size:10px;font-weight:600;text-transform:uppercase;
                           letter-spacing:.07em;margin:0 0 .4rem">{label}</p>
                <p style="color:#E8EAF0;font-size:21px;font-weight:700;margin:0">{value}</p>
                <p style="color:{clr};font-size:11px;margin:.3rem 0 0;font-weight:500">{delta}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:.8rem'></div>", unsafe_allow_html=True)

    # ── Row 2: Area chart + Donut ─────────────────────────────
    c1, c2 = st.columns([3, 2])

    with c1:
        utils.card_header("Student Performance Over Time", "By presentation period")
        presentations = ['2013-B', '2013-J', '2014-B', '2014-J']
        area_data = {
            'Distinction': ([4100, 4300, 4500, 4250], '#4361EE', 'rgba(67,97,238,0.20)'),
            'Pass':        ([17200,17800,18100,17500], '#4CC9F0', 'rgba(76,201,240,0.15)'),
            'Fail':        ([5200, 5100, 4900, 5300], '#F72585', 'rgba(247,37,133,0.15)'),
            'Withdrawn':   ([8700, 8600, 8500, 8800], '#7209B7', 'rgba(114,9,183,0.15)'),
        }
        fig = go.Figure()
        for label, (vals, clr, fill) in area_data.items():
            fig.add_trace(go.Scatter(
                x=presentations, y=vals, name=label,
                stackgroup='one',
                line=dict(width=1.5, color=clr),
                fillcolor=fill,
                hovertemplate=f'<b>{label}</b>: %{{y:,}}<extra></extra>',
            ))
        fig.update_layout(**utils.dark_layout(height=240))
        fig.update_layout(legend=dict(orientation='h', y=1.1, x=0))
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    with c2:
        utils.card_header("Risk Distribution")
        fig2 = go.Figure(go.Pie(
            labels=['Low Risk', 'Medium Risk', 'High Risk'],
            values=[65.2, 21.8, 13.0],
            hole=0.62,
            marker=dict(
                colors=['#4CC9F0', '#FFD166', '#F72585'],
                line=dict(color='#080B14', width=3),
            ),
            textinfo='percent',
            textfont=dict(size=11, color='white'),
            hovertemplate='<b>%{label}</b>: %{value}%<extra></extra>',
        ))
        fig2.add_annotation(
            text='<b>12,841</b><br><span style="font-size:10px">At Risk</span>',
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=13, color='#E8EAF0'),
        )
        fig2.update_layout(**utils.dark_layout(height=240))
        fig2.update_layout(showlegend=True,
                           legend=dict(orientation='v', x=1.0, y=0.5, font=dict(size=10)))
        st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})

    # ── Row 3: Heatmap + Top at-risk + Leaderboard ───────────
    c1, c2, c3 = st.columns(3)

    with c1:
        utils.card_header("Engagement Heatmap", "VLE clicks by day & hour")
        days  = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
        hours = ['6AM','9AM','12PM','3PM','6PM','9PM']
        np.random.seed(42)
        z = np.random.randint(20, 280, (7, 6))
        z[1][3] = 280; z[2][4] = 260; z[3][2] = 250
        fig3 = go.Figure(go.Heatmap(
            z=z, x=hours, y=days,
            colorscale=[[0,'#0D1117'],[0.4,'#4361EE'],[0.7,'#7209B7'],[1,'#F72585']],
            showscale=False,
            hovertemplate='<b>%{y} %{x}</b>: %{z} clicks<extra></extra>',
        ))
        fig3.update_layout(**utils.dark_layout(height=230))
        st.plotly_chart(fig3, use_container_width=True, config={'displayModeBar': False})

    with c2:
        utils.card_header("Top At-Risk Students")
        students = [
            ("Ahmed K.",   "High Risk",   92, "#F72585"),
            ("Nourhan A.", "High Risk",   87, "#F72585"),
            ("Omar H.",    "Medium Risk", 78, "#FFD166"),
            ("Sara M.",    "Medium Risk", 72, "#FFD166"),
            ("Mostafa M.", "Medium Risk", 69, "#FFD166"),
        ]
        for name, risk, pct, clr in students:
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:.7rem;padding:.45rem 0;
                        border-bottom:1px solid rgba(255,255,255,0.04)">
                <div style="width:28px;height:28px;border-radius:50%;background:{clr}22;
                            border:1px solid {clr}44;display:flex;align-items:center;
                            justify-content:center;font-size:11px;flex-shrink:0">👤</div>
                <div style="flex:1">
                    <p style="color:#E8EAF0;font-size:12px;font-weight:500;margin:0">{name}</p>
                    <span style="background:{clr}22;color:{clr};font-size:9px;padding:1px 6px;
                                 border-radius:4px;font-weight:600">{risk}</span>
                </div>
                <div style="text-align:right">
                    <p style="color:{clr};font-size:13px;font-weight:700;margin:0">{pct}%</p>
                    <div style="background:rgba(255,255,255,0.06);border-radius:4px;height:3px;width:55px;margin-top:3px">
                        <div style="background:{clr};width:{pct}%;height:100%;border-radius:4px"></div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with c3:
        utils.card_header("Model Leaderboard", "By ROC-AUC")
        models = [
            ("Ensemble (Top3)",   93.1, "#06D6A0"),
            ("LightGBM (Tuned)",  92.4, "#4361EE"),
            ("XGBoost (Tuned)",   91.8, "#4CC9F0"),
            ("Random Forest",     89.2, "#7209B7"),
            ("Gradient Boosting", 88.7, "#FFD166"),
            ("MLP Neural Net",    87.5, "#F72585"),
        ]
        for i, (name, auc, clr) in enumerate(models):
            icon = "👑" if i == 0 else f"{i+1}."
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:.6rem;padding:.4rem 0;
                        border-bottom:1px solid rgba(255,255,255,0.04)">
                <span style="color:#6B7280;font-size:11px;width:18px">{icon}</span>
                <div style="flex:1">
                    <p style="color:#E8EAF0;font-size:11px;font-weight:500;margin:0 0 3px;
                               white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{name}</p>
                    <div style="background:rgba(255,255,255,0.05);border-radius:3px;height:4px">
                        <div style="background:{clr};width:{auc}%;height:100%;border-radius:3px"></div>
                    </div>
                </div>
                <span style="color:{clr};font-size:12px;font-weight:700;min-width:38px;text-align:right">{auc}%</span>
            </div>
            """, unsafe_allow_html=True)

    # ── AI Insights banner ────────────────────────────────────
    st.markdown("<div style='height:.8rem'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="background:linear-gradient(135deg,rgba(67,97,238,0.10),rgba(114,9,183,0.10));
                border:1px solid rgba(67,97,238,0.22);border-radius:12px;padding:1.1rem 1.4rem;
                display:flex;gap:1.2rem;align-items:flex-start">
        <span style="font-size:26px">🧠</span>
        <div style="flex:1">
            <p style="color:#4CC9F0;font-size:10px;font-weight:600;letter-spacing:.1em;
                      text-transform:uppercase;margin:0 0 .5rem">AI Insights</p>
            <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:1rem">
                <p style="color:#9CA3AF;font-size:12px;line-height:1.6;margin:0">
                    📌 Students engaging in <b style="color:#E8EAF0">first 2 weeks</b>
                    are <b style="color:#06D6A0">3.2×</b> more likely to pass
                </p>
                <p style="color:#9CA3AF;font-size:12px;line-height:1.6;margin:0">
                    📌 <b style="color:#FFD166">on_schedule_ratio</b> is the strongest
                    new predictor — beats raw click count
                </p>
                <p style="color:#9CA3AF;font-size:12px;line-height:1.6;margin:0">
                    📌 Early registration (before module start) reduces dropout risk
                    by <b style="color:#4CC9F0">18%</b>
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
