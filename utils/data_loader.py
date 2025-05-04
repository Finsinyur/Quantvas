import streamlit as st
import pandas as pd
import psycopg2

def load_data():
    # Get the PostgreSQL URL
    database_url = st.secrets["database_url"]

    connection = psycopg2.connect(database_url)
    df = pd.read_sql("SELECT * FROM futures_price_2020", connection)
    df = df.sort_values(
        by = ['date', 'exch_code', 'expiration_date']
    )

    df['expiration_date'] = pd.to_datetime(df['expiration_date'])

    df_ts = df[df['expiration_date'].dt.year == 2020].copy()
    df_ts['expiration_month'] = df_ts['expiration_date'].dt.strftime("%Y-%m-01")

    connection.close()
    return df

def load_spec():
    database_url = st.secrets["database_url"]

    connection = psycopg2.connect(database_url)
    df = pd.read_sql("SELECT * FROM product_reference_data", connection)

    connection.close()
    return df