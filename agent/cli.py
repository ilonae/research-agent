"""CLI entry point — installed as the `arxiv-digest` command"""

import argparse
import logging
import sys
from langchain_core.messages import HumanMessage
from agent.graph import build_graph

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="arxiv-digest",
        description="Fetch, filter, and summarise today's ArXiv papers",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Skip LLM summarisation (no Ollama needed)",
    )
    args = parser.parse_args()

    if args.dry_run:
        import tools.semantic_filter as sf
        sf.should_summarise = lambda state: "skip"

    graph = build_graph()
    final = graph.invoke({
        "messages":        [HumanMessage(content="Run daily digest.")],
        "raw_papers":      [],
        "relevant_papers": [],
        "digest":          "",
    })

    print("\n" + "=" * 60)
    print(f"  Papers fetched:   {len(final['raw_papers'])}")
    print(f"  Papers relevant:  {len(final['relevant_papers'])}")
    print("=" * 60)

    if final["digest"]:
        print("\n" + final["digest"])
    else:
        print("\nNo relevant papers found.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
