# DeepSeek Clone Architecture Overview

This document summarises the high-level architecture of the DeepSeek AI interface clone.

## Frontend
- **Framework**: Next.js 14 with the App Router and TypeScript for type-safe React components.
- **Styling**: Tailwind CSS backed by CSS variables mirroring the DeepSeek palette.
- **State**: Client-side session state persisted with `localStorage` helpers in `lib/storage.ts`.
- **Streaming UX**: Chat responses are streamed from the `/api/chat` route handler, simulating token-by-token delivery.
- **File Support**: Drag-and-drop uploads implemented with `react-dropzone` and forwarded to the API mock endpoint.
- **Search Integration**: `/api/search` provides stubbed results for rapid prototyping of retrieval-augmented flows.

## Backend
- **FastAPI** app defined in `backend/api/main.py` with routers per domain.
- **Services**: `ChatService` composes deterministic replies while background tasks leverage Celery with Redis.
- **Extensibility**: Routers for chat history, web search, and model listings align with the specification for future upgrades.

## Data Layer
- **PostgreSQL** schema scripted in `database/schema.sql` to persist users, conversations, messages, and files.
- **Vector Store**: Placeholder for ChromaDB integration; the schema is structured to attach embeddings per message.

## Deployment
- **Frontend**: Suitable for Vercel deployment using default Next.js build commands.
- **Backend**: Deployable on Render/Railway with Uvicorn (`uvicorn backend.api.main:app --host 0.0.0.0 --port 8000`).
- **Workers**: Celery tasks triggered via `celery -A backend.services.tasks.celery_app worker --loglevel=info` connected to Redis.

The repository skeleton mirrors production concerns while remaining light-weight for experimentation.
