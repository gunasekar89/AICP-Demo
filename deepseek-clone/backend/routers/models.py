from typing import Dict, List

from fastapi import APIRouter

router = APIRouter(prefix="/api", tags=["models"])

MODELS = [
    {"id": "gpt-4-turbo", "name": "GPT-4 Turbo", "context_window": 128_000},
    {"id": "deepseek-reasoner", "name": "DeepSeek Reasoner", "context_window": 131_072},
    {"id": "deepseek-coder", "name": "DeepSeek Coder", "context_window": 65_536},
]


@router.get('/models')
async def list_models() -> Dict[str, List[Dict[str, object]]]:
    return {"models": MODELS}
