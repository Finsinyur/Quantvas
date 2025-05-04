import streamlit as st
from utils.data_loader import load_data
from utils.futures_engine import futures_adjustment, get_performance_metrics
import plotly.express as px
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

st.title("1️⃣ Continuous-First futures")
df = load_data()

# --- Sidebar Inputs ---
st.sidebar.header("🔧 Filters")

# Product selector
products = sorted(df['exch_code'].unique())
selected_product = st.sidebar.selectbox("Ticker:", products, index=products.index("SGP") if "SGP" in products else 0)


# Adjustment type
options = [None, 'Backward Adjustment', 'Forward Adjustment']
selected_adjustment = st.sidebar.selectbox("Select Adjustment Algorithm:", options)

# Date range slider
min_date = df['date'].min()
max_date = df['date'].max()
start_date, end_date = st.sidebar.slider(
    "Date Range:",
    min_value=min_date,
    max_value=max_date,
    value=(min_date, max_date)
)

# --- Data Filtering ---
mask = (
    (df['exch_code'] == selected_product) &
    (df['date'] >= start_date) &
    (df['date'] <= end_date)
)
filtered_df = df[mask]

# --- Plot ---
if filtered_df.empty:
    st.warning("No data for the selected filters.")
else:
    plot_df = futures_adjustment(filtered_df, selected_product, selected_adjustment)
    fig = px.line(
        plot_df,
        x='date',
        y='daily_settle_price',
        color='label',
        hover_data=['date', 'label', 'daily_settle_price'],
        title='Futures time series: {}'.format(selected_product)
    )

    fig.update_layout(
        width=1000,
        height=500,
        margin=dict(l=40, r=40, t=40, b=40),
        legend=dict(
            orientation="h",
            x=1,
            y=1,
            xanchor='right',
            yanchor='top',
            bgcolor='rgba(0,0,0,0)'
        )
    )

    st.plotly_chart(fig, use_container_width=True)

    st.header("Performance Metrics")
    st.subheader("Unadjusted front month futures")
    row1_col1, row1_col2, row1_col3, row1_col4 = st.columns(4)
    total_return, volatility, sharpe_ratio, maxdrawdown = get_performance_metrics(plot_df, "Unadjusted Price")
    row1_col1.metric("Total Return", f"{total_return:.1%}")
    row1_col2.metric("Volatility", f"{volatility:.1%}")
    row1_col3.metric("Sharpe Ratio", f"{sharpe_ratio:.1%}")
    row1_col4.metric("Max Drawdown", f"{np.round(maxdrawdown,0)}")

    if selected_adjustment:
        st.subheader("Adjusted front month futures")
        row2_col1, row2_col2, row2_col3, row2_col4 = st.columns(4)
        total_return, volatility, sharpe_ratio, maxdrawdown = get_performance_metrics(plot_df, selected_adjustment)
        row2_col1.metric("Total Return", f"{total_return:.1%}")
        row2_col2.metric("Volatility", f"{volatility:.1%}")
        row2_col3.metric("Sharpe Ratio", f"{sharpe_ratio:.1%}")
        row2_col4.metric("Max Drawdown", f"{np.round(maxdrawdown,0)}")





