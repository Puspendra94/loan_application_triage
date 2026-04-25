"""
Main Entry Point

Runs the loan triage system.
"""

from src.orchestrator import create_graph
from src.util.phoenix import initialize_phoenix_tracer
from src.util.human_verification_handler import handle_human_verification
from src.state import LoanApplicationState


def main():
    """
    Main function to run the loan triage system.
    """
    # Initialize Phoenix tracer
    initialize_phoenix_tracer()

    # Create the graph
    graph = create_graph()

    # Sample loan application
    sample_application = """
    Hi, I am John Doe, PAN: QWERT1234Z, working at Google, monthly income 50000, need loan of 200000.
    """

    # Initial state
    initial_state: LoanApplicationState = {
        "raw_text": sample_application,
        "applicant_name": "",
        "pan": "",
        "employer_name": "",
        "loan_amount": 0,
        "monthly_income": 0,
        "credit_score": 0,
        "risk_category": "",
        "employment_verified": False,
        "verification_summary": "",
        "decision": "",
        "reasoning": "",
        "audit_log": [],
        "messages": []
    }

    # Run the graph
    config = {"configurable": {"thread_id": "1"}}

    # ============================================================================
    # ADVANCED APPROACH (Commented for future reference)
    # ============================================================================
    # This method uses `astream()` which streams results from each agent step-by-step
    # It's useful for:
    #   - Debugging: See what each agent outputs at each stage
    #   - Learning: Understand the multi-agent workflow progression
    #   - Monitoring: Track real-time processing in production dashboards
    #
    # Flow:
    #   1. Intake Agent → Extracts applicant info from raw text
    #   2. Verification Agent → Calls credit bureau & employment services
    #   3. Decision Agent → Makes final approve/reject/refer decision
    #
    # How it works:
    #   - `async for event in graph.astream()` loops through each agent's output
    #   - Each event contains the node name and updated state
    #   - You can see intermediate values (credit_score, employment_verified, etc.)
    #
    # When to use this:
    #   - Learning and understanding the system
    #   - Debugging why a decision was made
    #   - Real-time monitoring dashboards
    #
    # Uncomment below to see the detailed step-by-step workflow:
    #
    # async for event in graph.astream(initial_state, config=config):
    #     for node_name, state in event.items():
    #         print(f"\n--- {node_name} ---")
    #         for key, value in state.items():
    #             if key != "messages":  # Skip messages for brevity
    #                 print(f"{key}: {value}")
    #
    # final_state = graph.get_state(config).values
    # print("\n=== FINAL DECISION ===")
    # print(f"Decision: {final_state.get('decision', 'N/A')}")
    # print(f"Reasoning: {final_state.get('reasoning', 'N/A')}")

    # ============================================================================
    # SIMPLE APPROACH (Easy to understand for beginners)
    # ============================================================================
    # This method uses `invoke()` which is the simplest way to run the graph
    # It's like calling a function: you pass input, wait for result, get output
    #
    # Why it's simpler:
    #   - No async/await complexity
    #   - Direct result: input → process → output
    #   - Perfect for scripts that just need the final decision
    #   - Same result as the advanced approach, just without seeing intermediate steps
    #
    result = graph.invoke(initial_state, config=config)

    # ============================================================================
    # HUMAN VERIFICATION HANDLER
    # ============================================================================
    # If the decision agent recommends "REFER", the graph pauses and waits for
    # human review. This utility function handles that interruption.
    #
    # When to use:
    #   - Edge cases where automated decision is uncertain
    #   - High-value loans requiring human judgment
    #   - Applications with conflicting indicators
    #
    # The function:
    #   1. Checks if graph execution was interrupted
    #   2. Shows all application details to the human reviewer
    #   3. Gets approval/rejection decision and reasoning from user
    #   4. Resumes the graph with the human decision
    #   5. Repeats until graph completes (if multiple reviews needed)
    #
    result = handle_human_verification(graph, result, config)

    print("\n=== FINAL DECISION ===")
    print(f"Decision: {result.get('decision', 'N/A')}")
    print(f"Reasoning: {result.get('reasoning', 'N/A')}")
    print(f"Applicant: {result.get('applicant_name', 'Unknown')}")
    print(f"Loan Amount: ₹{result.get('loan_amount', 0):,.0f}")
    print(f"Credit Score: {result.get('credit_score', 0)}")
    print(f"Employment Verified: {result.get('employment_verified', False)}")



if __name__ == "__main__":
    main()
