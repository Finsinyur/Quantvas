import streamlit as st
from utils.data_loader import load_data
from utils.sidebar import insert_side_bar
import plotly.express as px
import plotly.graph_objects as go
import plotly.express as px

st.title("🕝 Intra-Commodity Spread Analysis")
df = load_data()
df_ts = df[df['expiration_date'].dt.year == 2020].copy()
df_ts['expiration_month'] = df_ts['expiration_date'].dt.strftime("%Y-%m-01")

# --- Sidebar Inputs ---
st.sidebar.header("🔧 Filters")

# Product selector
products = sorted(df_ts['exch_code'].unique())
selected_product = st.sidebar.selectbox("Ticker:", products, index=products.index("SGP") if "SGP" in products else 0)

# Contract selector (dependent on selected products)
filtered_contracts = sorted(df_ts[df_ts['exch_code'] == selected_product]['contract_code'].unique())
selected_contracts = st.sidebar.multiselect("Contracts:", filtered_contracts, default=filtered_contracts[:2])

# Date range slider
min_date = df_ts['date'].min()
max_date = df_ts['date'].max()
start_date, end_date = st.sidebar.slider(
    "Date Range:",
    min_value=min_date,
    max_value=max_date,
    value=(min_date, max_date)
)

# Normalize checkbox
normalize = st.sidebar.checkbox("Normalize Prices")

# --- Data Filtering ---
mask = (
    (df_ts['exch_code'] == selected_product) &
    (df_ts['contract_code'].isin(selected_contracts)) &
    (df_ts['date'] >= start_date) &
    (df_ts['date'] <= end_date)
)
filtered_df = df_ts[mask]

# Normalize if requested
if normalize and not filtered_df.empty:
    filtered_df['daily_settle_price'] = (
        filtered_df.groupby(['exch_code', 'contract_code'])['daily_settle_price']
        .transform(lambda x: x / x.iloc[0] * 100)
    )

# --- Plot ---
if filtered_df.empty:
    st.warning("No data for the selected filters.")
else:
    fig = px.line(
        filtered_df,
        x='date',
        y='daily_settle_price',
        color='exch_code',
        line_dash='contract_code',
        hover_data=['date', 'underlying', 'exch_code', 'daily_settle_price'],
        title='Futures time series: {}'.format(selected_product),
        template='ggplot2'
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

insert_side_bar()