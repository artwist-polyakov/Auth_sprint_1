from abc import ABC

from pydantic import BaseModel


class Answer(ABC):
    pass


class BaseAnswerModel(BaseModel):
    pass
