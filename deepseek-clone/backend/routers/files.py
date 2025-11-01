from typing import Dict

from fastapi import APIRouter, File, UploadFile

router = APIRouter(prefix="/api/files", tags=["files"])


@router.post('/upload')
async def upload_file(file: UploadFile = File(...)) -> Dict[str, str]:
    contents = await file.read()
    summary = f"Received {file.filename} ({file.content_type}) with {len(contents)} bytes."
    return {"summary": summary}
