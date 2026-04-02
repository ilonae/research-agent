"""LLM summarisation and Markdown assembly"""

import logging
from datetime import datetime
from langchain_core.messages import AIMessage, HumanMessage
from langchain_ollama import ChatOllama
from config.settings import OLLAMA_MODEL, OLLAMA_URL

logger = logging.getLogger(__name__)

_llm = ChatOllama(model=OLLAMA_MODEL, base_url=OLLAMA_URL, temperature=0.2)

_PROMPT = (
    "Summarise this ML paper in 2 sentences. "
    "Focus on the method and why it matters for XAI or interpretability.\n\n"
    "Title: {title}\n"
    "Abstract: {abstract}"
)


def summarise_papers(state):
    """Generate 2-sentence LLM summaries and assemble a Markdown digest."""
    summarised = []
    for paper in state["relevant_papers"]:
        try:
            response = _llm.invoke([
                HumanMessage(content=_PROMPT.format(
                    title=paper["title"],
                    abstract=paper["abstract"],
                ))
            ])
            paper["summary"] = response.content
        except Exception as e:
            logger.warning("LLM failed for '%s': %s", paper["title"], e)
            paper["summary"] = paper["abstract"][:250] + "..."
        summarised.append(paper)

    lines = [f"# ArXiv Digest — {datetime.now().strftime('%Y-%m-%d')}\n"]
    for i, p in enumerate(summarised, 1):
        lines.append(f"## {i}. {p['title']}")
        lines.append(f"**Keywords matched:** {', '.join(p['matched'])}")
        lines.append(f"\n{p['summary']}\n")
        lines.append(f"{p['url']}\n")
        lines.append("---\n")

    return {
        **state,
        "relevant_papers": summarised,
        "digest": "\n".join(lines),
        "messages": state["messages"] + [
            AIMessage(content="Digest complete.")
        ],
    }
