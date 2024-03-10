from typing import Protocol


class UnitOfWork(Protocol):
    def commit(self) -> None:
        raise NotImplementedError
