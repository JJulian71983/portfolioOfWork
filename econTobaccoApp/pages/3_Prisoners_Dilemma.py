import streamlit as st

# Page Configurations, Titles, Headings
st.set_page_config(page_title="Econ Games", layout="wide", initial_sidebar_state="auto")

if not st.session_state["auth_passed"]:
    st.switch_page("pages/1_Login.py")
else:
    st.title(body=r"$\text{\Large Prisoner's\ Dilemma}$")

with st.sidebar:
    st.page_link(page="home.py", label="Home", use_container_width=False)
    st.page_link(page="pages/2_Tobacco_market_of_1690.py", label="Tobacco Market", use_container_width=False)
    if st.button(label="Logout", key="logout", on_click=None, use_container_width=False):
        st.session_state["disconnect"] = True
        st.switch_page("home.py")
