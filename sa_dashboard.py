import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime

# Set up the page with wider layout and better title
st.set_page_config(
    page_title="SA Digital Resilience Dashboard", 
    page_icon="📊", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
    }
    .positive-metric {
        border-left: 4px solid #2ecc71;
    }
    .negative-metric {
        border-left: 4px solid #e74c3c;
    }
    .section-header {
        color: #2c3e50;
        border-bottom: 2px solid #3498db;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Load your pre-cleaned data with better error handling
@st.cache_data
def load_data():
    try:
        ict_df = pd.read_csv('analysis_results/cleaned_ict_south_africa.csv')
        cyb_df = pd.read_csv('analysis_results/cleaned_cybersecurity_south_africa.csv')
        
        # Ensure proper data types
        ict_df['Year'] = pd.to_numeric(ict_df['Year'], errors='coerce')
        cyb_df['Year'] = pd.to_numeric(cyb_df['Year'], errors='coerce')
        ict_df['Value'] = pd.to_numeric(ict_df['Value'], errors='coerce')
        cyb_df['Value'] = pd.to_numeric(cyb_df['Value'], errors='coerce')
        
        return ict_df, cyb_df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame(), pd.DataFrame()

ict_long, cyb_long = load_data()

# Sidebar for navigation and info
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/a/af/Flag_of_South_Africa.svg/1200px-Flag_of_South_Africa.svg.png", 
             width=100)
    st.title("SA Digital Dashboard")
    st.markdown("---")
    
    st.subheader("Project Info")
    st.info("""
    **Course:** NDTA631 - Data Analysis & Visualization
    **Team:** Hope, Gomolemo, Gift, Keotshepile, Ikho
    **Data Source:** World Bank Data360
    """)
    
    st.subheader("Key Insights")
    st.success("📈 Digital adoption grew from 5% to 75% (2000-2024)")
    st.warning("🛡️ Capacity development score declined by 2.54 points")
    st.error("📊 Limited cybersecurity data prevents correlation analysis")
    
    st.markdown("---")
    st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

# Main content
st.markdown('<h1 class="main-header">South Africa Digital Resilience Dashboard</h1>', unsafe_allow_html=True)

# Create tabs for organization
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🏠 Overview", "📶 ICT Growth", "🛡️ Cyber Readiness", "📊 Gap Analysis", "🎯 Recommendations"])

with tab1:
    st.markdown('<h2 class="section-header">Executive Summary</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### Research Question:
        **"Is South Africa's cybersecurity infrastructure keeping up with its growing digital footprint?"**
        
        ### Key Findings:
        - 🚀 **Explosive Digital Growth**: Internet penetration increased from 5.35% (2000) to ~75% (2024)
        - 📱 **Mobile-First Revolution**: 72.3 mobile broadband subscriptions per 100 people vs 5.3 fixed broadband
        - 🛡️ **Mixed Cybersecurity Results**: Overall improvement but concerning decline in capacity development
        - ⚠️ **Data Availability Gap**: Cybersecurity data only available for 2020 & 2024, limiting analysis
        """)
    
    with col2:
        # Quick stats card
        st.markdown("### 🎯 At a Glance")
        st.metric("Internet Penetration (2024)", "75%", "+69.65% since 2000")
        st.metric("Mobile Broadband", "72.3/100", "Leading technology")
        st.metric("Cybersecurity Score", "86.25/100", "+7.79 since 2020")
        st.metric("Capacity Development", "12.83/20", "-2.54 since 2020", delta_color="inverse")
    
    # Key Metrics in a grid
    st.markdown('<h3 class="section-header">Performance Indicators</h3>', unsafe_allow_html=True)
    
    metrics_col1, metrics_col2, metrics_col3, metrics_col4 = st.columns(4)
    
    with metrics_col1:
        st.markdown('<div class="metric-card positive-metric">', unsafe_allow_html=True)
        st.metric("📊 Internet Users (2024)", "75%", "+8.2% CAGR")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with metrics_col2:
        st.markdown('<div class="metric-card positive-metric">', unsafe_allow_html=True)
        st.metric("📱 Mobile Penetration", "179.3/100", "Multiple SIM adoption")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with metrics_col3:
        st.markdown('<div class="metric-card positive-metric">', unsafe_allow_html=True)
        st.metric("🛡️ GCI Score", "86.25/100", "Good to Excellent")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with metrics_col4:
        st.markdown('<div class="metric-card negative-metric">', unsafe_allow_html=True)
        st.metric("👨‍💻 Capacity Development", "12.83/20", "Trending down")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Main overview chart
    st.markdown('<h3 class="section-header">Digital Transformation Timeline</h3>', unsafe_allow_html=True)
    
    # Create a timeline of key milestones
    timeline_data = {
        'Year': [2000, 2005, 2010, 2015, 2020, 2024],
        'Event': [
            '5.35% Internet Penetration',
            'Early Mobile Adoption',
            'Accelerated Growth Phase',
            'Crossed 50% Internet Users',
            'First GCI Measurement (78.46)',
            'Current State: 75% Penetration\nGCI: 86.25'
        ],
        'Value': [5.35, 15, 35, 55, 78.46, 86.25]
    }
    
    timeline_df = pd.DataFrame(timeline_data)
    fig_timeline = px.scatter(timeline_df, x='Year', y='Value', text='Event',
                             title='South Africa Digital Journey: Key Milestones (2000-2024)',
                             size=[10, 15, 20, 25, 30, 35], size_max=40)
    fig_timeline.update_traces(textposition='top center', marker=dict(color='#e74c3c'))
    fig_timeline.update_layout(showlegend=False, height=400)
    st.plotly_chart(fig_timeline, use_container_width=True)

with tab2:
    st.markdown('<h2 class="section-header">ICT Infrastructure & Adoption Analysis</h2>', unsafe_allow_html=True)
    
    # Indicator selector
    col1, col2 = st.columns([2, 1])
    
    with col1:
        ict_indicators = ict_long['INDICATOR_LABEL'].unique()
        selected_indicator = st.selectbox("📊 Select ICT Indicator:", ict_indicators)
    
    with col2:
        show_stats = st.checkbox("📈 Show Statistics", value=True)
    
    # Selected indicator chart
    chart_df = ict_long[ict_long['INDICATOR_LABEL'] == selected_indicator]
    
    if not chart_df.empty:
        fig = px.line(chart_df, x='Year', y='Value', 
                     title=f'{selected_indicator} Trend (2000-2024)',
                     markers=True, line_shape='spline')
        fig.update_layout(hovermode='x unified', height=500)
        st.plotly_chart(fig, use_container_width=True)
        
        if show_stats:
            # Calculate statistics
            growth = ((chart_df['Value'].iloc[-1] - chart_df['Value'].iloc[0]) / chart_df['Value'].iloc[0]) * 100
            avg_value = chart_df['Value'].mean()
            
            stat_col1, stat_col2, stat_col3 = st.columns(3)
            with stat_col1:
                st.metric("📈 Total Growth", f"{growth:.1f}%")
            with stat_col2:
                st.metric("📊 Average Value", f"{avg_value:.1f}")
            with stat_col3:
                st.metric("📅 Time Span", f"{int(chart_df['Year'].max() - chart_df['Year'].min())} years")
    
    # Comparative analysis
    st.markdown('<h3 class="section-header">Comparative Analysis</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Mobile vs Fixed broadband
        try:
            mobile_df = ict_long[ict_long['INDICATOR_LABEL'] == 'Active mobile-broadband subscriptions per 100 inhabitants (ITU)']
            fixed_df = ict_long[ict_long['INDICATOR_LABEL'] == 'Fixed-broadband subscriptions per 100 inhabitants (ITU)']
            
            fig_compare = go.Figure()
            fig_compare.add_trace(go.Scatter(x=mobile_df['Year'], y=mobile_df['Value'], 
                                           mode='lines+markers', name='Mobile Broadband', 
                                           line=dict(color='#3498db', width=3)))
            fig_compare.add_trace(go.Scatter(x=fixed_df['Year'], y=fixed_df['Value'], 
                                           mode='lines+markers', name='Fixed Broadband', 
                                           line=dict(color='#e74c3c', width=3)))
            fig_compare.update_layout(title="📶 Mobile vs Fixed Broadband Penetration",
                                    yaxis_title="Subscriptions per 100 inhabitants",
                                    height=400)
            st.plotly_chart(fig_compare, use_container_width=True)
        except:
            st.warning("Broadband comparison data not available")
    
    with col2:
        # Internet adoption growth curve
        try:
            internet_df = ict_long[ict_long['INDICATOR_LABEL'] == 'Percentage of individuals using the internet (ITU)']
            fig_growth = px.area(internet_df, x='Year', y='Value',
                               title='🌐 Internet Adoption Growth Curve',
                               color_discrete_sequence=['#27ae60'])
            fig_growth.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig_growth, use_container_width=True)
        except:
            st.warning("Internet adoption data not available")

with tab3:
    st.markdown('<h2 class="section-header">Cybersecurity Readiness Assessment</h2>', unsafe_allow_html=True)
    
    if not cyb_long.empty:
        # Cybersecurity score trend
        gci_df = cyb_long[cyb_long['INDICATOR_LABEL'] == 'Global Cybersecurity Index - Overall Score (ITU GCI)']
        
        if not gci_df.empty:
            fig_gci = px.line(gci_df, x='Year', y='Value', 
                            title='🛡️ Global Cybersecurity Index Trend',
                            markers=True, line_shape='linear')
            fig_gci.update_layout(yaxis_range=[0, 100], height=400)
            st.plotly_chart(fig_gci, use_container_width=True)
        
        # Component analysis
        st.markdown('<h3 class="section-header">2024 Cybersecurity Component Analysis</h3>', unsafe_allow_html=True)
        
        cyb_2024 = cyb_long[cyb_long['Year'] == 2024]
        main_components = [
            'Cooperative Score - CS (ITU GCI)',
            'Technical Score - TS (ITU GCI)',
            'Organizational Score - OS (ITU GCI)',
            'Capacity Development Score - CDS (ITU GCI)'
        ]
        
        available_components = [comp for comp in main_components if comp in cyb_2024['INDICATOR_LABEL'].values]
        
        if available_components:
            cyb_2024_components = cyb_2024[cyb_2024['INDICATOR_LABEL'].isin(available_components)]
            
            # Create radar chart for components
            fig_radar = go.Figure()
            
            fig_radar.add_trace(go.Scatterpolar(
                r=cyb_2024_components['Value'].values,
                theta=[comp.split(' - ')[0] for comp in available_components],
                fill='toself',
                name='2024 Scores',
                line_color='#3498db'
            ))
            
            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, 20])
                ),
                showlegend=True,
                title="Cybersecurity Capability Radar (2024)",
                height=500
            )
            
            st.plotly_chart(fig_radar, use_container_width=True)
            
            # Bar chart comparison
            fig_components = px.bar(cyb_2024_components, x='INDICATOR_LABEL', y='Value',
                                  title='📊 Cybersecurity Component Scores (2024)',
                                  color='Value', color_continuous_scale='Viridis')
            fig_components.update_layout(height=400)
            st.plotly_chart(fig_components, use_container_width=True)

with tab4:
    st.markdown('<h2 class="section-header">The Data Gap Analysis</h2>', unsafe_allow_html=True)
    
    # Create the data disparity visualization
    fig_gap = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Internet data
    internet_df = ict_long[ict_long['INDICATOR_LABEL'] == 'Percentage of individuals using the internet (ITU)']
    fig_gap.add_trace(
        go.Scatter(x=internet_df['Year'], y=internet_df['Value'], 
                  name="Internet Users (%)", line=dict(color='#3498db', width=3)),
        secondary_y=False,
    )
    
    # GCI data if available
    try:
        gci_df = cyb_long[cyb_long['INDICATOR_LABEL'] == 'Global Cybersecurity Index - Overall Score (ITU GCI)']
        fig_gap.add_trace(
            go.Scatter(x=gci_df['Year'], y=gci_df['Value'], name="GCI Score", 
                      mode='markers+lines', marker=dict(size=15, color='#e74c3c'), 
                      line=dict(dash='dash', color='#e74c3c', width=2)),
            secondary_y=True,
        )
    except:
        pass
    
    fig_gap.update_layout(
        title_text="⚠️ The Data Disconnect: Rich ICT History vs. Limited Cyber Data",
        hovermode="x unified",
        height=500,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    fig_gap.update_xaxes(title_text="Year")
    fig_gap.update_yaxes(title_text="<b>Internet Users</b> (%)", secondary_y=False)
    fig_gap.update_yaxes(title_text="<b>GCI Score</b>", secondary_y=True, range=[0, 100])
    
    st.plotly_chart(fig_gap, use_container_width=True)
    
    # Explanation
    col1, col2 = st.columns(2)
    
    with col1:
        st.error("""
        ## 🚫 Statistical Limitation
        **Correlation Analysis Failed:** `NaN` result
        
        **Reason:** You cannot calculate a valid statistical correlation with only two data points (2020 & 2024).
        
        This isn't an error - it's mathematical truth. The data needed for a definitive answer doesn't exist yet.
        """)
    
    with col2:
        st.success("""
        ## ✅ Framework Achievement
        **What we built:**
        - Complete ETL pipeline ✅
        - Advanced visualization system ✅  
        - Database integration ✅
        - Analytical framework ✅
        
        **The engine is ready.** Just needs more data fuel.
        """)
    
    # Data availability heatmap
    st.markdown('<h3 class="section-header">Data Availability Matrix</h3>', unsafe_allow_html=True)
    
    # Create a simple availability matrix
    availability_data = {
        'Domain': ['ICT Indicators', 'Cybersecurity'],
        'Time Span': ['2000-2024 (25 years)', '2020, 2024 (2 years)'],
        'Data Points': ['600+', '60'],
        'Status': ['📊 Rich History', '⚠️ Limited Snapshot']
    }
    
    availability_df = pd.DataFrame(availability_data)
    st.dataframe(availability_df, use_container_width=True, hide_index=True)

with tab5:
    st.markdown('<h2 class="section-header">Strategic Recommendations</h2>', unsafe_allow_html=True)
    
    # Recommendations in cards
    rec_col1, rec_col2, rec_col3 = st.columns(3)
    
    with rec_col1:
        st.markdown('<div class="metric-card positive-metric">', unsafe_allow_html=True)
        st.subheader("🚨 Immediate Actions")
        st.markdown("""
        - **Launch mobile security awareness campaigns**
        - **Establish public-private cybersecurity partnerships**
        - **Implement tax incentives for cyber training**
        - **Address capacity development decline**
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with rec_col2:
        st.markdown('<div class="metric-card positive-metric">', unsafe_allow_html=True)
        st.subheader("📅 Medium-term (6-18 months)")
        st.markdown("""
        - **Integrate cyber curriculum in education**
        - **Invest in secure broadband infrastructure**
        - **Create sector-specific CERT teams**
        - **Improve data collection consistency**
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with rec_col3:
        st.markdown('<div class="metric-card positive-metric">', unsafe_allow_html=True)
        st.subheader("🎯 Long-term Strategy")
        st.markdown("""
        - **National cybersecurity innovation fund**
        - **Develop African-context solutions**
        - **Position as regional cyber hub**
        - **Annual cyber readiness reporting**
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Quantitative targets
    st.markdown('<h3 class="section-header">Quantitative Targets</h3>', unsafe_allow_html=True)
    
    targets_col1, targets_col2, targets_col3, targets_col4 = st.columns(4)
    
    with targets_col1:
        st.metric("🎯 Target 1", "Capacity Score 18/20", "By 2026")
    
    with targets_col2:
        st.metric("🎯 Target 2", "90% Internet Penetration", "By 2027")
    
    with targets_col3:
        st.metric("🎯 Target 3", "95% Security Awareness", "By 2027")
    
    with targets_col4:
        st.metric("🎯 Target 4", "40% Incident Reduction", "Through training")
    
    # Call to action
    st.markdown("---")
    st.success("""
    ## 🚀 Next Steps
    **1.** Advocate for consistent cybersecurity data collection  
    **2.** Implement this dashboard for ongoing monitoring  
    **3.** Focus investment on human capital development  
    **4.** Use this framework for regional comparative analysis
    """)

# Footer
st.markdown("---")
st.caption("""
**NDTA631 - Group Assignment** | Hope Mnguni, Gomolemo Walaza, Gift Nemakonde, Keotshepile Modise, Ikho Nogemane
| Data Source: World Bank Data360 
""")