from config import get_llm

from agents.intake_agent import IntakeAgent
from agents.document_agent import DocumentAgent


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
