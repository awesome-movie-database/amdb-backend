import typer

from amdb.presentation.cli.setup import setup_typer_command_handlers
from amdb.main.config import GenericConfig
from .di import create_dependencies_dict


def create_app(generic_config: GenericConfig) -> typer.Typer:
    app = typer.Typer(
        rich_markup_mode="rich",
        context_settings={"obj": create_dependencies_dict(generic_config)},
    )
    setup_typer_command_handlers(app)

    return app
