from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path


TOKEN_RE = re.compile(r"[A-Za-z0-9_@.+-]+")
SENTENCE_RE = re.compile(r"(?<=[.!?])\s+")


@dataclass
class MemoryItem:
    agent: str
    text: str


def tokenize(text: str) -> set[str]:
    return {token.lower() for token in TOKEN_RE.findall(text)}


class MemoryStore:
    def __init__(self, path: str | Path = "memory.json") -> None:
        self.path = Path(path)
        self.items: list[MemoryItem] = []
        self.load()

    def load(self) -> None:
        if not self.path.exists():
            self.items = []
            return
        raw_items = json.loads(self.path.read_text(encoding="utf-8"))
        self.items = [MemoryItem(**item) for item in raw_items]

    def save(self) -> None:
        self.path.write_text(
            json.dumps([asdict(item) for item in self.items], indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    def add(self, agent: str, text: str) -> None:
        cleaned = text.strip()
        if not cleaned:
            raise ValueError("Memory text cannot be empty.")
        self.items.append(MemoryItem(agent=agent.strip() or "global", text=cleaned))
        self.save()

    def query(self, agent: str, query: str, limit: int = 5) -> list[MemoryItem]:
        query_tokens = tokenize(query)
        scored: list[tuple[int, MemoryItem]] = []

        for item in self.items:
            if item.agent not in {agent, "global"}:
                continue
            score = len(query_tokens & tokenize(item.text))
            if score > 0:
                scored.append((score, item))

        scored.sort(key=lambda pair: pair[0], reverse=True)
        return [item for _, item in scored[:limit]]


def compress(items: list[MemoryItem], query: str, sentence_budget: int = 3) -> list[str]:
    query_tokens = tokenize(query)
    candidates: list[tuple[int, str]] = []

    for item in items:
        for sentence in SENTENCE_RE.split(item.text):
            sentence = sentence.strip()
            if not sentence:
                continue
            score = len(query_tokens & tokenize(sentence))
            candidates.append((score, sentence))

    candidates.sort(key=lambda pair: pair[0], reverse=True)
    selected = [sentence for score, sentence in candidates if score > 0]
    if not selected:
        selected = [item.text for item in items]
    return selected[:sentence_budget]
