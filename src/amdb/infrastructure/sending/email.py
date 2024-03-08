from typing import Protocol

from amdb.application.common.entities.file import File


class SendFakeEmail(Protocol):
    def __call__(
        self,
        *,
        email: str,
        subject: str,
        files: list[File],
    ) -> None:
        ...
