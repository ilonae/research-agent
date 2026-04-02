from langgraph.graph import StateGraph, START, END
from agent.state import AgentState
from agent.nodes import fetch_papers, filter_relevant, summarise_papers, should_summarise


def build_graph():
    g = StateGraph(AgentState)
    g.add_node("fetch_papers",    fetch_papers)
    g.add_node("filter_relevant", filter_relevant)
    g.add_node("summarise_papers", summarise_papers)

    g.add_edge(START, "fetch_papers")
    g.add_edge("fetch_papers", "filter_relevant")
    g.add_conditional_edges( "filter_relevant", should_summarise, {"continue": "summarise_papers", "skip": END})
    g.add_edge("summarise_papers", END)
    return g.compile()

agent = build_graph()
