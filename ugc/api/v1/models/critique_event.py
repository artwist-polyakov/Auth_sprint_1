from pydantic import BaseModel, Field


class CritiqueEventSchema(BaseModel):
    rating: int = Field(..., ge=1, le=10)
    content: str
