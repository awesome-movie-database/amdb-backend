from typing import Callable


class Stub:
    def __init__(self, dependency: Callable) -> None:
        self.dependency = dependency

    def __call__(self) -> None:
        raise NotImplementedError

    def __eq__(self, value: object) -> bool:
        if isinstance(value, Stub):
            return self.dependency == value.dependency
        return False

    def __hash__(self) -> int:
        return hash(self.dependency)
