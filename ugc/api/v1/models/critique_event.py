from pydantic import BaseModel


class CritiqueEventSchema(BaseModel):
    rating: int
    content: str
