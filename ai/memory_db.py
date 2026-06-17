"""
ADVANCED CHALLENGE — Follower Memory Database
---------------------------------------------
Persists a per-follower profile so the actor can personalise replies.
Schema matches the brief:
    {"user": "John", "favorite_team": "Brazil", "last_comment": "Brazil will win!"}
Stored as JSON on disk.
"""
from __future__ import annotations
import json
import re
import time
import config
from data import TEAMS


class MemoryDB:
    def __init__(self, path=None):
        self.path = path or config.MEMORY_FILE
        self.db = self._load()

    def _load(self):
        try:
            return json.loads(self.path.read_text(encoding="utf-8"))
        except Exception:
            return {}

    def _save(self):
        self.path.write_text(json.dumps(self.db, ensure_ascii=False, indent=2), encoding="utf-8")

    def remember(self, user, **fields):
        prof = self.db.get(user, {"user": user})
        prof.update(fields)
        # infer favourite team from the comment if not known
        if not prof.get("favorite_team") and fields.get("last_comment"):
            for t in TEAMS:
                if re.search(rf"\b{re.escape(t['name'])}\b", fields["last_comment"], re.I):
                    prof["favorite_team"] = t["name"]
                    break
        prof["updated"] = time.time()
        self.db[user] = prof
        self._save()
        return prof

    def get(self, user):
        return self.db.get(user)

    def list(self):
        return list(self.db.values())

    def clear(self):
        self.db = {}
        self._save()
