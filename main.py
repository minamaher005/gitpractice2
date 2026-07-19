from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import Item, ItemCreate, ItemUpdate
from database import db

app = FastAPI(
    title="Items API",
    description="A simple FastAPI CRUD application",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── CREATE ──────────────────────────────────────────────────────────────────
@app.post("/items/", response_model=Item, status_code=201, tags=["Items"])
def create_item(item: ItemCreate):
    """Create a new item."""
    return db.create(item)


# ── READ (all) ───────────────────────────────────────────────────────────────
@app.get("/items/", response_model=list[Item], tags=["Items"])
def list_items(skip: int = 0, limit: int = 100):
    """Return all items (with optional pagination)."""
    return db.get_all(skip=skip, limit=limit)


# ── READ (one) ───────────────────────────────────────────────────────────────
@app.get("/items/{item_id}", response_model=Item, tags=["Items"])
def get_item(item_id: int):
    """Return a single item by ID."""
    item = db.get(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
    return item


# ── UPDATE ───────────────────────────────────────────────────────────────────
@app.put("/items/{item_id}", response_model=Item, tags=["Items"])
def update_item(item_id: int, data: ItemUpdate):
    """Fully update an item by ID."""
    item = db.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
    return item


# ── DELETE ───────────────────────────────────────────────────────────────────
@app.delete("/items/{item_id}", status_code=204, tags=["Items"])
def delete_item(item_id: int):
    """Delete an item by ID."""
    if not db.delete(item_id):
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")


# ── HEALTH ────────────────────────────────────────────────────────────────────
@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok", "total_items": db.count()}
