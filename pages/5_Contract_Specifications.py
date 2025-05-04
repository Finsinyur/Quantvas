import streamlit as st
from utils.data_loader import load_spec
import pandas as pd

st.title("📃 Contract Specification")

st.header("Contract Mnemonic")
st.write(
    """
Every future contracts are represented by its ticker (e.g. SGP) followed by its contract mnemonic (e.g. F20).

The contract mnemonic is short-form to represent the settlement date of the respective futures.
It comes with an alphabet that represents the settlement month (see table below), followed by the settlement year (YY).

One misconception is that the settlement month is the same as the expiration month. 
While this is the case for certain asset classes (e.g. Equity indices), this is not the case for others.
For instance, the Brent Crude oil futures are quoted on a M-2 basis, i.e. a M20 futures settled on March 2020 expires on January 2020.
"""
)
# Define your table data directly as a list of lists
data = [['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']]

# Define the column names
columns = ['F', 'G', 'H', 'J', 'K', 'M', 'N', 'Q', 'U', 'V', 'X', 'Z']

df_mnemonic = pd.DataFrame(data = data, columns= columns, index = ['Mnemonic'])

st.dataframe(df_mnemonic)

st.header('Full Contract Details')
df = load_spec()
df['expiration_date'] = pd.to_datetime(df['expiration_date'])
tmp_df = df[df['expiration_date'].dt.year == 2020].copy()
#tmp_df['expiration_date'] = tmp_df['expiration_date'].dt.strftime("%d/%m/%Y")

df_product_specs =\
    pd.pivot_table(
        data = tmp_df,
        index = ["exch_code", "exchange", "underlying", "asset_class", "contract_size", "contract_price_unit"],
        columns= "contract_code",
        values="expiration_date",
        aggfunc=lambda x: x.iloc[0].strftime("%d/%m/%Y") if not x.empty else None
    )



st.dataframe(df_product_specs, use_container_width=True, height=600)
