from pydantic import BaseModel


class KafkaModel(BaseModel):
    topic: str
    key: str
    value: str
