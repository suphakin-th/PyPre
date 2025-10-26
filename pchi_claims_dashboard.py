"""
PCHI Claims Dashboard
A comprehensive dashboard for analyzing insurance claims data from 2020 to now
"""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
from datetime import datetime
import numpy as np

# Page configuration
st.set_page_config(
    page_title="PCHI Claims Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    .stMetric {
        background-color: white;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    h1 {
        color: #1f77b4;
        padding-bottom: 10px;
        border-bottom: 3px solid #1f77b4;
    }
    h2 {
        color: #2ca02c;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Cache data loading
@st.cache_data
def load_data(filepath):
    """Load and preprocess the claims data"""
    df = pd.read_csv(filepath)

    # Convert date columns
    date_columns = ['POLICY EFF DATE', 'POLICY EXP DATE', 'SICK/FROM', 'SICK/TO',
                   'RECEIPT/DT', 'PAYDATE', 'CHQDATE', 'CREATE_DATE', 'UPDATE_DATE']
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')

    # Convert numeric columns
    numeric_columns = ['INCURRED', 'APPROVED', 'CLAIMED', 'OUTSTANDING',
                      'DED_AMT', 'COPAY_AMT', 'MANUAL_REJECTED_AMT']
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Add derived columns
    if 'PAYDATE' in df.columns:
        df['YEAR'] = df['PAYDATE'].dt.year
        df['MONTH'] = df['PAYDATE'].dt.month
        df['QUARTER'] = df['PAYDATE'].dt.quarter
        df['YEAR_MONTH'] = df['PAYDATE'].dt.to_period('M').astype(str)

    return df

# Title and header
st.title("📊 PCHI Claims Analytics Dashboard")
st.markdown("### Comprehensive Insurance Claims Analysis (2020 - Present)")

# File path
DATA_PATH = "data/uploads/20251024 PCHI Claim summary 2020 - now.csv"

# Load data with progress bar
with st.spinner("Loading claims data... This may take a moment for large files."):
    try:
        df = load_data(DATA_PATH)
        st.success(f"✅ Successfully loaded {len(df):,} claims records")
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        st.stop()

# Sidebar filters
st.sidebar.header("🔍 Filters")

# Year filter
if 'YEAR' in df.columns:
    years = sorted(df['YEAR'].dropna().unique())
    selected_years = st.sidebar.multiselect(
        "Select Year(s)",
        options=years,
        default=years
    )
    df_filtered = df[df['YEAR'].isin(selected_years)]
else:
    df_filtered = df.copy()

# Claim Status filter
if 'CLAIM_STATUS' in df.columns:
    statuses = df['CLAIM_STATUS'].unique()
    selected_statuses = st.sidebar.multiselect(
        "Claim Status",
        options=statuses,
        default=statuses
    )
    df_filtered = df_filtered[df_filtered['CLAIM_STATUS'].isin(selected_statuses)]

# Business Unit filter
if 'BU' in df.columns:
    bus = sorted(df['BU'].dropna().unique())
    selected_bu = st.sidebar.multiselect(
        "Business Unit",
        options=bus,
        default=bus
    )
    df_filtered = df_filtered[df_filtered['BU'].isin(selected_bu)]

# Product filter
if 'PRODUCT' in df.columns:
    products = sorted(df['PRODUCT'].dropna().unique())
    selected_products = st.sidebar.multiselect(
        "Product Type",
        options=products,
        default=products[:5] if len(products) > 5 else products
    )
    df_filtered = df_filtered[df_filtered['PRODUCT'].isin(selected_products)]

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Filtered Records:** {len(df_filtered):,} / {len(df):,}")

# ==================== KEY METRICS ====================
st.header("📈 Key Performance Indicators")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    total_claims = len(df_filtered)
    st.metric("Total Claims", f"{total_claims:,}")

with col2:
    total_incurred = df_filtered['INCURRED'].sum()
    st.metric("Total Incurred", f"฿{total_incurred:,.0f}")

with col3:
    total_approved = df_filtered['APPROVED'].sum()
    st.metric("Total Approved", f"฿{total_approved:,.0f}")

with col4:
    total_claimed = df_filtered['CLAIMED'].sum()
    st.metric("Total Claimed", f"฿{total_claimed:,.0f}")

with col5:
    approval_rate = (df_filtered['CLAIM_STATUS'] == 'Accept').sum() / len(df_filtered) * 100 if len(df_filtered) > 0 else 0
    st.metric("Approval Rate", f"{approval_rate:.1f}%")

# ==================== CHARTS ROW 1 ====================
st.header("📊 Claims Analysis")

col1, col2 = st.columns(2)

with col1:
    # Claims Trend Over Time
    if 'YEAR_MONTH' in df_filtered.columns:
        monthly_claims = df_filtered.groupby('YEAR_MONTH').agg({
            'CL_NO': 'count',
            'INCURRED': 'sum',
            'APPROVED': 'sum'
        }).reset_index()

        fig = make_subplots(specs=[[{"secondary_y": True}]])

        fig.add_trace(
            go.Scatter(x=monthly_claims['YEAR_MONTH'], y=monthly_claims['CL_NO'],
                      name="Claim Count", line=dict(color='#1f77b4', width=3)),
            secondary_y=False
        )

        fig.add_trace(
            go.Scatter(x=monthly_claims['YEAR_MONTH'], y=monthly_claims['APPROVED'],
                      name="Approved Amount", line=dict(color='#2ca02c', width=2)),
            secondary_y=True
        )

        fig.update_xaxes(title_text="Month")
        fig.update_yaxes(title_text="Number of Claims", secondary_y=False)
        fig.update_yaxes(title_text="Approved Amount (฿)", secondary_y=True)
        fig.update_layout(
            title="Claims Trend Over Time",
            hovermode='x unified',
            height=400
        )

        st.plotly_chart(fig, use_container_width=True)

with col2:
    # Claim Status Distribution
    if 'CLAIM_STATUS' in df_filtered.columns:
        status_counts = df_filtered['CLAIM_STATUS'].value_counts()

        fig = go.Figure(data=[go.Pie(
            labels=status_counts.index,
            values=status_counts.values,
            hole=0.4,
            marker=dict(colors=['#2ca02c', '#d62728']),
            textinfo='label+percent+value',
            textfont_size=14
        )])

        fig.update_layout(
            title="Claim Status Distribution",
            height=400,
            showlegend=True
        )

        st.plotly_chart(fig, use_container_width=True)

# ==================== CHARTS ROW 2 ====================
col1, col2 = st.columns(2)

with col1:
    # Top 10 Providers by Claim Amount
    if 'PROVIDER' in df_filtered.columns:
        top_providers = df_filtered.groupby('PROVIDER')['APPROVED'].sum().nlargest(10).reset_index()

        fig = px.bar(
            top_providers,
            x='APPROVED',
            y='PROVIDER',
            orientation='h',
            title="Top 10 Providers by Approved Amount",
            labels={'APPROVED': 'Approved Amount (฿)', 'PROVIDER': 'Provider'},
            color='APPROVED',
            color_continuous_scale='Blues'
        )

        fig.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

with col2:
    # Claims by Business Unit
    if 'BU' in df_filtered.columns:
        bu_analysis = df_filtered.groupby('BU').agg({
            'CL_NO': 'count',
            'APPROVED': 'sum'
        }).reset_index()
        bu_analysis.columns = ['BU', 'Claim Count', 'Approved Amount']

        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=bu_analysis['BU'],
            y=bu_analysis['Claim Count'],
            name='Claim Count',
            marker_color='#1f77b4'
        ))

        fig.update_layout(
            title="Claims by Business Unit",
            xaxis_title="Business Unit",
            yaxis_title="Number of Claims",
            height=400,
            showlegend=True
        )

        st.plotly_chart(fig, use_container_width=True)

# ==================== CHARTS ROW 3 ====================
col1, col2 = st.columns(2)

with col1:
    # Age Distribution of Claimants
    if 'AGE' in df_filtered.columns:
        age_bins = [0, 18, 30, 40, 50, 60, 100]
        age_labels = ['0-18', '19-30', '31-40', '41-50', '51-60', '60+']
        df_filtered['AGE_GROUP'] = pd.cut(df_filtered['AGE'], bins=age_bins, labels=age_labels)

        age_dist = df_filtered['AGE_GROUP'].value_counts().sort_index()

        fig = px.bar(
            x=age_dist.index,
            y=age_dist.values,
            title="Claims by Age Group",
            labels={'x': 'Age Group', 'y': 'Number of Claims'},
            color=age_dist.values,
            color_continuous_scale='Greens'
        )

        fig.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

with col2:
    # Gender Distribution
    if 'Gender' in df_filtered.columns:
        gender_dist = df_filtered['Gender'].value_counts()

        fig = go.Figure(data=[go.Bar(
            x=gender_dist.index,
            y=gender_dist.values,
            marker_color=['#ff69b4', '#4169e1'],
            text=gender_dist.values,
            textposition='outside'
        )])

        fig.update_layout(
            title="Claims by Gender",
            xaxis_title="Gender",
            yaxis_title="Number of Claims",
            height=400,
            showlegend=False
        )

        st.plotly_chart(fig, use_container_width=True)

# ==================== CHARTS ROW 4 ====================
st.header("💰 Financial Analysis")

col1, col2 = st.columns(2)

with col1:
    # Claim Amount Distribution
    fig = go.Figure()

    fig.add_trace(go.Box(
        y=df_filtered['APPROVED'],
        name='Approved',
        marker_color='#2ca02c'
    ))

    fig.add_trace(go.Box(
        y=df_filtered['INCURRED'],
        name='Incurred',
        marker_color='#1f77b4'
    ))

    fig.add_trace(go.Box(
        y=df_filtered['CLAIMED'],
        name='Claimed',
        marker_color='#ff7f0e'
    ))

    fig.update_layout(
        title="Claim Amount Distribution (Box Plot)",
        yaxis_title="Amount (฿)",
        height=400,
        showlegend=True
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Approval vs Incurred Scatter
    sample_data = df_filtered.sample(min(1000, len(df_filtered)))

    fig = px.scatter(
        sample_data,
        x='INCURRED',
        y='APPROVED',
        color='CLAIM_STATUS',
        title="Approved vs Incurred Amount (Sample)",
        labels={'INCURRED': 'Incurred Amount (฿)', 'APPROVED': 'Approved Amount (฿)'},
        color_discrete_map={'Accept': '#2ca02c', 'Reject': '#d62728'},
        opacity=0.6
    )

    # Add diagonal line
    max_val = max(sample_data['INCURRED'].max(), sample_data['APPROVED'].max())
    fig.add_trace(go.Scatter(
        x=[0, max_val],
        y=[0, max_val],
        mode='lines',
        line=dict(color='gray', dash='dash'),
        name='Equal Line',
        showlegend=True
    ))

    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

# ==================== BENEFIT TYPE ANALYSIS ====================
st.header("🏥 Benefit Type Analysis")

if 'BEN_TYPE_DESC' in df_filtered.columns:
    col1, col2 = st.columns(2)

    with col1:
        # Top Benefit Types by Count
        top_benefits = df_filtered['BEN_TYPE_DESC'].value_counts().head(10)

        fig = px.bar(
            x=top_benefits.values,
            y=top_benefits.index,
            orientation='h',
            title="Top 10 Benefit Types by Claim Count",
            labels={'x': 'Number of Claims', 'y': 'Benefit Type'},
            color=top_benefits.values,
            color_continuous_scale='Reds'
        )

        fig.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Top Benefit Types by Amount
        benefit_amounts = df_filtered.groupby('BEN_TYPE_DESC')['APPROVED'].sum().nlargest(10)

        fig = px.bar(
            x=benefit_amounts.values,
            y=benefit_amounts.index,
            orientation='h',
            title="Top 10 Benefit Types by Approved Amount",
            labels={'x': 'Approved Amount (฿)', 'y': 'Benefit Type'},
            color=benefit_amounts.values,
            color_continuous_scale='Purples'
        )

        fig.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

# ==================== DISTRIBUTION CHANNEL ANALYSIS ====================
st.header("📢 Distribution Channel Analysis")

if 'DISTRIBUTION' in df_filtered.columns:
    col1, col2 = st.columns(2)

    with col1:
        # Distribution Channel Performance
        dist_analysis = df_filtered.groupby('DISTRIBUTION').agg({
            'CL_NO': 'count',
            'APPROVED': 'sum',
            'INCURRED': 'sum'
        }).reset_index()
        dist_analysis.columns = ['Distribution', 'Claims', 'Approved', 'Incurred']

        fig = px.bar(
            dist_analysis,
            x='Distribution',
            y='Claims',
            title="Claims by Distribution Channel",
            color='Approved',
            labels={'Claims': 'Number of Claims', 'Distribution': 'Channel'},
            color_continuous_scale='Viridis'
        )

        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Distribution Channel - Approval Rate
        dist_approval = df_filtered.groupby('DISTRIBUTION')['CLAIM_STATUS'].apply(
            lambda x: (x == 'Accept').sum() / len(x) * 100
        ).reset_index()
        dist_approval.columns = ['Distribution', 'Approval Rate']

        fig = px.bar(
            dist_approval,
            x='Distribution',
            y='Approval Rate',
            title="Approval Rate by Distribution Channel",
            labels={'Approval Rate': 'Approval Rate (%)', 'Distribution': 'Channel'},
            color='Approval Rate',
            color_continuous_scale='RdYlGn'
        )

        fig.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

# ==================== DATA QUALITY & INSIGHTS ====================
st.header("🔍 Data Insights & Statistics")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("📊 Summary Statistics")
    st.dataframe(
        df_filtered[['INCURRED', 'APPROVED', 'CLAIMED', 'AGE']].describe().round(2),
        use_container_width=True
    )

with col2:
    st.subheader("🏆 Top Providers")
    top_5_providers = df_filtered.groupby('PROVIDER')['APPROVED'].sum().nlargest(5)
    st.dataframe(
        pd.DataFrame({
            'Provider': top_5_providers.index,
            'Approved Amount': top_5_providers.values.round(2)
        }).reset_index(drop=True),
        use_container_width=True
    )

with col3:
    st.subheader("📈 Monthly Averages")
    if 'YEAR_MONTH' in df_filtered.columns:
        monthly_avg = df_filtered.groupby('YEAR_MONTH')['APPROVED'].mean().round(2)
        st.dataframe(
            pd.DataFrame({
                'Month': monthly_avg.index[-5:],
                'Avg Approved': monthly_avg.values[-5:]
            }).reset_index(drop=True),
            use_container_width=True
        )

# ==================== DATA TABLE ====================
st.header("📋 Raw Data Explorer")

# Column selector
all_columns = df_filtered.columns.tolist()
default_columns = ['CL_NO', 'CLAIM_STATUS', 'PROVIDER', 'PAYDATE', 'INCURRED', 'APPROVED', 'CLAIMED', 'BEN_TYPE_DESC', 'DIAGNOSIS_DETAILS']
selected_columns = st.multiselect(
    "Select columns to display:",
    options=all_columns,
    default=[col for col in default_columns if col in all_columns]
)

if selected_columns:
    # Row limit
    row_limit = st.slider("Number of rows to display:", 10, 1000, 100)

    st.dataframe(
        df_filtered[selected_columns].head(row_limit),
        use_container_width=True,
        height=400
    )

    # Download button
    csv = df_filtered[selected_columns].to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=csv,
        file_name=f"pchi_claims_filtered_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>📊 PCHI Claims Dashboard | Data from 2020 to Present</p>
        <p>Last Updated: {}</p>
    </div>
""".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')), unsafe_allow_html=True)
