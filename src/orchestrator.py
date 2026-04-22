"""
Loan Triage Orchestrator

LangGraph-based orchestrator that coordinates the three agents.
"""

from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver

from .state import LoanApplicationState
from .agents.intake import intake_agent
from .agents.verification import verification_agent
from .agents.decision import decision_agent
from .util.llm import get_tools


def human_review_agent(state: LoanApplicationState) -> LoanApplicationState:
    """
    Human review agent - placeholder for human intervention.
    """
    return state


def route_after_decision(state: LoanApplicationState) -> str:
    """
    Route function after decision agent.
    """
    # Check if last message has tool calls (verification agent wants to use tools)
    last_message = state["messages"][-1]
    if getattr(last_message, "tool_calls", None):
        return "tools"
    # No tool calls = verification done, route by decision
    if state["decision"] == "REFER":
        return "REFER"
    return "DECISION"


def create_graph():
    """
    Create and compile the LangGraph workflow.
    """
    # Initialize memory saver
    memory = MemorySaver()

    # Get tools
    tools = get_tools()

    # Create the graph builder
    builder = StateGraph(LoanApplicationState)

    # Add nodes
    builder.add_node("intake_agent_node", intake_agent)
    builder.add_node("verification_agent_node", verification_agent)
    builder.add_node('tools', ToolNode(tools))
    builder.add_node('decision_agent_node', decision_agent)
    builder.add_node('human_review_agent_node', human_review_agent)

    # Add edges
    builder.add_edge(START, 'intake_agent_node')
    builder.add_edge('intake_agent_node', 'verification_agent_node')
    builder.add_edge('tools', 'verification_agent_node')

    # Add conditional edges
    builder.add_conditional_edges(
        'verification_agent_node',
        tools_condition,
        {
            "tools": 'tools',
            "__end__": 'decision_agent_node'
        }
    )

    builder.add_conditional_edges(
        'decision_agent_node',
        route_after_decision,
        {
            "REFER": 'human_review_agent_node',
            "DECISION": END
        }
    )

    builder.add_edge('human_review_agent_node', END)

    # Compile the graph
    graph = builder.compile(checkpointer=memory)
    return graph
