"""
Verification Agent

Responsible for verifying application data through external services.
"""

import json
import re
from ..state import LoanApplicationState
from ..util.llm import get_llm_with_tools
from langchain_core.messages import SystemMessage


def verification_agent(state: LoanApplicationState) -> LoanApplicationState:
    """
    Verification agent that uses tools to verify credit and employment data.
    """
    llm = get_llm_with_tools()

    system_message = SystemMessage(content=(f"""
        You are a verification agent. You have access to tools to verify credit and employment information.

        AVAILABLE TOOLS:
        - mock_credit_bureau: Use this to get credit score for a PAN number, response format will be {{
            "credit_score": Int,
            "risk_category": Literal["LOW", "MEDIUM", "HIGH"]
        }}
        - mock_employment_verification: Use this to verify employment details, response format will be {{
            "employment_verified": Boolean,
            "employment_type": String,
            "years_in_business": Int
        }}

        INSTRUCTIONS:
        1. First, call the mock_credit_bureau tool with the PAN: {state['pan']}
        2. Then, call the mock_employment_verification tool with the employer: {state['employer_name']}
        3. Based on the tool results, provide a verification_summary
        4. Respond with JSON like {{"credit_score": <int or 0>, "risk_category": Literal["LOW", "MEDIUM", "HIGH"] "employment_verified": <true or false>, "verification_summary": "<summary string>"}}

        IMPORTANT: You MUST call the tools first before providing your final answer.
        Do not provide default values unless the tools fail to return results.
    """))

    # 2. Invoke the LLM with the history.
    # state["messages"] contains the history of what has happened in the graph so far.
    response = llm.invoke([system_message] + state["messages"])

    # 3. IF the LLM wants to call a tool, we just return the message.
    # The graph will route this to the 'tools' node, which runs your Python code,
    # and then the graph loops back HERE.
    if response.tool_calls:
        return {"messages": [response]}

    # 4. IF there are no tool calls, it means the LLM has seen the tool data
    # and is ready to give the final JSON answer.
    try:
        raw_content = response.content
        print(f"[verification_agent] Raw LLM response content:\n{response.content}")
        json_match = re.search(r"({.*})", raw_content, re.DOTALL)
        json_str = json_match.group(1) if json_match else raw_content
        extracted = json.loads(json_str.strip())

        return {
            "messages": [response],
            **extracted
        }
    except Exception as e:
        # Fallback if the LLM fails to produce valid JSON even after tool calls
        return {
            "messages": [response],
            "credit_score": 0,
            "employment_verified": False,
            "verification_summary": f"Error parsing response: {str(e)}"
        }