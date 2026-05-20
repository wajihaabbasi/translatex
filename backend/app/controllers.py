import os
import json
from datetime import datetime
from fastapi import HTTPException
from app.config import client, HISTORY_FILE
from app.models import TranslationRequest

def fetch_local_history_records() -> list:
    """Reads saved data objects securely out of local storage history arrays."""
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as file_stream:
                return json.load(file_stream)
        except (json.JSONDecodeError, IOError):
            return []
    return []

def commit_history_transaction(source: str, translation: str, target_lang: str) -> None:
    """Inserts a fresh records packet cleanly at position zero inside our storage array."""
    history = fetch_local_history_records()
    
    new_record = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "source": source,
        "translation": translation,
        "lang": target_lang
    }
    history.insert(0, new_record)
    
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as file_stream:
            json.dump(history, file_stream, indent=2, ensure_ascii=False)
    except IOError as error:
        print(f"Non-Fatal System Storage Exception: Failed to append logs: {error}")

async def execute_text_translation(payload: TranslationRequest) -> dict:
    """Executes the asynchronous connection to the Groq server and handles history logging."""
    try:
        response = await client.chat.completions.create(
            model="gemini-3.5-flash",
            messages=[
                {
                    "role": "system",
                    "content": (
                        f"You are an expert utility translation tool. Translate the user's text cleanly "
                        f"into {payload.target_lang}. Return only the final translation. Do not add intro, "
                        f"meta-commentary, notes, or wrap text inside conversational paragraphs."
                    )
                },
                {"role": "user", "content": payload.text}
            ],
            temperature=0.2,
        )
        
        translated_result = response.choices[0].message.content.strip()
        
        # Log to tracking histories
        commit_history_transaction(payload.text, translated_result, payload.target_lang)
        
        return {"translation": translated_result}
        
    except Exception as network_error:
        raise HTTPException(
            status_code=500, 
            detail=f"Downstream Groq Infrastructure Disconnection: {str(network_error)}"
        )