from typing import Dict

from fastapi import APIRouter

router = APIRouter(prefix="/api/chat", tags=["history"])


@router.get('/history')
async def get_history() -> Dict[str, str]:
    return {"status": "ok", "message": "History endpoint placeholder"}


@router.delete('/{session_id}')
async def delete_history(session_id: str) -> Dict[str, str]:
    return {"status": "deleted", "session_id": session_id}
