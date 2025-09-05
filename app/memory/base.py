from typing import List, Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class StoredMessage:
    id: str
    role: str
    content: str
    tokens: int

class IMemory:
    def get_thread(self, thread_id: str) -> List[StoredMessage]:
        raise NotImplementedError
    def append(self, thread_id: str, message: StoredMessage, max_tokens: int) -> None:
        raise NotImplementedError
    def truncate(self, thread_id: str, max_tokens: int) -> None:
        raise NotImplementedError
