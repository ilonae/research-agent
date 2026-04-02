"""Fetch paper metadata from ArXiv feeds"""

import feedparser
import logging
from langchain_core.messages import AIMessage
from config.settings import ARXIV_CATEGORIES, MAX_PER_FEED

logger = logging.getLogger(__name__)


def fetch_papers(state):
    """Pull latest entries from ArXiv for each category"""
    papers = []
    for cat in ARXIV_CATEGORIES:
        url = f"https://rss.arxiv.org/rss/{cat}"
        feed = feedparser.parse(url)
        for entry in feed.entries[:MAX_PER_FEED]:
            papers.append({
                "title":    entry.get("title", "").replace("\n", " ").strip(),
                "abstract": entry.get("summary", "").replace("\n", " ").strip(),
                "url":      entry.get("link", ""),
                "category": cat,
            })
        logger.info("Fetched %d papers from %s", len(feed.entries[:MAX_PER_FEED]), cat)

    return {
        **state,
        "raw_papers": papers,
        "messages": state["messages"] + [
            AIMessage(content=f"Fetched {len(papers)} papers total.")
        ],
    }
