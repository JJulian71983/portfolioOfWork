import streamlit as st
from utils import clear_cache
import os

# Page Configurations
st.set_page_config(page_title="Econ Games", layout="wide", initial_sidebar_state="auto")

if "auth_passed" not in st.session_state:
    st.session_state["auth_passed"] = False
    st.switch_page(page="pages/1_Login.py")
if "disconnect" not in st.session_state:
    st.session_state["disconnect"] = False
else:
    os.remove("C:\\Anaconda\\Projects\\tobaccoMarket\\game_inputs.json")
    clear_cache()
    st.stop()

# Page Titles
st.title(body=r"$\text{\Large Economics\ Games}$")
st.subheader("Educational games for macro, micro, and economic history courses")
st.divider()
st.button(label="Clear Cache", key="clear", on_click=clear_cache)
with st.sidebar:
    st.page_link(page="pages/2_Tobacco_market_of_1690.py", label="Tobacco Market", use_container_width=False)
    st.page_link(page="pages/3_Prisoners_Dilemma.py", label="Prisoner\'s Dilemma", use_container_width=False)
    if st.button(label="Logout", key="logout", on_click=None, use_container_width=False):
        st.session_state["disconnect"] = True
