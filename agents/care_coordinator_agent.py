import json
from datetime import date, timedelta

from pydantic import BaseModel, Field


class CareTaskProposal(BaseModel):
    """
    Structured task proposed by the Care Coordinator Agent.
    """

    title: str = Field(
        description="Short title of the proposed care task."
    )

    description: str = Field(
        description="Description of the proposed task."
    )

    due_date: str | None = Field(
        default=None,
        description="Proposed due date in YYYY-MM-DD format."
    )

    priority: str = Field(
        description="LOW, MEDIUM, or HIGH."
    )

    requires_human_approval: bool = Field(
        description="Whether a human must approve the task."
    )

    reason: str = Field(
        description="Reason for proposing the task."
    )


class CareCoordinatorAgent:
    """
    CareBridge Care Coordinator Agent.

    Converts extracted information into proposed
    coordination tasks.

    The agent does NOT independently execute
    medical decisions or patient treatment.
    """

    name = "Care Coordinator Agent"

    def __init__(self, llm):
        self.llm = llm

    def propose_task(
        self,
        document_result,
        reference_date: date | None = None
    ) -> CareTaskProposal:

        if reference_date is None:
            reference_date = date.today()

        system_prompt = """
You are the Care Coordinator Agent for CareBridge.

Your job is to convert verified information from
CareBridge document processing into a proposed
care coordination task.

You MUST NOT:
- Diagnose a patient.
- Prescribe medication.
- Change treatment.
- Recommend medication doses.
- Make independent medical decisions.

Only create coordination tasks supported by
the provided information.

Every task MUST require human approval.

Possible priorities:
LOW
MEDIUM
HIGH

Return ONLY valid JSON:

{
    "title": "string",
    "description": "string",
    "due_date": "YYYY-MM-DD or null",
    "priority": "LOW | MEDIUM | HIGH",
    "requires_human_approval": true,
    "reason": "short explanation"
}
"""

        document_data = {
            "document_type": document_result.document_type,
            "document_date": document_result.document_date,
            "follow_up_required": document_result.follow_up_required,
            "follow_up_days": document_result.follow_up_days,
            "instructions": document_result.instructions,
            "confidence": document_result.confidence,
        }

        prompt = f"""
Create a proposed care coordination task from
the following extracted document information.

EXTRACTED INFORMATION:
{json.dumps(document_data, indent=2)}

Reference date:
{reference_date.isoformat()}

Only create a task if a follow-up or coordination
action is explicitly supported.

Return only JSON.
"""

        response = self.llm.invoke(
            system_prompt + "\n\n" + prompt
        )

        content = response.content

        try:

            data = json.loads(content)

            result = CareTaskProposal.model_validate(data)

            # Deterministic safety rule:
            # Care Coordinator proposals can never
            # bypass human approval.
            result.requires_human_approval = True

            return result

        except Exception:

            return CareTaskProposal(
                title="Human review required",
                description=(
                    "The care coordination proposal "
                    "could not be safely validated."
                ),
                due_date=None,
                priority="HIGH",
                requires_human_approval=True,
                reason=(
                    "Structured output validation failed."
                ),
            )
