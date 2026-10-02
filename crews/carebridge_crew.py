from config import get_llm

from agents.intake_agent import IntakeAgent
from agents.document_agent import DocumentAgent
from agents.care_coordinator_agent import CareCoordinatorAgent


class CareBridgeCrew:
    """
    Main CareBridge agent coordinator.
    """

    def __init__(self):

        self.llm = get_llm()

        self.intake_agent = IntakeAgent(
            llm=self.llm
        )

        self.document_agent = DocumentAgent(
            llm=self.llm
        )

        self.care_coordinator_agent = CareCoordinatorAgent(
            llm=self.llm
        )

    def process_request(
        self,
        user_message: str
    ):

        return self.intake_agent.analyze(
            user_message
        )

    def analyze_document(
        self,
        document_text: str
    ):

        return self.document_agent.analyze(
            document_text
        )

    def propose_care_task(
        self,
        document_result
    ):

        return self.care_coordinator_agent.propose_task(
            document_result
        )
