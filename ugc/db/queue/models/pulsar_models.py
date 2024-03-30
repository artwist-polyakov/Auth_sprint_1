from pydantic import BaseModel


class PulsarModel(BaseModel):
    topic: str
