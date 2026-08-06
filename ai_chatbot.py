import streamlit as st

def fraud_chatbot(selected_score):
    st.subheader("🤖 AI Fraud Analyst Chatbot")

    query = st.text_input("Ask AI about this account")

    if query:
        if selected_score > 70:
            st.error("AI: High fraud probability detected. Recommend immediate freeze.")
        elif selected_score > 40:
            st.warning("AI: Moderate risk. Monitor transactions closely.")
        else:
            st.success("AI: Account appears safe with normal behavior.")