import streamlit as st

def insert_side_bar():
    st.sidebar.caption(
        "© 2025 Finsinyur. All rights reserved."
    )

    linkedin = "https://raw.githubusercontent.com/Finsinyur/Quantvas/main/img/linkedin.gif"
    main = "https://raw.githubusercontent.com/Finsinyur/Quantvas/main/img/main.gif"
    email = "https://raw.githubusercontent.com/Finsinyur/Quantvas/main/img/email.gif"
    quantsimplified = (
        "https://raw.githubusercontent.com/Finsinyur/Quantvas/main/img/blog.gif"
    )

    st.sidebar.caption(
        f"""
            <div style='display: flex; align-items: center;'>
                <a href = 'https://www.linkedin.com/in/leecaden/'><img src='{linkedin}' style='width: 35px; height: 35px; margin-right: 25px;'></a>
                <a href = 'https://www.quantcollective.io/'><img src='{main}' style='width: 32px; height: 32px; margin-right: 25px;'></a>
                <a href = 'mailto:caden.finsinyur@gmail.com'><img src='{email}' style='width: 28px; height: 28px; margin-right: 25px;'></a>
                <a href = 'https://caden-finsinyur.medium.com/'><img src='{quantsimplified}' style='width: 28px; height: 28px; margin-right: 25px;'></a>
            </div>
            """,
        unsafe_allow_html=True,
    )