import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.mark.xfail(reason="streaming not enforced; reference only", strict=False)
def test_streaming_contract():
    client = TestClient(app)
    body = {
        "thread_id": "t1",
        "user_id": "u1",
        "messages": [
            {"role":"system","content":"You are a helpful assistant."},
            {"role":"user","content":"Hello"}
        ]
    }
    r = client.post("/chat", json=body, headers={"Accept":"text/plain"})
    assert r.status_code == 200
    # Future: iterate over stream chunks
