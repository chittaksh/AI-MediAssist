
"""Shared OpenAI client and LangSmith tracing utilities."""

from langsmith import traceable


def traced_function(name: str):
    """
    Create a named LangSmith trace decorator.

    Keeping this helper makes the trace names consistent
    throughout the application.
    """
    return traceable(
        name=name,
        run_type="chain",
    )