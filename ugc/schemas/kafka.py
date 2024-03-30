from schemas.base import BaseSchema


class KafkaRepositoryProducerSchema(BaseSchema):
    topic: str
    key: str
    value: str

    class Config:
        orm_mode = True


class KafkaRepositoryConsumerSchema(BaseSchema):
    topic: str
    auto_offset_reset: str | None
    group_id: str

    class Config:
        orm_mode = True
