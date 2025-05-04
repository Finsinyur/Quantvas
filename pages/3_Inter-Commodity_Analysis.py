import streamlit as st
from utils.data_loader import load_data
import plotly.express as px
import plotly.graph_objects as go
import plotly.express as px

st.title("📈 Inter-Commodity Pair Analysis")

df = load_data()
df_ts = df[df['expiration_date'].dt.year == 2020].copy()
df_ts['expiration_month'] = df_ts['expiration_date'].dt.strftime("%Y-%m-01")

# --- Sidebar Inputs ---
st.sidebar.header("🔧 Filters")

# Expiry selector
expiries = sorted(df_ts['expiration_month'].unique())
selected_expiry =\
    st\
        .sidebar\
            .selectbox("Expiry:", expiries, 
                       index=expiries.index("2020-06-01") if "2020-06-01" in expiries else 0)

# Product selector (dependent on selected expiries)
filtered_products = sorted(df_ts[df_ts['expiration_month'] == selected_expiry]['exch_code'].unique())
selected_products = st.sidebar.multiselect("Products:", filtered_products, default=['B', 'CL'])

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
    (df_ts['expiration_month'] == selected_expiry) &
    (df_ts['exch_code'].isin(selected_products)) &
    (df_ts['date'] >= start_date) &
    (df_ts['date'] <= end_date)
)
filtered_df = df_ts[mask]

# Normalize if requested
if normalize and not filtered_df.empty:
    filtered_df['daily_settle_price'] = (
        filtered_df.groupby(['exch_code', 'expiration_month'])['daily_settle_price']
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
        hover_data=['date', 'underlying', 'exch_code', 'daily_settle_price'],
        title='Expiration series: {}'.format(selected_expiry),
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


st.write("""
         An inter-commodity pair refers to a combination of futures that are not of the same underlying.

         A classical example of an inter-commodity pair is the Brent-WTI, as both are based on crude oil price markers that
         are of different location (we also call this a locational spread).

         An inter-commodity pair can apply to many asset classes, for instance:
""")

st.markdown("""
- Equity Index : EURO STOXX 50-DAX (A play on continental Europe bluechip vs German bluechip)
- Volatility Index : VIX-VSTOXX (A play on difference in forward volatility of different regions) 
- Fixed Income: EURO-Bund vs EURO-Schatz (A play of the yield curve, short tenor (2Y) vs long tenor (10Y))
""")

st.write("""
         An inter-commodity pair trade is generally a trade that bets on mean-reversion.
         Therefore, when dealing with intercommodity spread, one needs to be careful with the spread leg construction. 
         One needs to construct the pair with an appropriate hedge ratio.
         For commodities, one needs to be cognizant of other factors that may or may not be tradable, such as freight.
         """)