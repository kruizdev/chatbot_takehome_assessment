"""TODO: Implement durable memory using SQLite (or LevelDB).
Requirements:
 - persist last N tokens per thread_id
 - role-aware truncation (keep 'system')
 - idempotent append by message id
 - survive process restart (backed by file db)
"""
import sqlite3
from typing import List
from .base import IMemory, StoredMessage

class SQLiteMemory(IMemory):
    def __init__(self, path: str = "memory.db"):
        self.path = path
        self._init()

    def _init(self):
        self.conn = sqlite3.connect(self.path, isolation_level=None, check_same_thread=False)
        cur = self.conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS messages(
  thread_id TEXT,
  id TEXT,
  role TEXT,
  content TEXT,
  tokens INTEGER,
  PRIMARY KEY (thread_id, id)
)""")
        self.conn.commit()

    def get_thread(self, thread_id: str) -> List[StoredMessage]:
        # TODO
        raise NotImplementedError

    def append(self, thread_id: str, message: StoredMessage, max_tokens: int) -> None:
        # TODO: insert if not exists; then call truncate
        raise NotImplementedError

    def truncate(self, thread_id: str, max_tokens: int) -> None:
        # TODO: implement role-aware truncation keeping 'system' messages
        raise NotImplementedError
