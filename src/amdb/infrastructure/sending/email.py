from amdb.application.common.entities.file import File


class SendFakeEmail:
    def __call__(
        self,
        *,
        email: str,
        subject: str,
        files: list[File],
    ) -> None:
        print(  # noqa
            "Email has been sent. \n"
            f"Address: {email} \n"
            f"Subject: {subject} \n"
            f"Number of file: {len(files)}",
        )
