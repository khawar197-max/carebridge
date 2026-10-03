from sqlalchemy.orm import Session

from database.models import Memory


def get_patient_memories(
    db: Session,
    patient_id: int,
    limit: int = 20,
) -> list[str]:

    memories = (
        db.query(Memory)
        .filter(
            Memory.patient_id == patient_id
        )
        .order_by(
            Memory.updated_at.desc()
        )
        .limit(limit)
        .all()
    )

    results = []

    for memory in memories:

        results.append(
            f"{memory.memory_key}: "
            f"{memory.memory_value}"
        )

    return results
