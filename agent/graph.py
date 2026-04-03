from langgraph.graph import StateGraph, START, END
from agent.state import AgentState
from tools.arxiv_fetcher import fetch_papers
from tools.memory import filter_unseen, mark_seen
from tools.semantic_filter import filter_relevant, should_summarise
from tools.digest_formatter import summarise_papers
from tools.delivery import save_digest


def build_graph():
    g = StateGraph(AgentState)
    g.add_node("fetch_papers",    fetch_papers)
    g.add_node("filter_unseen",   filter_unseen)
    g.add_node("filter_relevant", filter_relevant)
    g.add_node("summarise_papers", summarise_papers)
    g.add_node("save_digest",     save_digest)
    g.add_node("mark_seen",       mark_seen)

    g.add_edge(START,              "fetch_papers")
    g.add_edge("fetch_papers",     "filter_unseen")
    g.add_edge("filter_unseen",    "filter_relevant")
    g.add_conditional_edges("filter_relevant", should_summarise,
                            {"continue": "summarise_papers", "skip": "mark_seen"})
    g.add_edge("summarise_papers", "save_digest")
    g.add_edge("save_digest",      "mark_seen")
    g.add_edge("mark_seen",        END)
    return g.compile()
