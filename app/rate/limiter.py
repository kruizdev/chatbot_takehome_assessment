"""TODO: Implement token bucket per user_id.
- capacity=60
- refill=1 token/sec
- cost = ceil(input_tokens/250)
Return (allowed: bool, retry_after_ms: int) from consume().
"""
import time
import math
from typing import Dict, Tuple

class TokenBucket:
    def __init__(self, capacity: int = 60, refill_rate: float = 1.0):
        self.capacity = capacity
        self.refill = refill_rate
        self.state: Dict[str, Tuple[float, float]] = {}  # user_id -> (tokens, last_ts)

    def consume(self, user_id: str, cost_tokens: int) -> Tuple[bool, int]:
        # TODO
        return True, 0

def cost_for_input_tokens(n_tokens: int) -> int:
        return int(math.ceil(n_tokens / 250.0))
