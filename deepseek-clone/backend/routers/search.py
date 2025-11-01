from typing import Dict, List

from fastapi import APIRouter

router = APIRouter(prefix="/api/search", tags=["search"])

MOCK_SEARCH_RESULTS = [
    "Summarised latest cybersecurity trends from trusted sources.",
    "Aggregated benchmark data with inline citations.",
    "Step-by-step code examples compiled for rapid prototyping.",
]


@router.post('/web')
async def web_search(query: Dict[str, str]) -> Dict[str, List[str]]:
    term = query.get("query", "").strip()
    if not term:
        return {"results": []}
    results = [f"{item} (query: {term})" for item in MOCK_SEARCH_RESULTS]
    return {"results": results}
