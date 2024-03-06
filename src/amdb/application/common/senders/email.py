from typing import Protocol

from amdb.application.common.entities.file import File


class SendEmail(Protocol):
    def __call__(
        self,
        *,
        email: str,
        subject: str,
        files: list[File],
    ) -> None:
        raise NotImplementedError
