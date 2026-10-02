from datetime import date
from sqlalchemy.orm import Session

from database.models import (
    Patient,
    Interaction,
    CareTask,
)


def create_patient(
    db: Session,
    patient_code: str,
    display_name: str,
    date_of_birth: date | None = None,
    gender: str | None = None,
    emergency_contact: str | None = None,
):
    """
    Create a new patient record.
    """

    existing_patient = (
        db.query(Patient)
        .filter(Patient.patient_code == patient_code)
        .first()
    )

    if existing_patient:
        return existing_patient

    patient = Patient(
        patient_code=patient_code,
        display_name=display_name,
        date_of_birth=date_of_birth,
        gender=gender,
        emergency_contact=emergency_contact,
    )

    db.add(patient)
    db.commit()
    db.refresh(patient)

    return patient


def get_patient(
    db: Session,
    patient_code: str,
):
    """
    Retrieve a patient using their patient code.
    """

    return (
        db.query(Patient)
        .filter(Patient.patient_code == patient_code)
        .first()
    )


def save_interaction(
    db: Session,
    patient_id: int,
    user_message: str,
    agent_response: str,
    agent_name: str,
    risk_level: str = "LOW",
):
    """
    Store an interaction between the user and CareBridge.
    """

    interaction = Interaction(
        patient_id=patient_id,
        user_message=user_message,
        agent_response=agent_response,
        agent_name=agent_name,
        risk_level=risk_level,
    )

    db.add(interaction)
    db.commit()
    db.refresh(interaction)

    return interaction


def create_care_task(
    db: Session,
    patient_id: int,
    title: str,
    description: str | None = None,
    due_date: date | None = None,
    priority: str = "MEDIUM",
    created_by_agent: str | None = None,
):
    """
    Create a proposed care coordination task.

    Important:
    Tasks are created as PROPOSED and should require
    human approval before sensitive actions are taken.
    """

    task = CareTask(
        patient_id=patient_id,
        title=title,
        description=description,
        due_date=due_date,
        priority=priority,
        status="PROPOSED",
        created_by_agent=created_by_agent,
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


def get_patient_tasks(
    db: Session,
    patient_id: int,
):
    """
    Retrieve care tasks for a patient.
    """

    return (
        db.query(CareTask)
        .filter(CareTask.patient_id == patient_id)
        .order_by(CareTask.created_at.desc())
        .all()
    )


def approve_care_task(
    db: Session,
    task_id: int,
    approved_by: str,
):
    """
    Approve a proposed care task.

    Human approval is required before a proposed
    task becomes an approved action.
    """

    task = (
        db.query(CareTask)
        .filter(CareTask.id == task_id)
        .first()
    )

    if not task:
        return None

    if task.status != "PROPOSED":
        return task

    task.status = "APPROVED"
    task.approved_by = approved_by

    db.commit()
    db.refresh(task)

    return task


def reject_care_task(
    db: Session,
    task_id: int,
    rejected_by: str,
):
    """
    Reject a proposed care task.
    """

    task = (
        db.query(CareTask)
        .filter(CareTask.id == task_id)
        .first()
    )

    if not task:
        return None

    if task.status != "PROPOSED":
        return task

    task.status = "REJECTED"
    task.approved_by = rejected_by

    db.commit()
    db.refresh(task)

    return task
