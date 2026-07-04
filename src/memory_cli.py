from __future__ import annotations

import argparse

from .memory_core import MemoryStore, compress


def main() -> None:
    parser = argparse.ArgumentParser(description="Shared memory retrieval and compression demo.")
    parser.add_argument("--store", default="memory.json", help="Path to the JSON memory store.")

    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Add a memory item.")
    add_parser.add_argument("--agent", default="global", help="Agent namespace.")
    add_parser.add_argument("--text", required=True, help="Memory text to store.")

    query_parser = subparsers.add_parser("query", help="Retrieve and compress memory.")
    query_parser.add_argument("--agent", default="global", help="Agent namespace.")
    query_parser.add_argument("--query", required=True, help="Current task or question.")
    query_parser.add_argument("--limit", type=int, default=5, help="Number of memory items to retrieve.")
    query_parser.add_argument("--sentences", type=int, default=3, help="Compressed sentence budget.")

    args = parser.parse_args()
    store = MemoryStore(args.store)

    if args.command == "add":
        store.add(args.agent, args.text)
        print(f"Added memory for agent '{args.agent}'.")
        return

    if args.command == "query":
        results = store.query(args.agent, args.query, args.limit)
        compressed = compress(results, args.query, args.sentences)
        print("Compressed context:")
        for sentence in compressed:
            print(f"- {sentence}")


if __name__ == "__main__":
    main()
