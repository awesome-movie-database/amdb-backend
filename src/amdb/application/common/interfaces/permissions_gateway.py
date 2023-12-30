from typing import Protocol


class PermissionsGateway(Protocol):
    def for_create_movie(self) -> int:
        raise NotImplementedError
    
    def for_rate_movie(self) -> int:
        raise NotImplementedError
