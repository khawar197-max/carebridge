import json
from typing import Literal

from pydantic import BaseModel, Field


class IntakeResult(BaseModel):
    """
    Structured result produced by the Intake Agent.
    """

    intent: str = Field(
        description="The user's main request or intent."
    )

    urgency: Literal[
        "LOW",
        "NORMAL",
        "HIGH"
    ] = Field(
        description="Initial urgency classification."
    )

    required_agents: list[str] = Field(
        description="Agents required to handle the request."
    )

    requires_human_review: bool = Field(
        description="Whether human review is required."
    )

    reason: str = Field(
        description="Short explanation of the routing decision."
    )


class IntakeAgent:
    """
    CareBridge Intake & Triage Agent.

    This agent does NOT diagnose or prescribe.
    Its job is to understand the request and route
    it to the appropriate CareBridge components.
    """

    name = "Intake & Triage Agent"

    def __init__(self, llm):
        self.llm = llm

    def analyze(self, user_message: str) -> IntakeResult:

        system_prompt = """
You are the Intake & Triage Agent for CareBridge.

CareBridge is a privacy-first care coordination system.

Your responsibilities:
1. Understand the user's request.
2. Classify the intent.
3. Estimate workflow urgency.
4. Select the appropriate CareBridge agents.
5. Identify whether human review is required.

You MUST NOT:
- Diagnose diseases.
- Prescribe medication.
- Recommend medication doses.
- Replace a healthcare professional.
- Make independent medical decisions.

Available agents:

document:
Handles uploaded healthcare documents.

rag:
Retrieves information from the trusted CareBridge knowledge base.

care_coordinator:
Creates proposed care coordination tasks.

safety:
Checks safety-sensitive or potentially urgent situations.

memory:
Retrieves relevant previous CareBridge interactions.

If the request involves multiple areas, select multiple agents.

Return ONLY valid JSON using this structure:

{
    "intent": "string",
    "urgency": "LOW | NORMAL | HIGH",
    "required_agents": ["agent_name"],
    "requires_human_review": true,
    "reason": "short explanation"
}
"""

        prompt = f"""
Analyze the following user request:

USER REQUEST:
{user_message}

Return only JSON.
"""

        response = self.llm.invoke(
            system_prompt + "\n\n" + prompt
        )

        content = response.content

        try:
            data = json.loads(content)
            return IntakeResult.model_validate(data)

        except Exception:
            return IntakeResult(
                intent="unknown",
                urgency="HIGH",
                required_agents=["safety"],
                requires_human_review=True,
                reason=(
                    "The Intake Agent could not safely validate "
                    "the model output."
                ),
            )
