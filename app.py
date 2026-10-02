import streamlit as st

st.set_page_config(
    page_title="CareBridge",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 CareBridge")
st.subheader("Privacy-First Multi-Agent AI Care Coordination System")

st.write(
    """
    CareBridge is a privacy-first AI system designed to organize
    healthcare information, coordinate follow-ups, retrieve trusted
    information, and maintain an auditable care history.

    **CareBridge does not diagnose, prescribe, or replace a healthcare professional.**
    """
)

st.divider()

st.info("🚧 CareBridge is currently under development.")

st.header("System Modules")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("📄 Documents")
    st.write("Upload and extract information from healthcare documents.")

with col2:
    st.subheader("🧠 AI Agents")
    st.write("Specialized agents process information and coordinate workflows.")

with col3:
    st.subheader("🛡️ Safety")
    st.write("Safety checks and human approval protect sensitive actions.")

st.divider()

st.caption("CareBridge — Multi-Agent AI Hackathon Project")
