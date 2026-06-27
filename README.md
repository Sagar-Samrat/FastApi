# Learn CRUD with FastAPI 🚀

Welcome! This is a simple, beginner-friendly project designed to help you understand how **CRUD** (Create, Read, Update, Delete) operations work in a web API using **FastAPI**.

To make learning as easy as possible, this project uses a single file `main.py` with an **in-memory database** (a Python dictionary). This avoids the complexity of setting up SQL databases or running migration files, letting you focus entirely on the API structure.

---

## What is CRUD?

CRUD stands for the four basic operations of persistent storage:

| Operation | Description | HTTP Method | Endpoint Example |
| :--- | :--- | :--- | :--- |
| **C**reate | Adds a new item to the database | `POST` | `/items/` |
| **R**ead (All) | Retrieves a list of all items | `GET` | `/items/` |
| **R**ead (One) | Retrieves a single item by its ID | `GET` | `/items/{item_id}` |
| **U**pdate | Modifies an existing item by its ID | `PUT` | `/items/{item_id}` |
| **D**elete | Removes an item by its ID | `DELETE` | `/items/{item_id}` |

---

## Getting Started

### 1. Installation

First, make sure you have the required packages installed. Open your terminal in this directory and run:

```bash
pip install -r requirements.txt
```

### 2. Running the Application

Start the local development server using **Uvicorn**:

```bash
uvicorn main:app --reload
```

* `--reload`: Tells uvicorn to restart the server automatically whenever you make changes to your code.
* `main:app`: Refers to the `app` instance in `main.py`.

Once the server is running, you will see output like this:
```text
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

---

## 3. Interactive API Documentation (Swagger UI) 🛠️

One of FastAPI's best features is its automatic interactive documentation. 

1. Open your browser and go to: **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**
2. You will see a beautiful web page listing all 5 endpoints.
3. You can click on any endpoint, click **"Try it out"**, fill in the parameters/body, and click **"Execute"** to send live requests to your app!

---

## Code Walkthrough

Open [main.py](file:///Users/sagarsamrat/Desktop/FastApi/main.py) to read through the implementation. Here's a brief summary of what's inside:

* **FastAPI App Initialization**: `app = FastAPI(...)` sets up the core routing engine.
* **In-Memory database**: `items_db` is a simple dictionary where key-value pairs are stored. Since it is in-memory, restarting the server will reset the database back to empty.
* **Pydantic Schemas**:
  * `ItemCreate`: What is required from the user to create a new item (excludes `id` since the server generates it).
  * `ItemUpdate`: Allows updating specific fields (all fields are optional).
  * `ItemResponse`: Defines the exact structure returned to the client (includes the generated `id`).
* **Endpoints**: Decorated with `@app.post()`, `@app.get()`, `@app.put()`, and `@app.delete()`.
