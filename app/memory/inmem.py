from typing import List, Dict
from .base import IMemory, StoredMessage

def _count_tokens(text: str) -> int:
    # Very rough token proxy: word count
    return max(1, len(text.split()))

class InMemory(IMemory):
    def __init__(self):
        self.store: Dict[str, List[StoredMessage]] = {}

    def get_thread(self, thread_id: str) -> List[StoredMessage]:
        return list(self.store.get(thread_id, []))

    def append(self, thread_id: str, message: StoredMessage, max_tokens: int) -> None:
        msg = StoredMessage(
            id=message.id, role=message.role, content=message.content, tokens=_count_tokens(message.content)
        )
        arr = self.store.setdefault(thread_id, [])
        # idempotent by id
        if any(m.id == msg.id for m in arr):
            return
        arr.append(msg)
        self.truncate(thread_id, max_tokens)

    def truncate(self, thread_id: str, max_tokens: int) -> None:
        arr = self.store.get(thread_id, [])
        total = sum(m.tokens for m in arr)
        if total <= max_tokens:
            return
        # Keep system, trim from oldest user/assistant pairs first
        keep = []
        system = [m for m in arr if m.role == "system"]
        keep.extend(system)
        others = [m for m in arr if m.role != "system"]
        # drop from start until tokens fit
        for m in others:
            if sum(x.tokens for x in keep) + sum(y.tokens for y in others[others.index(m):]) <= max_tokens:
                keep.extend(others[others.index(m):])
                break
        self.store[thread_id] = keep
