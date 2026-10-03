from sqlalchemy.orm import Session

from database.models import AuditLog


def log_agent_action(
    db: Session,
    agent_name: str,
    action: str,
    patient_id: int | None = None,
    user_id: int | None = None,
    input_reference: str | None = None,
    output_reference: str | None = None,
    approval_status: str | None = None,
):
    """
    Record an important CareBridge agent action.
    """

    audit = AuditLog(
        user_id=user_id,
        patient_id=patient_id,
        agent_name=agent_name,
        action=action,
        input_reference=input_reference,
        output_reference=output_reference,
        approval_status=approval_status,
    )

    db.add(audit)
    db.commit()
    db.refresh(audit)

    return audit


def get_audit_history(
    db: Session,
    patient_id: int | None = None,
):
    query = (
        db.query(AuditLog)
        .order_by(AuditLog.timestamp.desc())
    )

    if patient_id is not None:
        query = query.filter(
            AuditLog.patient_id == patient_id
        )

    return query.all()
