"""
Phoenix Tracing Setup

Provides tracing configuration for the loan triage system.
"""

from phoenix.otel import register


def initialize_phoenix_tracer():
    """
    Initialize Phoenix tracer for the loan triage agent.
    """
    tracer_provider = register(
        project_name='Loan Application Triage Agent',
        auto_instrument=True,
    )
    return tracer_provider