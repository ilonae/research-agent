# Changelog

All notable changes to this project will be documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [0.1.0] — 2026-04-03

### Added
- LangGraph pipeline: fetch → deduplicate → filter → summarise → save
- ArXiv RSS fetcher across configurable category slugs
- Semantic relevance filter using `sentence-transformers` and cosine similarity against user-defined anchor sentences
- Local LLM summarisation via Ollama (`langchain-ollama`)
- SQLite seen-papers store — skips already-processed papers on subsequent runs, tracks `first_seen` date for weekly queries
- Versioned prompt templates in `prompts/summarise_paper.yaml` with per-version changelog notes
- Pydantic settings with `.env` support and `AGENT_` prefix — all parameters overridable without editing source
- Digest output to `outputs/digests/YYYY-MM-DD.md`
- Docker Compose setup with Ollama sidecar and health check
- GitHub Actions workflow for daily scheduled runs — commits digest back to repo
- `arxiv-digest` CLI entry point
- PyPI package: `pip install arxiv-paper-digest`
