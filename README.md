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

## Deploy to Render

Quick steps to deploy this app to Render (using GitHub):

1. Commit and push this repository to GitHub (branch `main`).

2. On Render (https://render.com), create a new **Web Service** and connect your GitHub repo.

3. Use these settings when prompted:

 - **Environment:** `Python`
 - **Build Command:** `pip install -r requirements.txt`
 - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
 - **Region/Branch:** as desired (e.g., `main`)

4. Optionally add the `render.yaml` file present in the repo to enable IaC-style configuration. Render will pick it up for automatic service configuration.

5. After deploy completes, visit the service URL provided by Render. The API docs will be available at `/docs` on that URL.

Notes:

 - Render will set the `PORT` environment variable automatically; the start command uses it.
 - If you prefer Docker-based deployment, add a `Dockerfile` and select Docker on Render when creating the service.

## GitHub Actions (CI) and automatic Render deploy

This repo includes a GitHub Actions workflow at `.github/workflows/ci-deploy.yml` which runs on pushes to `main`.

What it does:
- Checks out the code, sets up Python, installs dependencies, and runs a simple lint step (`flake8`).
- If you set these GitHub repository secrets, it will trigger a deploy on Render automatically:
  - `RENDER_API_KEY` — your Render API key (create a service account API key on Render).
  - `RENDER_SERVICE_ID` — the Render Service ID for your web service (found in Render dashboard URL or service settings).

To enable automatic deploys:
1. Go to your GitHub repo Settings → Secrets → Actions and add `RENDER_API_KEY` and `RENDER_SERVICE_ID`.
2. Push to `main` — the workflow will run and trigger a deploy on Render (if secrets present).

## Quick deploy (fast) — options

Choose one of the following quick paths to deploy fast on Render:

Option A — Connect GitHub repo (recommended):

1. Commit and push this repo to GitHub (branch `main`):

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin git@github.com:YOUR_USER/YOUR_REPO.git
git push -u origin main
```

2. In Render, create a new **Web Service** and connect your GitHub repo. Use the start command:
```
uvicorn main:app --host 0.0.0.0 --port $PORT
```

Option B — Trigger a deploy via Render API (fastest if repo already on Render):

1. Ensure the repository is connected to the Render service already (or create the service once via the Render UI).
2. Run the included script (you need `jq` installed locally):

```bash
RENDER_API_KEY=your_api_key RENDER_SERVICE_ID=your_service_id ./deploy_render.sh
```

Option C — Use Docker (push to Render as a Docker service):

1. Build and test locally:
```bash
docker build -t fastapi-crud:latest .
docker run -p 8000:8000 fastapi-crud:latest
```
2. Push to a registry (Docker Hub, GitHub Container Registry) and point Render to that image, or configure Render to build from the repo using the included `Dockerfile`.

---

If you want, I can prepare a Git commit and show the exact commands to push to your GitHub repo (you'll need to replace the remote URL). Tell me whether you want me to create the initial commit and push, or whether you'll push from your machine.

