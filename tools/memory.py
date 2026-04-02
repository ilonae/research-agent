"""SQLite seen-papers storage
Schema:
seen_papers(paper_id TEXT PK, title TEXT, category TEXT, first_seen DATE)
"""

import logging
import re
import sqlite3
from contextlib import contextmanager
from datetime import date
from pathlib import Path
from langchain_core.messages import AIMessage

logger = logging.getLogger(__name__)

DB_PATH = Path("outputs/seen_papers.db")

_CREATE = """
CREATE TABLE IF NOT EXISTS seen_papers (
    paper_id   TEXT PRIMARY KEY,
    title      TEXT,
    category   TEXT,
    first_seen DATE NOT NULL
)
"""


def _extract_id(url: str) -> str:
    """Return the bare ArXiv ID from a URL, falling back to the full URL."""
    m = re.search(r"arxiv\.org/(?:abs|pdf)/([^\s?#]+)", url)
    return m.group(1) if m else url


@contextmanager
def _connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute(_CREATE)
        conn.commit()
        yield conn
    finally:
        conn.close()

# Graph nodes

def filter_unseen(state):
    """Drop papers that are already in store"""
    with _connect() as conn:
        ids = {row[0] for row in conn.execute("SELECT paper_id FROM seen_papers")}

    before = len(state["raw_papers"])
    fresh = [p for p in state["raw_papers"] if _extract_id(p["url"]) not in ids]
    skipped = before - len(fresh)
    logger.info("Memory: %d already seen, %d new papers", skipped, len(fresh))

    return {
        **state,
        "raw_papers": fresh,
        "messages": state["messages"] + [
            AIMessage(content=f"Skipped {skipped} already-seen papers; {len(fresh)} new.")
        ],
    }


def mark_seen(state):
    """Persist all raw_papers processed this :into the seen-papers storage"""
    today = date.today().isoformat()
    rows = [
        (_extract_id(p["url"]), p["title"], p["category"], today)
        for p in state["raw_papers"]
    ]
    if not rows:
        return state

    with _connect() as conn:
        conn.executemany(
            "INSERT OR IGNORE INTO seen_papers (paper_id, title, category, first_seen)"
            " VALUES (?, ?, ?, ?)",
            rows,
        )
        conn.commit()

    logger.info("Memory: marked %d papers as seen", len(rows))
    return {
        **state,
        "messages": state["messages"] + [
            AIMessage(content=f"Marked {len(rows)} papers as seen.")
        ],
    }
