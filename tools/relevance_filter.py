"""Keyword-based relevance filter for fetched papers"""

import logging
from langchain_core.messages import AIMessage
from config.settings import KEYWORDS

logger = logging.getLogger(__name__)


def filter_relevant(state):
    """Keep only papers whose title or abstract contains at least one keyword."""
    relevant = []
    lower_kw = [k.lower() for k in KEYWORDS]

    for paper in state["raw_papers"]:
        text = f"{paper['title']} {paper['abstract']}".lower()
        hits = [kw for kw in lower_kw if kw in text]
        if hits:
            paper["matched"] = hits
            relevant.append(paper)

    logger.info(
        "%d/%d papers passed keyword filter",
        len(relevant),
        len(state["raw_papers"]),
    )

    return {
        **state,
        "relevant_papers": relevant,
        "messages": state["messages"] + [
            AIMessage(content=f"{len(relevant)} relevant papers found.")
        ],
    }


def should_summarise(state):
    """Conditional edge: skip summarisation when no relevant papers were found"""
    return "continue" if state.get("relevant_papers") else "skip"
