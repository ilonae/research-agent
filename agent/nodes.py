"""
Three nodes — fetch, filter, summarise
"""

import feedparser
import logging
from datetime import datetime
from langchain_core.messages import AIMessage, HumanMessage
from langchain_ollama import ChatOllama
from config.settings import OLLAMA_MODEL, OLLAMA_URL, ARXIV_CATEGORIES, KEYWORDS, MAX_PER_FEED

logger = logging.getLogger(__name__)

llm = ChatOllama(model=OLLAMA_MODEL, base_url=OLLAMA_URL, temperature=0.2)


def fetch_papers(state):
    """Pull latest from ArXiv for each category."""
    papers = []
    for cat in ARXIV_CATEGORIES:
        url  = f"https://rss.arxiv.org/rss/{cat}"
        feed = feedparser.parse(url)
        for entry in feed.entries[:MAX_PER_FEED]:
            papers.append({
                "title":    entry.get("title", "").replace("\n", " ").strip(),
                "abstract": entry.get("summary", "").replace("\n", " ").strip(),
                "url":      entry.get("link", ""),
                "category": cat,
            })
        logger.info(f"Fetched {len(feed.entries[:MAX_PER_FEED])} papers from {cat}")

    return {
        **state,
        "raw_papers": papers,
        "messages": state["messages"] + [
            AIMessage(content=f"Fetched {len(papers)} papers total.")
        ],
    }


def filter_relevant(state):
    """Only keywords related to XAI/interpretability"""
    relevant = []
    lower_kw  = [k.lower() for k in KEYWORDS]

    for paper in state["raw_papers"]:
        text = f"{paper['title']} {paper['abstract']}".lower()
        hits = [kw for kw in lower_kw if kw in text]
        if hits:
            paper["matched"] = hits
            relevant.append(paper)

    logger.info(f"{len(relevant)}/{len(state['raw_papers'])} papers passed keyword filter")

    return {
        **state,
        "relevant_papers": relevant,
        "messages": state["messages"] + [
            AIMessage(content=f"{len(relevant)} relevant papers found.")
        ],
    }


def summarise_papers(state):
    """2-sentence summary of each relevant paper"""
    summarised = []
    for paper in state["relevant_papers"]:
        try:
            response = llm.invoke([HumanMessage(content=(
                "Summarise this ML paper in 2 sentences. "
                "Focus on the method and why it matters for XAI or interpretability.\n\n"
                f"Title: {paper['title']}\n"
                f"Abstract: {paper['abstract']}"
            ))])
            paper["summary"] = response.content
        except Exception as e:
            logger.warning(f"LLM failed for '{paper['title']}': {e}")
            paper["summary"] = paper["abstract"][:250] + "..."
        summarised.append(paper)

    lines = [f"# ArXiv Digest — {datetime.now().strftime('%Y-%m-%d')}\n"]
    for i, p in enumerate(summarised, 1):
        lines.append(f"## {i}. {p['title']}")
        lines.append(f"**Keywords matched:** {', '.join(p['matched'])}")
        lines.append(f"\n{p['summary']}\n")
        lines.append(f"{p['url']}\n")
        lines.append("---\n")

    digest = "\n".join(lines)

    return {
        **state,
        "relevant_papers": summarised,
        "digest": digest,
        "messages": state["messages"] + [
            AIMessage(content="Digest complete.")
        ],
    }


def should_summarise(state):
    """Conditional: skip if nothing was found."""
    return "continue" if state.get("relevant_papers") else "skip"
