# Agent Memory RAG Compressor

A lightweight prototype for long-running multi-agent LLM workflows. It combines shared agent memory, keyword-based retrieval, and extractive context compression so agents can reuse important past information without passing an entire conversation history into every prompt.

This repository is an original educational implementation inspired by the ideas behind `mem0ai/mem0`, `microsoft/LLMLingua`, MacRAG, MemAgent, and OpenViking. It does not copy upstream source code.

## Motivation

Multi-agent LLM systems often fail when useful information is buried in long conversation histories. Simply expanding context windows is expensive and does not guarantee better recall. A practical agent workflow needs three complementary capabilities:

- Memory: store durable facts, decisions, and user preferences
- Retrieval: select relevant memory for the current task
- Compression: keep retrieved context concise enough to fit prompt budgets

This project implements a small auditable version of that pipeline for experimentation and portfolio demonstration.

## Features

- Shared memory store for multiple named agents
- Agent-specific namespaces plus global memory
- Simple keyword retrieval using token overlap
- Extractive context compression with a configurable sentence budget
- CLI demo for adding memory and querying compressed context
- JSON storage for easy inspection and reproducibility

## Quick Start

Add memory:

```bash
python -m src.memory_cli add --agent researcher --text "ARB improves candidate recall by 2.0 to 10.9 percentage points on OAEI biomedical ontology matching tasks."
python -m src.memory_cli add --agent coder --text "The project should preserve missing metrics as TODO items instead of inventing results."
```

Query memory:

```bash
python -m src.memory_cli query --agent researcher --query "ontology matching recall results" --limit 3 --sentences 2
```

Example output:

```text
Compressed context:
- ARB improves candidate recall by 2.0 to 10.9 percentage points on OAEI biomedical ontology matching tasks.
```

## Architecture

```text
User / Agent Query
      |
      v
Tokenization and scoring
      |
      v
Memory retrieval from agent and global namespaces
      |
      v
Extractive compression
      |
      v
Compact context for the next LLM call
```

## Design Principles

- Auditable: retrieval and compression are transparent and inspectable
- Conservative: no model-generated facts are written into memory by default
- Modular: the retriever and compressor can be replaced with vector search or LLMLingua-style compression
- Research-friendly: missing evaluation metrics are kept as TODOs until measured

## Relationship to Reference Projects

- `mem0ai/mem0`: informs the idea of a universal memory layer for AI agents
- `microsoft/LLMLingua`: informs the motivation for prompt/context compression
- `BytedTsinghua-SIA/MemAgent`: informs long-context memory-agent design motivation
- `volcengine/OpenViking`: informs the combination of agent memory, knowledge RAG, and skills
- MacRAG: informs multi-scale adaptive context retrieval

This repository is not a fork and does not include source code from those projects.

## Repository Structure

```text
agent-memory-rag-compressor/
  src/
    memory_core.py
    memory_cli.py
  README.md
  pyproject.toml
  LICENSE
```

## Evaluation TODOs

- [TODO] Measure token reduction compared with full-history prompting
- [TODO] Measure answer accuracy with and without compressed memory
- [TODO] Add a benchmark conversation set for multi-agent research workflows
- [TODO] Compare keyword retrieval with vector retrieval

## License

MIT License.
