from typing import Dict, Any, List, Protocol

class LLM(Protocol):
    def complete(self, messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        ...
