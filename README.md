# arxiv-paper-digest

[![PyPI](https://img.shields.io/pypi/v/arxiv-paper-digest)](https://pypi.org/project/arxiv-paper-digest/)
[![Python](https://img.shields.io/pypi/pyversions/arxiv-paper-digest)](https://pypi.org/project/arxiv-paper-digest/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A daily agent that monitors ArXiv for papers matching your research interests, filters by semantic similarity, summarises with a local LLM, and saves a Markdown digest. No external API keys required.

## How it works

```
1. ArXiv RSS
2. filter_unseen (SQLite)
3. semantic filter (sentence-transformers)
4. summarise (Ollama)
5. outputs/digests/YYYY-MM-DD.md
```

## Quickstart

```bash
# Requires Ollama running with the model pulled
ollama pull llama3.2:3b

pip install arxiv-paper-digest
arxiv-digest              # full run
arxiv-digest --dry-run    # skip LLM, test the rest of the pipeline
```

Or from source:

```bash
git clone https://github.com/ilonae/research-agent
cd research-agent
pip install -e ".[dev]"
```

## Configuration

Copy `.env.example` to `.env`. All variables are optional — defaults shown:

| Variable | Default |
|---|---|
| `AGENT_OLLAMA_MODEL` | `llama3.2:3b` |
| `AGENT_OLLAMA_URL` | `http://localhost:11434` |
| `AGENT_MAX_PER_FEED` | `20` |
| `AGENT_ARXIV_CATEGORIES` | `["cs.LG","cs.AI","cs.CV"]` |
| `AGENT_SIMILARITY_THRESHOLD` | `0.35` |
| `AGENT_EMBEDDING_MODEL` | `all-MiniLM-L6-v2` |
| `AGENT_ANCHORS` | `[]` — set your topics here |

To target a different research area, set `AGENT_ANCHORS` to sentences describing your topics and update `AGENT_ARXIV_CATEGORIES` accordingly:

```bash
AGENT_ARXIV_CATEGORIES=["cs.RO","cs.CV"]
AGENT_ANCHORS=["robot learning from human demonstration","sim-to-real transfer for manipulation"]
```

## Docker

```bash
docker compose up   # starts Ollama sidecar + agent
```

## Scheduled runs

`.github/workflows/daily-digest.yml` runs at 07:00 UTC and commits the digest back to the repo. Trigger manually from **Actions → Run workflow** to test.

## Querying the memory store

```bash
sqlite3 outputs/seen_papers.db \
  "SELECT title, first_seen FROM seen_papers
   WHERE first_seen >= date('now', '-7 days')
   ORDER BY first_seen DESC;"
```

## Development

```bash
pip install -e ".[dev]"
pytest && ruff check . && mypy agent/ tools/ config/
```

## License

MIT
