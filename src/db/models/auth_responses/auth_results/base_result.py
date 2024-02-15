from abc import ABC


class BaseSuccess(ABC):
    # пользователь создан
    pass


class BaseFailure(ABC):
    pass


class BaseResult(ABC):
    # возвращает результат работы UserRepository
    # содержит Failure и Success - в одной переменной. if Success... else...
    def __init__(self):
        self.answer_type: BaseSuccess | BaseFailure
