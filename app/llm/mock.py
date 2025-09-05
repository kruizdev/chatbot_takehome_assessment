from typing import Dict, Any, List
import itertools

# A deterministic mock that either returns text or a tool call
class MockLLM:
    _id_iter = itertools.count(1)

    def __init__(self) -> None:
        pass

    def complete(self, messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        # If the latest user message mentions "pet policy" with an airline, trigger a tool call.
        last = next((m for m in reversed(messages) if m.get("role") == "user"), None)
        if last and "pet policy" in last.get("content", "").lower():
            airline = "Delta" if "delta" in last["content"].lower() else "United"
            return {
                "id": f"cmpl_{next(self._id_iter)}",
                "role": "assistant",
                "content": None,
                "tool_call": {
                    "id": f"tool_{next(self._id_iter)}",
                    "name": "airline_pets.get_policy",
                    "arguments": {"airline": airline, "pet_type": "dog", "question": last["content"]},
                },
            }
        # Otherwise return a tiny echo text
        return {
            "id": f"cmpl_{next(self._id_iter)}",
            "role": "assistant",
            "content": "Here is an answer based on your question.",
            "tool_call": None,
        }
