"""
LLM Configuration and Initialization

Provides LLM setup with fallbacks for the loan triage system.
"""

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.tools import tool

# Load environment variables
load_dotenv()


def initialize_llm_with_fallbacks():
    """
    Initialize LLM with fallbacks as used in the notebook.
    """
    primary_model = init_chat_model("openai/gpt-oss-120b", model_provider="groq")
    # 1. The "Heavy Lifter" (Use for complex logic)
    model_1 = init_chat_model("llama-3.3-70b-versatile", model_provider="groq")
    # 2. The "Solid Alternative" (If 70b hits a limit)
    model_2 = init_chat_model("mixtral-8x7b-32768", model_provider="groq")
    # 3. The "Infinite Runner" (Very high limits, use to keep the code alive)
    model_3 = init_chat_model("llama-3.1-8b-instant", model_provider="groq")

    llm_group = primary_model.with_fallbacks([model_1, model_2, model_3])
    return llm_group


def get_tools():
    """Get the list of tools for the agents."""
    from ..tools.credit_bureau import mock_credit_bureau
    from ..tools.employment import mock_employment_verification

    return [mock_credit_bureau, mock_employment_verification]


def get_llm_with_tools():
    """Get LLM instance with tools bound."""
    llm_group = initialize_llm_with_fallbacks()
    tools = get_tools()
    return llm_group.bind_tools(tools)