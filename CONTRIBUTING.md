# Contributing

## Setup

```bash
git clone https://github.com/ilonae/research-agent
cd research-agent
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env   # fill in your anchors
```

Requires [Ollama](https://ollama.com/download) for full runs. Use `--dry-run` to skip it.

## Running the agent

```bash
arxiv-digest --dry-run   # fetch + filter, no LLM
arxiv-digest             # full run
```

## Code style

```bash
ruff check .
mypy agent/ tools/ config/
```

## Project layout

| Path | Purpose |
|---|---|
| `agent/` | LangGraph state and graph wiring |
| `config/` | Pydantic settings, env var loading |
| `tools/` | One file per graph node |
| `prompts/` | Versioned YAML prompt templates |
| `outputs/` | Digests and SQLite memory store |

## Adding a new tool

1. Create `tools/your_tool.py` with a function `(state: AgentState) -> AgentState`
2. Wire it as a node in `agent/graph.py`
3. Add any new settings to `config/settings.py` and `.env.example`

## Prompt changes

Edit `prompts/summarise_paper.yaml` — add a new version entry with a `released` date and `note` explaining what changed. Update `current_version` to point to it.

## Opening a PR

- Keep commits focused; one concern per commit
- Run `ruff` and `mypy` before pushing
- For new features, include a `--dry-run` path that works without Ollama
