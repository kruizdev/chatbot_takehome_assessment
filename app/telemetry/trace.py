import time
import uuid
from typing import Any, Dict, List

class Span:
    def __init__(self, name: str):
        self.name = name
        self.trace_id = str(uuid.uuid4())
        self.start = time.time()
        self.events: List[Dict[str, Any]] = []

    def event(self, name: str, **fields: Any) -> None:
        self.events.append({"ts": time.time(), "name": name, **fields})

    def finish(self) -> Dict[str, Any]:
        return {"trace_id": self.trace_id, "duration_ms": int((time.time() - self.start) * 1000), "events": self.events}

def start_span(name: str) -> Span:
    return Span(name)
