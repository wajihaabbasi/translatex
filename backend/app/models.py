from pydantic import BaseModel, Field

class TranslationRequest(BaseModel):
    text: str = Field(..., description="The raw source text intended to translate", min_length=1)
    target_lang: str = Field(..., description="The definitive chosen target language choice string")