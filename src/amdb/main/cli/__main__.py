import typer

from amdb.infrastructure.database.builders import (
    build_engine,
    build_session_factory,
    BuildGatewayFactory,
)
from amdb.infrastructure.in_memory.permissions_gateway import InMemoryPermissionsGateway
from amdb.infrastructure.auth.raw.identity_provider import RawIdentityProvider
from amdb.presentation.cli.setup import setup_typer_command_handlers
from amdb.main.config import build_generic_config
from amdb.main.ioc import IoC


def main() -> None:
    generic_config = build_generic_config()

    engine = build_engine(generic_config.database)
    session_factory = build_session_factory(engine)

    ioc = IoC(
        build_gateway_factory=BuildGatewayFactory(session_factory),
        permissions_gateway=InMemoryPermissionsGateway(),
    )
    identity_provider = RawIdentityProvider()

    app = typer.Typer(
        rich_markup_mode="rich",
        context_settings={"obj": {"ioc": ioc, "identity_provider": identity_provider}},
    )
    setup_typer_command_handlers(app)

    app()


main()
