import streamlit as st


# Functions
def clear_cache():
    for key in st.session_state.keys():
        del st.session_state[key]
