from config import get_llm

from agents.intake_agent import IntakeAgent
from agents.document_agent import DocumentAgent
from agents.care_coordinator_agent import CareCoordinatorAgent
from agents.safety_agent import SafetyAgent


class CareBridgeCrew:

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

        self.safety_agent = SafetyAgent(
            llm=self.llm
        )

    # -----------------------------------------
    # INTAKE AGENT
    # -----------------------------------------

    def process_request(
        self,
        user_message: str,
        trusted_context: str = ""
    ):

        return self.intake_agent.analyze(
            user_message,
            trusted_context=trusted_context
        )

    # -----------------------------------------
    # DOCUMENT AGENT
    # -----------------------------------------

    def analyze_document(
        self,
        document_text: str
    ):

        return self.document_agent.analyze(
            document_text
        )

    # -----------------------------------------
    # CARE COORDINATOR
    # -----------------------------------------

    def propose_care_task(
        self,
        document_result
    ):

        return self.care_coordinator_agent.propose_task(
            document_result
        )

    # -----------------------------------------
    # SAFETY AGENT
    # -----------------------------------------

    def analyze_safety(
        self,
        text: str
    ):

        return self.safety_agent.analyze(
            text
        )
        
