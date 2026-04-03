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

    # Semantic filter 
    embedding_model: str = Field(
        default="all-MiniLM-L6-v2",
        description="sentence-transformers model name",
    )
    similarity_threshold: float = Field(
        default=0.35,
        description="Min cosine similarity to any anchor for paper to pass",
    )
    anchors: list[str] = Field(
        default=[
            "explainable AI and interpretability of neural networks",
            "concept-based explanations for image classifiers",
            "feature attribution and saliency maps for deep learning",
            "mechanistic interpretability of large language models",
            "pruning neural networks while preserving interpretability",
            "prototype-based and example-based explanations",
            "XAI methods for medical image analysis",
            "fairness, accountability, and transparency in machine learning",
        ],
        description="Anchor sentences that define the topics of interest",
    )


settings = Settings()

OLLAMA_MODEL = settings.ollama_model
OLLAMA_URL = settings.ollama_url
MAX_PER_FEED = settings.max_per_feed
ARXIV_CATEGORIES = settings.arxiv_categories
KEYWORDS = settings.keywords
EMBEDDING_MODEL = settings.embedding_model
SIMILARITY_THRESHOLD = settings.similarity_threshold
ANCHORS = settings.anchors
