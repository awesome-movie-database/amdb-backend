class RawPermissionsGateway:
    def for_create_movie(self) -> int:
        return 2

    def for_delete_movie(self) -> int:
        return 2

    def for_rate_movie(self) -> int:
        return 4

    def for_unrate_movie(self) -> int:
        return 4
