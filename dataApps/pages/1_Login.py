import streamlit as st
import hashlib
import time

# Page Configurations
st.set_page_config(page_title="Econ Games", layout="centered", initial_sidebar_state="collapsed")

if "auth_passed" not in st.session_state:
    st.session_state["auth_passed"] = False
if st.session_state["auth_passed"]:
    st.warning(body="You have already logged in.")
    time.sleep(3)
    st.switch_page("home.py")


def authentication(session_state=st.session_state["auth_passed"]):
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = None
    if not session_state:
        def authentication_form():
            with st.form(key="form_key", clear_on_submit=False, border=True):
                st.text_input(label="Username", key="username", type="default", value=None, placeholder=None)
                st.text_input(label="Password", key="password", type="password", value=None, placeholder=None)
                st.form_submit_button(label="Sign In", on_click=authentication_check, use_container_width=False)

        def authentication_check():
            hash_password = hashlib.new("sha256")
            hash_password.update(bytes(st.session_state["password"], encoding='utf-8'))
            if "hashPassword" not in st.session_state:
                st.session_state["hashPassword"] = hash_password.hexdigest()
            if "dict_to_pass" not in st.session_state:
                st.session_state["dict_to_pass"] = {"user": st.session_state["username"], "password": st.session_state["hashPassword"]}
            if st.session_state["dict_to_pass"]["user"] in st.secrets["passwords"] and st.session_state["dict_to_pass"]["password"] == st.secrets["passwords"][st.session_state["dict_to_pass"]["user"]]:
                if "teamName" not in st.session_state:
                    st.session_state["teamName"] = st.session_state["dict_to_pass"]["user"]
                st.session_state["authenticated"] = True
                for key in st.session_state.keys():
                    if key in ["password", "username", "hashPassword", "dict_to_pass"]:
                        del st.session_state[key]
                    else:
                        pass
                st.success("Successfully authenticated.")
                return None
            else:
                st.session_state["authenticated"] = False
                for key in st.session_state.keys():
                    if key in ["password", "username", "hashPassword", "dict_to_pass"]:
                        del st.session_state[key]
                    else:
                        pass
                st.error("Username and/or password incorrect.")
                return None

        authentication_form()
        if st.session_state["authenticated"]:
            st.session_state["auth_passed"] = True
            return True
        else:
            return False
    if not authentication():
        st.stop()
    else:
        print("Check this #1")


if not st.session_state["auth_passed"]:
    with st.container(height=280, border=True):
        authentication()
if st.session_state["auth_passed"]:
    st.switch_page("home.py")
else:
    print("Check this #2.")
