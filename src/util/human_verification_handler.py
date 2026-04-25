"""
Human Verification Handler

Handles human review interruptions in the loan triage workflow.
"""

from langgraph.types import Command


def handle_human_verification(graph, result, config):
    """
    Handle human verification interruptions in the loan triage workflow.

    This function manages the human review process when the decision agent
    recommends "REFER" for edge cases requiring human judgment.

    Args:
        graph: The LangGraph instance
        result: Current graph execution result
        config: Graph configuration

    Returns:
        Updated result after human review (if needed)
    """
    while "__interrupt__" in result:
        print(f"""
    ========== HUMAN REVIEW REQUIRED ==========""")
        print(f"Applicant     : {result.get('applicant_name', 'Unknown')}")
        print(f"PAN           : {result.get('pan', 'N/A')}")
        print(f"Employer      : {result.get('employer_name', 'Unknown')}")
        print(f"Loan Amount   : ₹{result.get('loan_amount', 0):,.0f}")
        print(f"Monthly Income: ₹{result.get('monthly_income', 0):,.0f}")
        print(f"Credit Score  : {result.get('credit_score', 0)}")
        print(f"Employment    : {result.get('employment_verified', False)}")
        print(f"Summary       : {result.get('verification_summary', 'N/A')}")
        print(f"Initial Reasoning: {result.get('reasoning', 'N/A')}")
        print("="*43)

        # ✅ Get human decision from CLI
        decision = input("\nEnter decision (APPROVE/REJECT): ").strip().upper()
        while decision not in ["APPROVE", "REJECT"]:
            decision = input("Invalid entry. Please enter APPROVE or REJECT: ").strip().upper()

        # ✅ Get reasoning for the human decision
        reasoning = input("Enter your reasoning for this decision: ").strip()
        if not reasoning:
            reasoning = "Human reviewer decision"

        # ✅ Resume graph execution with human input
        result = graph.invoke(
            Command(resume={"decision": decision, "reasoning": reasoning}),
            config=config
        )

    return result