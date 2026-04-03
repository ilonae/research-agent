# arxiv-xai-digest

A daily agent that monitors ArXiv for XAI and interpretability papers, filters by semantic similarity, summarises with a local LLM, and saves a Markdown digest. No external API keys required.

## How it works

```
ArXiv RSS → filter_unseen (SQLite) → semantic filter (sentence-transformers)
          → summarise (Ollama) → outputs/digests/YYYY-MM-DD.md
```

## Quickstart

```bash
# Requires Ollama running with the model pulled
ollama pull llama3.2:3b

pip install arxiv-xai-digest
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
| `AGENT_ANCHORS` | 8 XAI topic sentences |

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
