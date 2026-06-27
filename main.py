from typing import Dict, List, Optional
from fastapi import FastAPI, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

# Initialize the FastAPI application
# FastAPI will automatically generate Swagger documentation at http://127.0.0.1:8000/docs
app = FastAPI(
    title="Simple CRUD API",
    description="A simple in-memory CRUD API using FastAPI to learn core concepts",
    version="1.0.0"
)

# Mount static files for a minimal UI and serve index at root
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=FileResponse)
def root() -> FileResponse:
    """Serve the single-page static UI."""
    return FileResponse("static/index.html")

# In-memory "database" representing our items.
# Key is the item ID (int), value is the item data dictionary.
items_db: Dict[int, dict] = {}
# Counter to generate unique sequential IDs
current_id = 1


# --- PYDANTIC SCHEMAS ---
# Pydantic is used for data validation, serialization, and automatic documentation generation.

class ItemBase(BaseModel):
    """
    Base schema containing fields shared between creation, updating, and retrieval.
    """
    name: str = Field(..., example="Wireless Mouse", description="The name of the item")
    description: Optional[str] = Field(None, example="Ergonomic 2.4GHz wireless mouse", description="A description of the item")
    price: float = Field(..., gt=0, example=29.99, description="The price of the item (must be greater than 0)")
    tax: Optional[float] = Field(None, example=2.5, description="Associated tax for the item")


class ItemCreate(ItemBase):
    """
    Schema for creating an item. The client doesn't provide an ID; the server will generate it.
    """
    pass


class ItemUpdate(BaseModel):
    """
    Schema for updating an item. All fields are optional so client can update only a subset.
    """
    name: Optional[str] = Field(None, example="Super Wireless Mouse")
    description: Optional[str] = Field(None, example="Enhanced ergonomic mouse")
    price: Optional[float] = Field(None, gt=0, example=34.99)
    tax: Optional[float] = Field(None, example=3.0)


class ItemResponse(ItemBase):
    """
    Schema for returning an item to the client. Includes the server-generated ID.
    """
    id: int = Field(..., example=1, description="The unique database ID of the item")


# --- API ENDPOINTS (CRUD Operations) ---

# 1. CREATE (POST)
@app.post(
    "/items/",
    response_model=ItemResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new item"
)
def create_item(item: ItemCreate):
    """
    Creates a new item and stores it in the in-memory database.
    
    - **name**: Name of the item (Required)
    - **description**: Description of the item (Optional)
    - **price**: Price of the item (Required)
    - **tax**: Tax amount (Optional)
    """
    global current_id
    
    # Check if we already have an item with the same name to prevent duplicates (optional logic)
    for stored_item in items_db.values():
        if stored_item["name"].lower() == item.name.lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"An item with the name '{item.name}' already exists."
            )
            
    # Convert Pydantic model to a standard dictionary
    new_item_data = item.dict()
    # Assign the new sequential ID
    new_item_data["id"] = current_id
    
    # Save the item in our mock database
    items_db[current_id] = new_item_data
    
    # Increment the ID counter for the next item
    current_id += 1
    
    # Return the newly created item (which matches the ItemResponse schema)
    return new_item_data


# 2. READ ALL (GET)
@app.get(
    "/items/",
    response_model=List[ItemResponse],
    status_code=status.HTTP_200_OK,
    summary="Get all items"
)
def read_items():
    """
    Retrieves all items stored in the in-memory database.
    """
    # Convert dictionary values to a list of dicts
    return list(items_db.values())


# 3. READ ONE (GET)
@app.get(
    "/items/{item_id}",
    response_model=ItemResponse,
    status_code=status.HTTP_200_OK,
    summary="Get item by ID"
)
def read_item(item_id: int):
    """
    Retrieves a single item using its unique ID.
    
    Raises a **404 Not Found** error if the item does not exist.
    """
    if item_id not in items_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {item_id} not found"
        )
    return items_db[item_id]


# 4. UPDATE (PUT)
@app.put(
    "/items/{item_id}",
    response_model=ItemResponse,
    status_code=status.HTTP_200_OK,
    summary="Update an existing item"
)
def update_item(item_id: int, item_update: ItemUpdate):
    """
    Updates the fields of an existing item.
    
    - Only fields provided in the request body will be updated.
    - Raises a **404 Not Found** error if the item does not exist.
    """
    if item_id not in items_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {item_id} not found"
        )
        
    # Get the existing item data
    existing_item = items_db[item_id]
    
    # Extract only the fields that the client sent (ignore None values)
    update_data = item_update.dict(exclude_unset=True)
    
    # Apply changes to the existing item data
    for key, value in update_data.items():
        existing_item[key] = value
        
    # Save the updated data back to the database
    items_db[item_id] = existing_item
    
    return existing_item


# 5. DELETE (DELETE)
@app.delete(
    "/items/{item_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete an item by ID"
)
def delete_item(item_id: int):
    """
    Deletes an item from the database.
    
    Raises a **404 Not Found** error if the item does not exist.
    """
    if item_id not in items_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {item_id} not found"
        )
        
    # Remove the item from the dictionary
    deleted_item = items_db.pop(item_id)
    
    # Return a confirmation message
    return {"message": f"Item '{deleted_item['name']}' with ID {item_id} has been deleted successfully."}
