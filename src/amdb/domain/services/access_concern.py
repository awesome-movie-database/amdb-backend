class AccessConcern:
    def authorize(
        self,
        current_permissions: int,
        required_permissions: int,
    ) -> bool:
        return (
            current_permissions & required_permissions == required_permissions
        )
