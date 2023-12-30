from typing import Protocol


class UnitOfWork(Protocol):
    def flush(self) -> None:
        raise NotImplementedError

    def commit(self) -> None:
        raise NotImplementedError
    
    def rollback(self) -> None:
        raise NotImplementedError
