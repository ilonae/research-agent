from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="AGENT_",
    )

    ollama_model: str = Field(default="llama3.2:3b", description="Ollama model tag")
    ollama_url: str = Field(default="http://localhost:11434", description="Ollama base URL")
    max_per_feed: int = Field(default=20, description="Max papers fetched per ArXiv feed")

    arxiv_categories: list[str] = Field(
        default=["cs.LG", "cs.AI", "cs.CV"],
        description="ArXiv category slugs to monitor",
    )
    keywords: list[str] = Field(
        default=[
            "explainab", "interpretab", "attribution",
            "LRP", "CRP", "SHAP", "saliency", "prototype",
            "pruning", "medical imaging", "skin lesion",
            "mechanistic", "point cloud",
        ],
        description="Keyword substrings for relevance filtering",
    )


settings = Settings()

OLLAMA_MODEL = settings.ollama_model
OLLAMA_URL = settings.ollama_url
MAX_PER_FEED = settings.max_per_feed
ARXIV_CATEGORIES = settings.arxiv_categories
KEYWORDS = settings.keywords
