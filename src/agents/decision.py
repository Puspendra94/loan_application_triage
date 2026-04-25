"""
Decision Agent

Responsible for making final loan approval decisions.
"""

import json
import re
from ..state import LoanApplicationState
from ..util.llm import get_llm_with_tools


def decision_agent(state: LoanApplicationState) -> LoanApplicationState:
    """
    Decision agent that makes final loan approval decisions.
    """
    llm = get_llm_with_tools()

    prompt = f"""You are a senior credit decision officer reviewing a loan application.
        APPLICATION DETAILS:
        - Applicant: {state['applicant_name']}
        - Loan Amount: {state['loan_amount']}
        - Monthly Income: {state['monthly_income']}
        - Employer: {state['employer_name']}

        VERIFICATION RESULTS:
        - Credit Score: {state['credit_score']}
        - Employment Verified: {state['employment_verified']}
        - Verification Summary: {state['verification_summary']}
        - Risk Category: {state['risk_category']}

        DECISION RULES:
        - APPROVE: credit_score >= 700 AND employment_verified == True AND loan_amount <= 10x monthly_income
        - REJECT: credit_score < 500 OR employment_verified == False
        - REFER: anything that doesn't clearly fit APPROVE or REJECT (edge cases, missing data, medium risk)

        Respond ONLY with raw JSON, no markdown:
        {{"decision": "APPROVE" or "REJECT" or "REFER", "reasoning": "<clear explanation referencing the numbers above>"}}
    """

    response = llm.invoke(prompt)
    print(f"[decision_agent] Raw LLM response:\n{response.content}")

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
                "decision": "REFER",
                "reasoning": "Failed to parse decision response"
            }

    # ✅ Log parsed fields
    print(f"[decision_agent] Extracted fields:\n{extracted}")

    return {
        'messages': [response],
        **extracted
    }
