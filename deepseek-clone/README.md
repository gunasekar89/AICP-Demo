# DeepSeek AI Web Interface Clone

This directory contains a full-stack reference implementation inspired by the DeepSeek AI assistant. It covers the frontend chat experience, FastAPI backend, database schema, and background task scaffolding requested in the project brief.

## Structure

```
frontend/   # Next.js 14 application with chat UI, file uploads, and API routes
backend/    # FastAPI service exposing chat, search, and file processing endpoints
database/   # PostgreSQL schema for users, conversations, messages, and files
docs/       # Architecture overview and supplementary documentation
```

## Frontend Quickstart

```bash
cd frontend
npm install
npm run dev
```

The application starts on `http://localhost:3000` with a responsive chat layout, markdown rendering, mock streaming responses, drag-and-drop uploads, and a settings drawer.

## Backend Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
uvicorn backend.api.main:app --reload
```

Endpoints available under `http://localhost:8000/api/*` provide chat completions, file upload summaries, search stubs, model listings, and health checks.

## Background Workers

A Celery worker is configured to use Redis as both broker and backend:

```bash
celery -A backend.services.tasks.celery_app worker --loglevel=info
```

## Database

Apply the schema using any PostgreSQL-compatible tool:

```bash
psql $DATABASE_URL -f database/schema.sql
```

The schema mirrors the relationships required for session management, attachments, and contextual retrieval.

## Deployment

- **Frontend**: Deploy to Vercel using the default `npm run build` pipeline.
- **Backend**: Deploy to Render or Railway with the Uvicorn command shown above.
- **Storage**: Integrate AWS S3 or Cloudflare R2 for persistent file storage.
- **Vector DB**: Swap in a managed ChromaDB or Pinecone instance and connect through the `ChatService`.

## Running on macOS

The project runs natively on Apple Silicon and Intel Macs. Install the prerequisites and start the services from separate shells:

1. **Install dependencies** (requires [Homebrew](https://brew.sh/)):

   ```bash
   brew install node@20 python@3.11 redis postgresql
   npm install --global pnpm # optional package manager used by some teams
   ```

2. **Prepare the backend**:

   ```bash
   cd backend
   python3.11 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   uvicorn backend.api.main:app --reload
   ```

3. **Start Redis and PostgreSQL** (if you are running them locally):

   ```bash
   brew services start redis
   brew services start postgresql
   createdb deepseek_clone
   psql deepseek_clone -f ../database/schema.sql
   ```

4. **Run the frontend** from a new terminal:

   ```bash
   cd frontend
   npm install
   npm run dev
   ```

5. **Optional: launch Celery worker** once Redis is available:

   ```bash
   cd backend
   source .venv/bin/activate
   celery -A backend.services.tasks.celery_app worker --loglevel=info
   ```

With these commands the frontend is available at `http://localhost:3000` and the FastAPI backend at `http://localhost:8000` on macOS.

This scaffold provides a production-style baseline while remaining lightweight enough for rapid iteration.

## One-Command Startup

For a Docker-based workflow you can launch the entire stack (frontend, backend, worker, Redis, and PostgreSQL) with the helper script:

```bash
./run.sh --build   # run from the deepseek-clone/ directory
```

The script auto-detects whether to use `docker compose` or `docker-compose`, creates a `.env` file from `.env.example` if needed, and forwards any additional arguments to `docker compose up`.
