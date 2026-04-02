"""Digest and extension points for future channels"""

import logging
from datetime import datetime
from pathlib import Path
from langchain_core.messages import AIMessage

logger = logging.getLogger(__name__)

OUTPUT_DIR = Path("outputs/digests")


def save_digest(state):
    """Markdown digest to outputs/digests/YYYY-MM-DD.md."""
    digest = state.get("digest", "")
    if not digest:
        logger.warning("save_digest called with empty digest; skipping write")
        return state

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    date_str = datetime.now().strftime("%Y-%m-%d")
    path = OUTPUT_DIR / f"{date_str}.md"
    path.write_text(digest, encoding="utf-8")
    logger.info("Digest saved to %s", path)

    return {
        **state,
        "messages": state["messages"] + [
            AIMessage(content=f"Digest saved to {path}.")
        ],
    }

def deliver_email(digest: str, recipients: list[str]) -> None:
    """Send digest by email - with smtplib or SendGrid"""
    raise NotImplementedError("deliver_email is not yet implemented")


def deliver_slack(digest: str, webhook_url: str) -> None:
    """Post digest to a Slack channel via Webhook"""
    raise NotImplementedError("deliver_slack is not yet implemented")
