"""
Verification Agent

Responsible for verifying application data through external services.
"""

import json
import re
from ..state import LoanApplicationState
from ..util.llm import get_llm_with_tools


def verification_agent(state: LoanApplicationState) -> LoanApplicationState:
    """
    Verification agent that uses tools to verify credit and employment data.
    """
    llm = get_llm_with_tools()

    prompt = f"""
        You are a verification agent. You have access to tools to verify credit and employment information.

        AVAILABLE TOOLS:
        - mock_credit_bureau: Use this to get credit score for a PAN number
        - mock_employment_verification: Use this to verify employment details

        INSTRUCTIONS:
        1. First, call the mock_credit_bureau tool with the PAN: {state['pan']}
        2. Then, call the mock_employment_verification tool with the employer: {state['employer_name']}
        3. Based on the tool results, provide a verification_summary
        4. Respond with JSON containing credit_score, employment_verified, and verification_summary

        IMPORTANT: You MUST call the tools first before providing your final answer.
        Do not provide default values unless the tools fail to return results.
    """

    config = {'configurable': {'thread_id': '1'}}
    response = llm.invoke(prompt, config=config)
    print(f"[verification_agent] Raw LLM response:\n{response.content}")

    if getattr(response, "tool_calls", None):
        return {"messages": [response]}

    raw_content = response.content
    json_match = re.search(r"```(?:json)?\s*(.*?)```", raw_content, re.DOTALL)
    json_str = json_match.group(1) if json_match else raw_content

    # Try to parse JSON, with fallback for single quotes
    try:
        extracted = json.loads(json_str.strip())
    except json.JSONDecodeError:
        # Fallback: try to fix common JSON formatting issues
        import ast
        try:
            # Use ast.literal_eval as a safer alternative for parsing Python-like dict syntax
            extracted = ast.literal_eval(json_str.strip())
        except (ValueError, SyntaxError):
            # Last resort: return default values
            extracted = {
                "credit_score": 0,
                "employment_verified": False,
                "verification_summary": "Failed to parse verification response"
            }

    # ✅ Log parsed fields
    print(f"[verification_agent] Extracted fields:\n{extracted}")

    return {
        'messages': [response],
        **extracted
    }
