"""
Intake Agent

Responsible for initial processing of loan applications.
"""

import json
import re
from ..state import LoanApplicationState
from ..util.llm import get_llm_with_tools


def intake_agent(state: LoanApplicationState) -> LoanApplicationState:
    """
    Intake agent that extracts structured data from raw application text.
    """
    llm = get_llm_with_tools()

    prompt = f"""
        You are a loan intake agent.
        Extract structured JSON from the text below eg.: applicant_name, pan, employer_name, loan_amount, monthly_income etc.
        Respond ONLY with raw JSON, no markdown, no explanation.
        If a field is missing, use defaults like Unknown for strings, 0 for numeric and so on

        Text: {state['raw_text']}
    """

    response = llm.invoke(prompt)
    print(f"[intake_agent] Raw LLM response:\n{response.content}")

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
                "applicant_name": "Unknown",
                "pan": "",
                "employer_name": "Unknown",
                "loan_amount": 0,
                "monthly_income": 0
            }

    # ✅ Log parsed fields
    print(f"[intake_agent] Extracted fields:\n{extracted}")

    return {
        'messages': [response],
        **extracted
    }
