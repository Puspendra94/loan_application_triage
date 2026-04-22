"""
Main Entry Point

Runs the loan triage system.
"""

import asyncio
from src.orchestrator import create_graph
from src.util.phoenix import initialize_phoenix_tracer
from src.state import LoanApplicationState


async def main():
    """
    Main function to run the loan triage system.
    """
    # Initialize Phoenix tracer
    initialize_phoenix_tracer()

    # Create the graph
    graph = create_graph()

    # Sample loan application
    sample_application = """
    Hi, I am John Doe, PAN: ABCDE1234F, working at Google, monthly income 50000, need loan of 200000.
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
    async for event in graph.astream(initial_state, config=config):
        for node_name, state in event.items():
            print(f"\n--- {node_name} ---")
            for key, value in state.items():
                if key != "messages":  # Skip messages for brevity
                    print(f"{key}: {value}")

    # Get final state
    final_state = graph.get_state(config).values
    print("\n=== FINAL DECISION ===")
    print(f"Decision: {final_state.get('decision', 'N/A')}")
    print(f"Reasoning: {final_state.get('reasoning', 'N/A')}")


if __name__ == "__main__":
    asyncio.run(main())
