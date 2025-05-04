import streamlit as st
from utils.data_loader import load_data
from utils.sidebar import insert_side_bar
import plotly.express as px
import plotly.graph_objects as go
import plotly.express as px



st.title("📈 Forward Curve Analysis")
df = load_data()

# --- Sidebar Inputs ---
st.sidebar.header("🔧 Filters")

# Product selector
product_options = sorted(df['exch_code'].unique())
selected_products = st.sidebar.multiselect(
    "Product:",
    options=product_options,
    default=['SGP']
)

# Date selector
date_options = sorted(df['date'].unique())
selected_dates = st.sidebar.multiselect(
    "Dates:",
    options=date_options,
    default=[date_options[0]]
)


# Normalize checkbox
normalize = st.sidebar.checkbox("Normalize Prices", value=False)

# --- Filter Data ---
mask = (
    df['exch_code'].isin(selected_products) &
    df['date'].isin(selected_dates)
)
filtered_df = df[mask]

# --- Normalize if requested ---
if normalize and not filtered_df.empty:
    filtered_df = filtered_df.copy()
    filtered_df['daily_settle_price'] = (
        filtered_df.groupby(['exch_code', 'date'])['daily_settle_price']
        .transform(lambda x: 100 + (x - x.iloc[0]) / abs(x.iloc[0]) * 100)
    )

# --- Plot ---
if filtered_df.empty:
    st.warning("No data for the selected filters.")
else:
    plot_title = "Forward curves: {}".format(selected_products[0])
    if len(selected_products) > 1:
        plot_title += " & " + " & ".join(selected_products[1:])
    fig = px.line(
        filtered_df,
        x='expiration_date',
        y='daily_settle_price',
        color='exch_code',
        line_dash='date',
        hover_data=['date', 'underlying', 'asset_class', 'contract_code', 'daily_settle_price'],
        title=plot_title
    )

    fig.update_traces(mode='lines+markers', marker=dict(symbol='diamond'))

    fig.update_layout(
        width=1000,
        height=500,
        xaxis_title='Expiration Date',
        yaxis_title='Forward Price',  
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


st.write(
    """
    Test
    """
    )

insert_side_bar()
