from typing import Annotated

import typer
import rich

from amdb.application.common.interfaces.identity_provider import IdentityProvider
from amdb.application.commands.create_person import CreatePersonCommand
from amdb.presentation.handler_factory import HandlerFactory


person_commands = typer.Typer(name="person")


@person_commands.command()
def create(
    ctx: typer.Context,
    name: Annotated[
        str,
        typer.Argument(
            help="Name that will be used to [green]create[/green] person.",
        ),
    ],
    silently: Annotated[
        bool,
        typer.Option(
            help="[green]Create[/green] person without printing any information.",
        ),
    ] = False,
) -> None:
    """
    [green]Create[/green] person.

    If --silently is not used, will print movie id.
    """
    ioc: HandlerFactory = ctx.obj["ioc"]
    identity_provider: IdentityProvider = ctx.obj["identity_provider"]

    with ioc.create_person(identity_provider) as create_person_handler:
        create_person_command = CreatePersonCommand(
            name=name,
        )
        person_id = create_person_handler.execute(create_person_command)

    if not silently:
        rich.print(person_id)
