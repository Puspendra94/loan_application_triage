"""
Verification Agent

Responsible for verifying application data through external services.
"""

from ..state import LoanApplicationState
from ..util.llm import get_llm_with_tools
from langgraph.types import interrupt, Command

def human_review_agent(state: LoanApplicationState) -> LoanApplicationState:
    human_input = interrupt("Waiting for human review...")

    return {
        "decision": human_input["decision"],
        "reasoning": human_input.get("reasoning", "Manual review decision")
    }

