from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Item(BaseModel):
    id: int
    name: str
    description: str | None = None

items_db: List[Item] = [
    Item(id=1, name="Item 1", description="Description for Item 1"),
    Item(id=2, name="Item 2", description="Description for Item 2"),
]

@app.head("/items/{item_id}", status_code=status.HTTP_200_OK)
def head_item(item_id: int):
    """
    Checks if an item with the given ID exists.
    Raises HTTP 404 if not found.
    """
    if not any(item.id == item_id for item in items_db):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return 
