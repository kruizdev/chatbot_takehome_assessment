from fastapi import APIRouter, Response, status
from fastapi.responses import StreamingResponse
from typing import Dict, Any, Iterator
import json

from ..schemas.message import ChatRequest
from ..llm.mock import MockLLM
from ..tools.registry import REGISTRY
from ..safety.guard import is_denied
from ..telemetry.trace import start_span

router = APIRouter(prefix="", tags=["chat"])

# NOTE: This is a minimal reference. You should make it stream tokens and handle tool loops more richly.
@router.post("/chat")
def chat(req: ChatRequest):
    span = start_span("chat")
    llm = MockLLM()  # In real impl, inject via provider

    # Basic deny gate
    last_user = req.messages[-1].content if req.messages else ""
    if is_denied(last_user):
        span.event("safety_block", reason="denylist")
        meta = {"error": "request denied"}
        return Response(json.dumps(meta), status_code=status.HTTP_400_BAD_REQUEST, media_type="application/json" )

    # One-shot: call LLM once, if tool_call then execute, then return final text JSON.
    span.event("llm_request")
    out = llm.complete([m.model_dump() for m in req.messages])
    if out.get("tool_call"):
        span.event("tool_call", name=out["tool_call"]["name"])
        tc = out["tool_call"]
        fn = REGISTRY.get(tc["name"])
        result = fn(**tc["arguments"]) if fn else {"answer": "tool not found", "citations": []}
        # Return final merged message
        meta = {"text": result.get("answer"), "citations": result.get("citations"), "trace_id": span.trace_id}
        return Response(json.dumps(meta), media_type="application/json")
    else:
        meta = {"text": out.get("content"), "citations": [], "trace_id": span.trace_id}
        return Response(json.dumps(meta), media_type="application/json")
