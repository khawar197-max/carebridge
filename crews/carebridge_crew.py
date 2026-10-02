from config import get_llm
from agents.intake_agent import IntakeAgent


class CareBridgeCrew:
    """
    Main CareBridge agent coordinator.

    At this stage, only the Intake Agent is connected.
    Additional agents will be added step-by-step.
    """

    def __init__(self):
        self.llm = get_llm()

        self.intake_agent = IntakeAgent(
            llm=self.llm
        )

    def process_request(self, user_message: str):
        """
        Process a user request through the Intake Agent.
        """

        result = self.intake_agent.analyze(
            user_message
        )

        return result
