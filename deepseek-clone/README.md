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

This scaffold provides a production-style baseline while remaining lightweight enough for rapid iteration.
