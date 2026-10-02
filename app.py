import streamlit as st

from crews.carebridge_crew import CareBridgeCrew


st.set_page_config(
    page_title="CareBridge",
    page_icon="🏥",
    layout="wide"
)


def main():

    st.title("🏥 CareBridge")

    st.subheader(
        "Privacy-First Multi-Agent AI Care Coordination System"
    )

    st.warning(
        "CareBridge is a hackathon prototype. "
        "It does not diagnose, prescribe, or replace "
        "a qualified healthcare professional."
    )

    st.divider()

    st.header("CareBridge Assistant")

    user_message = st.text_area(
        "Describe your request",
        placeholder=(
            "Example: I uploaded my discharge summary "
            "and need help understanding the follow-up process."
        ),
        height=150
    )

    if st.button(
        "Analyze Request",
        type="primary"
    ):

        if not user_message.strip():

            st.error(
                "Please enter a request first."
            )

            return

        with st.spinner(
            "CareBridge is analyzing your request..."
        ):

            try:

                crew = CareBridgeCrew()

                result = crew.process_request(
                    user_message
                )

                st.success(
                    "Request analyzed successfully."
                )

                st.subheader(
                    "Intake Agent Result"
                )

                col1, col2 = st.columns(2)

                with col1:

                    st.metric(
                        "Intent",
                        result.intent
                    )

                with col2:

                    st.metric(
                        "Urgency",
                        result.urgency
                    )

                st.write(
                    "**Required Agents:**"
                )

                for agent in result.required_agents:

                    st.write(
                        f"• {agent}"
                    )

                st.write(
                    "**Human Review Required:**",
                    result.requires_human_review
                )

                st.write(
                    "**Reason:**"
                )

                st.info(
                    result.reason
                )

            except Exception as e:

                st.error(
                    "CareBridge could not process "
                    "the request."
                )

                st.caption(
                    f"Technical details: {e}"
                )


if __name__ == "__main__":
    main()
