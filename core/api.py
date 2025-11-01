"""FastAPI backend exposing WebSocket feeds for the Streamlit UI."""

from __future__ import annotations

import asyncio
import json
from typing import Any, AsyncIterator, Dict, List

from fastapi import FastAPI, WebSocket

from .kafka_pipeline import KafkaPipeline, bootstrap_pipeline
from .secops_stream_processor import process_stream


class SecOpsBackend:
    """Manage state shared between the FastAPI app and Streamlit frontend."""

    def __init__(self) -> None:
        self.pipeline = KafkaPipeline()
        bootstrap_pipeline(self.pipeline, sample_size=5)
        self.listeners: List[WebSocket] = []

    async def broadcast(self) -> None:
        """Continuously process pipeline events and publish to connected clients."""

        while True:
            events = self.pipeline.drain()
            if events:
                enriched = process_stream(events)
                payload = json.dumps(enriched)
                for socket in list(self.listeners):
                    await socket.send_text(payload)
            await asyncio.sleep(1)

    async def register(self, websocket: WebSocket) -> AsyncIterator[None]:
        """Context manager for WebSocket clients."""

        await websocket.accept()
        self.listeners.append(websocket)
        try:
            while True:
                await websocket.receive_text()
        except Exception:  # pragma: no cover - network disconnect
            pass
        finally:
            self.listeners.remove(websocket)


def build_app() -> FastAPI:
    """Instantiate the FastAPI application for use in deployment."""

    backend = SecOpsBackend()
    app = FastAPI(title="AI SecOps Backend")

    @app.on_event("startup")
    async def _startup() -> None:
        asyncio.create_task(backend.broadcast())

    @app.websocket("/events")
    async def websocket_endpoint(websocket: WebSocket) -> None:  # pragma: no cover - websocket flow
        async for _ in backend.register(websocket):
            pass

    return app
