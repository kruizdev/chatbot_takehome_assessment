import json, pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.mark.xfail(reason="/chat streaming + tool loop not fully implemented yet", strict=False)
def test_end_to_end_chat_tool_call():
    client = TestClient(app)
    body = {
        "thread_id": "t1",
        "user_id": "u1",
        "messages": [
            {"role":"system","content":"You are a helpful assistant."},
            {"role":"user","content":"What is Delta's pet policy for dogs? pet policy crate"}
        ]
    }
    r = client.post("/chat", json=body)
    assert r.status_code == 200
    data = r.json()
    assert "crate" in data.get("text",""), data
    assert data.get("citations"), data
