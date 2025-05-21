from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from mangum import Mangum

app = FastAPI()

# Sample data
class Item(BaseModel):
    id: int
    name: str
    description: str = None

items = [
    Item(id=1, name="Item 1", description="Description of Item 1"),
    Item(id=2, name="Item 2", description="Description of Item 2"),
]

# Get all items
@app.get("/items", response_model=List[Item])
def get_items():
    return items

# Get a single item by ID
@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int):
    item = next((item for item in items if item.id == item_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

# Add a new item
@app.post("/items", response_model=Item)
def add_item(item: Item):
    if any(existing_item.id == item.id for existing_item in items):
        raise HTTPException(status_code=400, detail="Item with this ID already exists")
    items.append(item)
    return item

# Update an existing item
@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, updated_item: Item):
    for index, item in enumerate(items):
        if item.id == item_id:
            items[index] = updated_item
            return updated_item
    raise HTTPException(status_code=404, detail="Item not found")

# Delete an item
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    global items
    items = [item for item in items if item.id != item_id]
    return {"message": "Item deleted successfully"}

handler = Mangum(app)
# This handler is used for AWS Lambda integration
# If you're deploying to AWS Lambda, you can use the handler variable
