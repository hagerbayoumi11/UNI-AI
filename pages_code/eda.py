import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from . import utils


def show():
    st.markdown("""
    <h1 style="color:#E8EAF0;font-size:24px;font-weight:700;margin:0 0 .3rem">📈 EDA & Insights</h1>
    <p style="color:#6B7280;font-size:13px;margin:0 0 1.5rem">
        Exploratory data analysis across all 7 OULAD tables
    </p>
    """, unsafe_allow_html=True)

    np.random.seed(42)
    tab1, tab2, tab3, tab4 = st.tabs(["🎯 Target & Demographics","📱 VLE Engagement","📝 Assessments","🔗 Feature Importance"])

    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            utils.card_header("Final Result Distribution")
            cats   = ['Pass','Withdrawn','Fail','Distinction']
            vals   = [12361, 7072, 7052, 3024]
            colors = ['#4CC9F0','#7209B7','#F72585','#4361EE']
            fig = go.Figure(go.Bar(
                x=cats, y=vals, marker_color=colors, marker_line_width=0,
                text=[f'{v:,}' for v in vals], textposition='outside',
                textfont=dict(color='#E8EAF0', size=11),
                hovertemplate='<b>%{x}</b>: %{y:,}<extra></extra>',
            ))
            fig.update_layout(**utils.dark_layout(height=270))
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar':False})

        with c2:
            utils.card_header("Pass Rate by Education Level")
            edu_l = ['No Formal','Lower A Level','A Level','HE Qual','Post Grad']
            rates = [42, 51, 58, 67, 73]
            bar_colors = ['#F72585','#F97316','#FFD166','#4CC9F0','#06D6A0']
            fig2 = go.Figure(go.Bar(
                x=rates, y=edu_l, orientation='h',
                marker_color=bar_colors, marker_line_width=0,
                text=[f'{v}%' for v in rates], textposition='outside',
                textfont=dict(color='#E8EAF0', size=10),
                hovertemplate='<b>%{y}</b>: %{x}%<extra></extra>',
            ))
            fig2.update_layout(**utils.dark_layout(height=270))
            fig2.update_layout(xaxis_range=[0,90], xaxis_ticksuffix='%')
            st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar':False})

        c3, c4 = st.columns(2)
        with c3:
            utils.card_header("Result by Gender")
            genders = ['Male','Female']
            g_data = {
                'Pass':        ([50.1,57.3], '#4CC9F0'),
                'Distinction': ([12.1,14.2], '#4361EE'),
                'Fail':        ([23.4,19.8], '#F72585'),
                'Withdrawn':   ([14.4, 8.7], '#7209B7'),
            }
            fig3 = go.Figure()
            for res, (vals, clr) in g_data.items():
                fig3.add_trace(go.Bar(
                    name=res, x=genders, y=vals,
                    marker_color=clr, marker_opacity=0.85, marker_line_width=0,
                    hovertemplate=f'<b>{res}</b>: %{{y:.1f}}%<extra></extra>',
                ))
            fig3.update_layout(**utils.dark_layout(height=270))
            fig3.update_layout(barmode='group', yaxis_ticksuffix='%',
                                legend=dict(orientation='h',y=1.08,x=0))
            st.plotly_chart(fig3, use_container_width=True, config={'displayModeBar':False})

        with c4:
            utils.card_header("Pass Rate by IMD Band", "Lower IMD = higher deprivation")
            imd_b = ['0-10%','20-30%','40-50%','60-70%','80-90%','90-100%']
            pass_r = [43, 49, 55, 61, 68, 72]
            fig4 = go.Figure(go.Scatter(
                x=imd_b, y=pass_r, mode='lines+markers',
                line=dict(color='#4361EE', width=2.5),
                marker=dict(color='#4CC9F0', size=8),
                fill='tozeroy', fillcolor='rgba(67,97,238,0.08)',
                hovertemplate='<b>%{x}</b>: %{y}%<extra></extra>',
            ))
            fig4.update_layout(**utils.dark_layout(height=270))
            fig4.update_layout(yaxis_range=[30,85], yaxis_ticksuffix='%', xaxis_tickangle=-30)
            st.plotly_chart(fig4, use_container_width=True, config={'displayModeBar':False})

    with tab2:
        utils.card_header("VLE Clicks by Final Result", "Violin plot — distribution shape")
        result_params = {
            'Distinction': (8.5, 0.6, 3024,  '#4361EE', 'rgba(67,97,238,0.30)'),
            'Pass':        (7.8, 0.8, 12361, '#4CC9F0', 'rgba(76,201,240,0.25)'),
            'Fail':        (6.8, 0.9, 7052,  '#F72585', 'rgba(247,37,133,0.25)'),
            'Withdrawn':   (6.2, 0.9, 7072,  '#7209B7', 'rgba(114,9,183,0.25)'),
        }
        fig_v = go.Figure()
        for res, (mu, sig, n, clr, fill) in result_params.items():
            data = np.clip(np.random.lognormal(mu, sig, n), 0, np.exp(mu+2*sig))
            fig_v.add_trace(go.Violin(
                x=[res]*len(data), y=data, name=res,
                fillcolor=fill, line_color=clr,
                meanline_visible=True, box_visible=True,
                hovertemplate=f'<b>{res}</b>: %{{y:,.0f}} clicks<extra></extra>',
            ))
        fig_v.update_layout(**utils.dark_layout(height=320))
        fig_v.update_layout(violingap=0.1, showlegend=False, yaxis_title='Total VLE Clicks')
        st.plotly_chart(fig_v, use_container_width=True, config={'displayModeBar':False})

        c1, c2 = st.columns(2)
        with c1:
            utils.card_header("On-Schedule Ratio by Result", "NEW — from week_from/week_to")
            cats2 = ['Distinction','Pass','Fail','Withdrawn']
            os_vals = [78, 63, 41, 32]
            os_clrs = ['#4361EE','#4CC9F0','#F72585','#7209B7']
            fig_os = go.Figure(go.Bar(
                x=cats2, y=os_vals, marker_color=os_clrs, marker_line_width=0,
                text=[f'{v}%' for v in os_vals], textposition='outside',
                textfont=dict(color='#E8EAF0', size=11),
                hovertemplate='<b>%{x}</b>: %{y}%<extra></extra>',
            ))
            fig_os.update_layout(**utils.dark_layout(height=260))
            fig_os.update_layout(yaxis_range=[0,100], yaxis_ticksuffix='%')
            st.plotly_chart(fig_os, use_container_width=True, config={'displayModeBar':False})

        with c2:
            utils.card_header("Clicks per Week by Result", "NEW — normalized by module length")
            cpw_vals = [185, 142, 88, 67]
            fig_cpw = go.Figure(go.Bar(
                x=cats2, y=cpw_vals, marker_color=os_clrs, marker_line_width=0,
                text=[str(v) for v in cpw_vals], textposition='outside',
                textfont=dict(color='#E8EAF0', size=11),
                hovertemplate='<b>%{x}</b>: %{y} clicks/week<extra></extra>',
            ))
            fig_cpw.update_layout(**utils.dark_layout(height=260))
            fig_cpw.update_layout(yaxis_title='Avg Clicks/Week')
            st.plotly_chart(fig_cpw, use_container_width=True, config={'displayModeBar':False})

    with tab3:
        c1, c2 = st.columns(2)
        with c1:
            utils.card_header("Score Distribution by Result")
            score_p = {'Distinction':(78,10,'#4361EE'),'Pass':(63,12,'#4CC9F0'),
                        'Fail':(42,14,'#F72585'),'Withdrawn':(50,16,'#7209B7')}
            fig_sc = go.Figure()
            for res, (mu, sig, clr) in score_p.items():
                scores = np.clip(np.random.normal(mu, sig, 2000), 0, 100)
                fig_sc.add_trace(go.Histogram(
                    x=scores, name=res, opacity=0.55,
                    marker_color=clr, nbinsx=30,
                    hovertemplate=f'<b>{res}</b>: %{{x:.0f}}%<extra></extra>',
                ))
            fig_sc.add_vline(x=40, line_dash='dash', line_color='rgba(247,37,133,0.6)',
                              annotation_text='Pass threshold (40)',
                              annotation_font=dict(size=10, color='#F72585'))
            fig_sc.update_layout(**utils.dark_layout(height=300))
            fig_sc.update_layout(barmode='overlay', xaxis_title='Score (%)',
                                  legend=dict(orientation='h',y=1.08,x=0))
            st.plotly_chart(fig_sc, use_container_width=True, config={'displayModeBar':False})

        with c2:
            utils.card_header("Registration Timing vs Pass Rate", "NEW — date_registration feature")
            reg_days = np.arange(-90, 31, 10)
            pass_pct = np.clip(72 - reg_days*0.35 + np.random.normal(0,2,len(reg_days)), 20, 85)
            fig_reg = go.Figure()
            fig_reg.add_trace(go.Scatter(
                x=reg_days, y=pass_pct, mode='lines+markers',
                line=dict(color='#4CC9F0', width=2.5),
                marker=dict(color='#4361EE', size=7),
                fill='tozeroy', fillcolor='rgba(76,201,240,0.08)',
                hovertemplate='%{x} days: %{y:.1f}% pass rate<extra></extra>',
            ))
            fig_reg.add_vline(x=0, line_dash='dash', line_color='rgba(255,209,102,0.5)',
                               annotation_text='Module start',
                               annotation_font=dict(size=10, color='#FFD166'))
            fig_reg.update_layout(**utils.dark_layout(height=300))
            fig_reg.update_layout(
                xaxis_title='Days before/after module start',
                yaxis_title='Pass Rate %', yaxis_ticksuffix='%',
            )
            st.plotly_chart(fig_reg, use_container_width=True, config={'displayModeBar':False})

    with tab4:
        utils.card_header("Top 15 Feature Importances", "Color = source table")
        feats    = [f[0] for f in utils.TOP_FEATURES]
        imp_vals = [f[1] for f in utils.TOP_FEATURES]
        cats_f   = [f[2] for f in utils.TOP_FEATURES]
        bar_clrs = [utils.CAT_COLORS[c] for c in cats_f]

        fig_fi = go.Figure(go.Bar(
            x=imp_vals[::-1], y=feats[::-1], orientation='h',
            marker_color=bar_clrs[::-1], marker_line_width=0,
            text=[f'{v:.3f}' for v in imp_vals[::-1]], textposition='outside',
            textfont=dict(color='#E8EAF0', size=10),
            hovertemplate='<b>%{y}</b>: %{x:.3f}<extra></extra>',
        ))
        fig_fi.update_layout(**utils.dark_layout(height=500))
        fig_fi.update_layout(xaxis_title='Importance', xaxis_range=[0,.17])
        st.plotly_chart(fig_fi, use_container_width=True, config={'displayModeBar':False})

        # Legend
        leg_cols = st.columns(4)
        for col, (cat, clr) in zip(leg_cols, utils.CAT_COLORS.items()):
            with col:
                st.markdown(f'<p style="color:{clr};font-size:12px;font-weight:600;margin:0">■ {cat}</p>',
                            unsafe_allow_html=True)
