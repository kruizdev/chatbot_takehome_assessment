from app.memory.inmem import InMemory
from app.memory.kv import SQLiteMemory
from app.memory.base import StoredMessage

def test_inmem_truncates_and_keeps_system():
    m = InMemory()
    tid = "T"
    m.append(tid, StoredMessage(id="s", role="system", content="rules", tokens=1), max_tokens=10)
    for i in range(10):
        m.append(tid, StoredMessage(id=f"u{i}", role="user", content="x "*3, tokens=3), max_tokens=10)
        m.append(tid, StoredMessage(id=f"a{i}", role="assistant", content="y "*3, tokens=3), max_tokens=10)
    arr = m.get_thread(tid)
    assert any(mm.role == "system" for mm in arr), "system must be retained"
    assert sum(mm.tokens for mm in arr) <= 10

def test_kv_persists_and_idempotent(tmp_path):
    dbfile = tmp_path / "mem.db"
    kv = SQLiteMemory(path=str(dbfile))
    tid = "T2"
    kv.append(tid, StoredMessage(id="s", role="system", content="rules", tokens=1), max_tokens=6)
    kv.append(tid, StoredMessage(id="u1", role="user", content="hello world", tokens=2), max_tokens=6)
    kv.append(tid, StoredMessage(id="u1", role="user", content="hello world", tokens=2), max_tokens=6)  # dup
    arr = kv.get_thread(tid)
    assert len([m for m in arr if m.id == "u1"]) == 1, "idempotent append"
    # simulate restart
    kv2 = SQLiteMemory(path=str(dbfile))
    arr2 = kv2.get_thread(tid)
    assert len(arr2) == len(arr), "should persist across restart"
