import streamlit as st
from utils.sidebar import insert_side_bar

# Streamlit UI
st.title("📊 Quantvas: Futures Analytics Dashboard")
st.header("Welcome to Quantvas!") 
st.write(
    """
    Quantvas stands for Quantitative Canvas - a dashboard for quantitative finance.
    The first iteration of Quantvas focuses on futures across traditional assets such as equity index and fixed income, 
    and less traditional ones like commodity, volatility and dividend.

    The aim of this app is to provide a platform for people to explore the concept of futures, 
    covering key topics such as the forward curve (term structure), intra-commodity pairs, inter-commodity pairs,
    and handling of futures to generate continuous front month series.

    This is an interactive dashboard app built for the sole purpose of education only.
    The content on this dashboard shall not be taken as financial advices.
    """
    )

st.header("Content Overview")
st.subheader("📈 Forward Curve Analysis")
st.write(
    """
The Forward Curve Analysis provides a visualization of the forward term structure. 
"""
) 
st.subheader("🕝 Intra-Commodity Analysis")
st.write(
    """
The Intra-Commodity Analysis allows user to compare the price difference between two expiration of the same underlying.
"""
) 
st.subheader("⚖️ Inter-Commodity Analysis")
st.write(
    """
The Inter-Commodity Analysis allows user to compare the price difference between two futures of the same expiry.
"""
) 
st.subheader("1️⃣ Continuous-First Futures")
st.write(
    """
The Continuous-first futures allows user to sttch different expiries together to form a continuous front month contract.
One can apply forward or backward adjustment, and compare with the unadjustment series.
It also displays the key performance metrics, assuming a simple buy-and-hold strategy.
"""
) 

st.subheader("📃 Contract Specifications")
st.write(
    """
The Contract Specifications page provides a clear explanation of the convention used in the futures industry. 
It also offers key information on the contracts, such as the ticker, exchange of listing and expiration dates.
"""
) 


insert_side_bar()


