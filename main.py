from fastapi import FastAPI, HTTPException, status
from typing import Union, Optional
from pydantic import BaseModel

app = FastAPI()

# Grocery items
grocery_items = {
    1: {"name": "Apples", "price": 500},
    2: {"name": "Bananas", "price": 1000},
    3: {"name": "Milk", "price": 2500},
    4: {"name": "Noodles", "price": 6500},
    5: {"name": "Detergent", "price": 1200}
}

class GroceryItem(BaseModel):
    name: str
    price: float

@app.get("/items")
async def get_items():
    return grocery_items

@app.get("/grocery_items/{item_id}/", response_model=GroceryItem)  # Removed "api" segment
def get_item(item_id: int):
    try:
        return grocery_items[item_id]
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )

@app.delete("/api/grocery_items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int):
    try:
        del grocery_items[item_id]
    except KeyError:
        raise HTTPException(
            status_code=404, detail=f'Item with id:{item_id} was not found!'
        )   

@app.post("/api/grocery_items", status_code=status.HTTP_201_CREATED)
def create_item(new_item: GroceryItem):
    item_id = max(grocery_items.keys()) + 1
    grocery_items[item_id] = new_item.model_dump()
    return grocery_items[item_id]

@app.put("/api/grocery_items/{item_id}/")
def update_item(item_id: int, updated_item: GroceryItem):
    try:
        item = grocery_items[item_id]
        item["name"] = updated_item.name
        item["price"] = updated_item.price
        return grocery_items
    except KeyError:
        raise HTTPException(
            status_code-404, detail=f'Item with id:{item_id} was not found!'
        )

