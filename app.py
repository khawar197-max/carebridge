import os
import tempfile
from datetime import date

import streamlit as st

from crews.carebridge_crew import CareBridgeCrew
from tools.document_tools import extract_text_from_file
from database.database import SessionLocal
from tools.database_tools import (
    create_patient,
    create_care_task,
    approve_care_task,
    reject_care_task,
)


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

    st.header("📄 Healthcare Document")

    uploaded_file = st.file_uploader(
        "Upload a synthetic healthcare document",
        type=["pdf", "txt"],
        help=(
            "For the hackathon demo, use synthetic or "
            "de-identified documents only."
        )
    )

    if st.button(
        "Analyze Request",
        type="primary"
    ):

        if not user_message.strip() and not uploaded_file:

            st.error(
                "Please enter a request or upload a document."
            )

            return

        try:

            crew = CareBridgeCrew()

            intake_result = None

            if user_message.strip():

                with st.spinner(
                    "CareBridge is analyzing your request..."
                ):

                    intake_result = crew.process_request(
                        user_message
                    )

                st.success(
                    "Request analyzed successfully."
                )

                st.subheader(
                    "🧭 Intake Agent Result"
                )

                col1, col2 = st.columns(2)

                with col1:

                    st.metric(
                        "Intent",
                        intake_result.intent
                    )

                with col2:

                    st.metric(
                        "Urgency",
                        intake_result.urgency
                    )

                st.write(
                    "**Required Agents:**"
                )

                for agent in intake_result.required_agents:

                    st.write(
                        f"• {agent}"
                    )

                st.write(
                    "**Human Review Required:**",
                    intake_result.requires_human_review
                )

                st.write(
                    "**Reason:**"
                )

                st.info(
                    intake_result.reason
                )

            document_result = None

            if uploaded_file:

                st.divider()

                st.subheader(
                    "📄 Medical Document Agent"
                )

                file_suffix = os.path.splitext(
                    uploaded_file.name
                )[1]

                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=file_suffix
                ) as temp_file:

                    temp_file.write(
                        uploaded_file.getbuffer()
                    )

                    temp_path = temp_file.name

                try:

                    with st.spinner(
                        "Extracting document text..."
                    ):

                        document_text = (
                            extract_text_from_file(
                                temp_path
                            )
                        )

                    if not document_text.strip():

                        st.error(
                            "No readable text was found "
                            "in the document."
                        )

                        return

                    st.success(
                        "Document text extracted."
                    )

                    with st.expander(
                        "View extracted document text"
                    ):

                        st.text(
                            document_text[:10000]
                        )

                    with st.spinner(
                        "Medical Document Agent is analyzing..."
                    ):

                        document_result = (
                            crew.analyze_document(
                                document_text
                            )
                        )

                    st.success(
                        "Document analyzed successfully."
                    )

                    col1, col2, col3 = st.columns(3)

                    with col1:

                        st.metric(
                            "Document Type",
                            document_result.document_type
                        )

                    with col2:

                        st.metric(
                            "Confidence",
                            f"{document_result.confidence:.0%}"
                        )

                    with col3:

                        review = (
                            "YES"
                            if document_result.requires_human_review
                            else "NO"
                        )

                        st.metric(
                            "Human Review",
                            review
                        )

                    st.write(
                        "**Document Date:**",
                        document_result.document_date
                    )

                    st.write(
                        "**Follow-up Required:**",
                        document_result.follow_up_required
                    )

                    st.write(
                        "**Follow-up Days:**",
                        document_result.follow_up_days
                    )

                    st.write(
                        "**Care Coordination Instructions:**"
                    )

                    for instruction in (
                        document_result.instructions
                    ):

                        st.write(
                            f"• {instruction}"
                        )

                    st.info(
                        document_result.reason
                    )

                    if document_result.requires_human_review:

                        st.warning(
                            "⚠️ Human verification is required "
                            "before this information is used "
                            "for care coordination."
                        )

                    if (
                        document_result.follow_up_required
                        and not document_result.requires_human_review
                    ):

                        st.divider()

                        st.subheader(
                            "📋 Care Coordinator Agent"
                        )

                        with st.spinner(
                            "Creating a care coordination proposal..."
                        ):

                            task_proposal = (
                                crew.propose_care_task(
                                    document_result
                                )
                            )

                        st.success(
                            "Care coordination proposal created."
                        )

                        st.write(
                            "**Proposed Task:**"
                        )

                        st.info(
                            task_proposal.title
                        )

                        st.write(
                            "**Description:**"
                        )

                        st.write(
                            task_proposal.description
                        )

                        col1, col2 = st.columns(2)

                        with col1:

                            st.write(
                                "**Due Date:**"
                            )

                            st.write(
                                task_proposal.due_date
                            )

                        with col2:

                            st.write(
                                "**Priority:**"
                            )

                            st.write(
                                task_proposal.priority
                            )

                        st.warning(
                            "👤 Human approval is required "
                            "before this task can become "
                            "an approved care action."
                        )

                        st.write(
                            "**Reason:**"
                        )

                        st.caption(
                            task_proposal.reason
                        )

                        st.divider()

                        st.subheader(
                            "Human Review"
                        )

                        col1, col2 = st.columns(2)

                        with col1:

                            approve = st.button(
                                "✅ Approve Task",
                                type="primary",
                                key="approve_task"
                            )

                        with col2:

                            reject = st.button(
                                "❌ Reject Task",
                                key="reject_task"
                            )

                        if approve:

                            db = SessionLocal()

                            try:

                                patient = create_patient(
                                    db=db,
                                    patient_code="DEMO-P001",
                                    display_name="Synthetic Demo Patient"
                                )

                                due_date = None

                                if task_proposal.due_date:

                                    due_date = date.fromisoformat(
                                        task_proposal.due_date
                                    )

                                task = create_care_task(
                                    db=db,
                                    patient_id=patient.id,
                                    title=task_proposal.title,
                                    description=task_proposal.description,
                                    due_date=due_date,
                                    priority=task_proposal.priority,
                                    created_by_agent=(
                                        "Care Coordinator Agent"
                                    )
                                )

                                approved_task = approve_care_task(
                                    db=db,
                                    task_id=task.id,
                                    approved_by="Human Reviewer"
                                )

                                st.success(
                                    "✅ Task approved and saved "
                                    "to database."
                                )

                                st.write(
                                    f"Task ID: {approved_task.id}"
                                )

                            finally:

                                db.close()

                        if reject:

                            db = SessionLocal()

                            try:

                                patient = create_patient(
                                    db=db,
                                    patient_code="DEMO-P001",
                                    display_name="Synthetic Demo Patient"
                                )

                                due_date = None

                                if task_proposal.due_date:

                                    due_date = date.fromisoformat(
                                        task_proposal.due_date
                                    )

                                task = create_care_task(
                                    db=db,
                                    patient_id=patient.id,
                                    title=task_proposal.title,
                                    description=task_proposal.description,
                                    due_date=due_date,
                                    priority=task_proposal.priority,
                                    created_by_agent=(
                                        "Care Coordinator Agent"
                                    )
                                )

                                rejected_task = reject_care_task(
                                    db=db,
                                    task_id=task.id,
                                    rejected_by="Human Reviewer"
                                )

                                st.error(
                                    "❌ Task rejected and "
                                    "recorded."
                                )

                                st.write(
                                    f"Task ID: {rejected_task.id}"
                                )

                            finally:

                                db.close()

                finally:

                    try:

                        os.remove(temp_path)

                    except OSError:

                        pass

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
