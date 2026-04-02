from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    raw_papers: list[dict]
    relevant_papers: list[dict]
    digest: str
