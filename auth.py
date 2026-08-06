import streamlit as st

def login():
    st.sidebar.title("🔐 Secure Login")

    user = st.sidebar.text_input("Username")
    pwd = st.sidebar.text_input("Password", type="password")

    if st.sidebar.button("Login"):
        if user == "boi" and pwd == "admin":
            st.session_state["auth"] = True
        else:
            st.sidebar.error("Invalid credentials")

def check_auth():
    return st.session_state.get("auth", False)