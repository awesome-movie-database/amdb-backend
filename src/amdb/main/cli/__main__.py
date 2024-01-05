from amdb.main.config import build_generic_config
from .app import create_app


def main() -> None:
    generic_config = build_generic_config()

    app = create_app(generic_config)

    app()


main()
