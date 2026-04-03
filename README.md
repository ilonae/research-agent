# arxiv-xai-digest

A daily agent that monitors ArXiv for new papers on explainable AI and interpretability, filters them by semantic relevance, summarises each one with a local LLM, and saves a Markdown digest to disk.

Runs fully locally — no external API keys required.

---

## How it works

```
ArXiv RSS feeds
      │
      ▼
 fetch_papers          Pull up to N papers per category
      │
      ▼
 filter_unseen         Skip papers already seen (SQLite)
      │
      ▼
 filter_relevant       Semantic similarity against anchor sentences
      │                (sentence-transformers, runs on CPU/MPS/CUDA)
      ▼
 summarise_papers      2-sentence summary via local Ollama LLM
      │
      ▼
 save_digest           Write outputs/digests/YYYY-MM-DD.md
      │
      ▼
 mark_seen             Persist paper IDs so next run skips them
```

The graph is built with [LangGraph](https://github.com/langchain-ai/langgraph). The semantic filter uses `all-MiniLM-L6-v2` (80 MB, fast on CPU). The LLM is served locally by [Ollama](https://ollama.com).

---

## Quickstart

### Prerequisites
- Python 3.11+
- [Ollama](https://ollama.com/download) installed and running

```bash
ollama pull llama3.2:3b
```

### Install

```bash
pip install arxiv-xai-digest
```

Or from source:

```bash
git clone https://github.com/ilonae/research-agent
cd research-agent
pip install -e ".[dev]"
```

### Run

```bash
# Full run — fetches, filters, summarises, saves digest
arxiv-digest

# Skip the LLM (no Ollama needed, tests the whole pipeline otherwise)
arxiv-digest --dry-run
```

The digest is saved to `outputs/digests/YYYY-MM-DD.md`.

---

## Configuration

All settings are overridable via environment variables (prefix `AGENT_`) or a `.env` file. Copy `.env.example` to get started:

```bash
cp .env.example .env
```

| Variable | Default | Description |
|---|---|---|
| `AGENT_OLLAMA_MODEL` | `llama3.2:3b` | Any model tag pulled in Ollama |
| `AGENT_OLLAMA_URL` | `http://localhost:11434` | Ollama base URL |
| `AGENT_MAX_PER_FEED` | `20` | Papers fetched per ArXiv category |
| `AGENT_ARXIV_CATEGORIES` | `["cs.LG","cs.AI","cs.CV"]` | ArXiv category slugs |
| `AGENT_SIMILARITY_THRESHOLD` | `0.35` | Min cosine similarity to pass filter |
| `AGENT_EMBEDDING_MODEL` | `all-MiniLM-L6-v2` | sentence-transformers model |
| `AGENT_ANCHORS` | *(8 XAI topics)* | Anchor sentences defining your research interest |

To focus on a different domain, replace `AGENT_ANCHORS` with sentences describing your topics and adjust `AGENT_ARXIV_CATEGORIES` accordingly.

---

## Docker

```bash
# Start Ollama sidecar + agent (digest written to ./outputs/)
docker compose up
```

The Ollama service waits for a health check before the agent starts. Model weights are stored in a named Docker volume so they survive restarts.

---

## Scheduled runs (GitHub Actions)

The included workflow (`.github/workflows/daily-digest.yml`) runs at 07:00 UTC every day, commits the new digest to the repo, and skips if nothing changed.

To enable it: push to a repo, go to **Actions → Daily ArXiv Paper Digest → Run workflow** for a first manual test.

---

## Querying the memory store

Seen papers are stored in `outputs/seen_papers.db` (SQLite). Query directly:

```bash
# How many papers seen total?
sqlite3 outputs/seen_papers.db "SELECT count(*) FROM seen_papers;"

# What did I find this week?
sqlite3 outputs/seen_papers.db \
  "SELECT title, first_seen FROM seen_papers
   WHERE first_seen >= date('now', '-7 days')
   ORDER BY first_seen DESC;"
```

---

## Project layout

```
agent/          LangGraph state + graph definition
config/         Pydantic settings (env / .env file)
prompts/        Versioned YAML prompt templates
tools/
  arxiv_fetcher.py    ArXiv RSS → paper dicts
  semantic_filter.py  Embedding-based relevance scoring
  digest_formatter.py LLM summarisation + Markdown assembly
  delivery.py         File output + email/Slack stubs
  memory.py           SQLite seen-papers store
outputs/
  digests/            YYYY-MM-DD.md files
  seen_papers.db      Deduplication store
```

---

## Development

```bash
pip install -e ".[dev]"
pytest
ruff check .
mypy agent/ tools/ config/
```

---

## License

MIT — see [LICENSE](LICENSE).
