from pydantic import BaseModel


class BaseSchema(BaseModel):
    def update(self, data: dict):
        update = self.dict()
        update.update(data)
        for k, v in self.validate(update).dict(exclude_defaults=True).items():
            setattr(self, k, v)
        return self
