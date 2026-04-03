"""Embedding-based relevance filter

Each paper's title and abstract scores against a set of anchor sentences that define 
the individual research topic.  A paper passes if its max cosine
similarity across all anchors meets the configured threshold.

This catches paraphrased concepts that share no keywords — e.g. "robot learning" and
"learning from demonstration" are semantically close even though neither substring contains the other
"""

import logging
import numpy as np
from functools import lru_cache
from langchain_core.messages import AIMessage
from config.settings import ANCHORS, SIMILARITY_THRESHOLD, EMBEDDING_MODEL

logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def _encoder():
    from sentence_transformers import SentenceTransformer
    logger.info("Loading embedding model '%s' (first run only)", EMBEDDING_MODEL)
    return SentenceTransformer(EMBEDDING_MODEL)


def _cosine(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-9))


def filter_relevant(state):
    """Keep papers with max anchor similarity >= SIMILARITY_THRESHOLD"""
    if not state["raw_papers"]:
        return {**state, "relevant_papers": []}

    model = _encoder()
    anchor_vecs = model.encode(ANCHORS, normalize_embeddings=True)

    relevant = []
    for paper in state["raw_papers"]:
        text = f"{paper['title']}. {paper['abstract']}"
        vec = model.encode(text, normalize_embeddings=True)
        scores = [_cosine(vec, av) for av in anchor_vecs]
        best_score = max(scores)
        best_anchor = ANCHORS[int(np.argmax(scores))]

        if best_score >= SIMILARITY_THRESHOLD:
            paper["similarity_score"] = round(best_score, 4)
            paper["matched_anchor"] = best_anchor
            # Keep "matched" key so digest_formatter doesn't need changes
            paper["matched"] = [f"similarity={best_score:.2f}"]
            relevant.append(paper)

    relevant.sort(key=lambda p: p["similarity_score"], reverse=True)

    logger.info(
        "%d/%d papers passed semantic filter (threshold=%.2f)",
        len(relevant), len(state["raw_papers"]), SIMILARITY_THRESHOLD,
    )

    return {
        **state,
        "relevant_papers": relevant,
        "messages": state["messages"] + [
            AIMessage(content=f"{len(relevant)} semantically relevant papers found.")
        ],
    }


def should_summarise(state):
    """Conditional edge: skip summarisation when no relevant papers were found"""
    return "continue" if state.get("relevant_papers") else "skip"
