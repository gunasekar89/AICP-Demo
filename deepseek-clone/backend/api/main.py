from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ..routers import chat, files, history, search, models
from ..services.health import router as health_router


def create_app() -> FastAPI:
    app = FastAPI(title="DeepSeek Clone API", version="0.1.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health_router)
    app.include_router(chat.router)
    app.include_router(files.router)
    app.include_router(history.router)
    app.include_router(search.router)
    app.include_router(models.router)

    return app


app = create_app()
