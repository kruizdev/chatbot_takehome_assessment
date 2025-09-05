from typing import Callable, Dict, Any
from .airline_pets import get_policy

ToolFn = Callable[..., dict]

REGISTRY: Dict[str, ToolFn] = {
    "airline_pets.get_policy": get_policy
}
