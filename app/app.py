import streamlit as st

st.set_page_config(
    page_icon=":books:",
    layout="wide",
)

pg = st.navigation([
    st.Page("home.py", title="Overview", icon=":material/home:"),
    st.Page("states_and_districts.py", title="States and Districts", icon=":material/location_on:"),
    st.Page("years.py", title="Years", icon=":material/date_range:"),
])

pg.run()
