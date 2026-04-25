"""
Loan Application Triage State Models

Pydantic models for managing the state of loan applications
through the triage process.
"""

from typing import TypedDict, Annotated, Literal
from langgraph.graph.message import add_messages


class LoanApplicationState(TypedDict):
    raw_text: str
    applicant_name: str
    pan: str
    employer_name: str
    loan_amount: float
    monthly_income: float
    credit_score: int | None
    risk_category: str | None
    employment_verified: bool | None
    verification_summary: str
    decision: Literal["APPROVE", "REJECT", "REFER"]
    reasoning: str
    audit_log: list
    messages: Annotated[list, add_messages]
