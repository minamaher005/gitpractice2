"""
In-memory "database" – replace with SQLAlchemy / MongoDB / etc. as needed.
"""
from datetime import datetime, timezone
from typing import Optional
from models import Item, ItemCreate, ItemUpdate


def _now() -> datetime:
    return datetime.now(timezone.utc)


class InMemoryDB:
    def __init__(self):
        self._store: dict[int, Item] = {}
        self._next_id: int = 1

    # ── CREATE ────────────────────────────────────────────────────────────────
    def create(self, data: ItemCreate) -> Item:
        now = _now()
        item = Item(
            id=self._next_id,
            created_at=now,
            updated_at=now,
            **data.model_dump(),
        )
        self._store[self._next_id] = item
        self._next_id += 1
        return item

    # ── READ ──────────────────────────────────────────────────────────────────
    def get(self, item_id: int) -> Optional[Item]:
        return self._store.get(item_id)

    def get_all(self, skip: int = 0, limit: int = 100) -> list[Item]:
        items = list(self._store.values())
        return items[skip : skip + limit]

    # ── UPDATE ────────────────────────────────────────────────────────────────
    def update(self, item_id: int, data: ItemUpdate) -> Optional[Item]:
        existing = self._store.get(item_id)
        if existing is None:
            return None
        updated = existing.model_copy(
            update={**data.model_dump(), "updated_at": _now()}
        )
        self._store[item_id] = updated
        return updated

    # ── DELETE ────────────────────────────────────────────────────────────────
    def delete(self, item_id: int) -> bool:
        if item_id not in self._store:
            return False
        del self._store[item_id]
        return True

    # ── MISC ──────────────────────────────────────────────────────────────────
    def count(self) -> int:
        return len(self._store)


# Singleton instance shared across the app
db = InMemoryDB()
