from fastapi import APIRouter
from app.models import TranslationRequest
from app.controllers import execute_text_translation, fetch_local_history_records

router = APIRouter()

@router.post("/translate")
async def handle_translation(payload: TranslationRequest):
    """Primary translation submission pipeline."""
    return await execute_text_translation(payload)

@router.get("/history")
def handle_history_retrieval():
    """Fetches the translation history log."""
    return fetch_local_history_records()