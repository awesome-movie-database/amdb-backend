![Image](/assets/main_banner.png)

<p align="center">
    <a href="https://github.com/Awesome-Movie-Database/amdb-backend/blob/main/LICENSE" target="_blank">
        <img src="https://img.shields.io/github/license/Awesome-Movie-Database/amdb-backend" alt="License">
    </a>
    <a href="https://github.com/astral-sh/ruff">
        <img src="https://img.shields.io/badge/code_style-ruff-%236b00ff" alt="Code style">
    </a>
    <a>
        <img src="https://img.shields.io/github/actions/workflow/status/Awesome-Movie-Database/amdb-backend/lint.yaml?label=mypy" alt="Mypy status">
    </a>
    <a>
        <img src="https://img.shields.io/github/actions/workflow/status/Awesome-Movie-Database/amdb-backend/test.yaml?label=test"
        alt="Test status">
    </a>
    <a href="https://codecov.io/github/Awesome-Movie-Database/amdb-backend" >
        <img src="https://codecov.io/github/Awesome-Movie-Database/amdb-backend/graph/badge.svg?token=7JK9QG9N0X"/>
    </a>
</p>

## Used technologies:

* [Python 3](https://www.python.org/downloads/)
    * [FastAPI](https://github.com/tiangolo/fastapi) - Framework for building WEB APIs
    * [FastStream](https://github.com/airtai/faststream) - Framework for building message queues
    * [Typer](https://github.com/tiangolo/typer) - Framework for buildig CLIs
    * [SQLAlchemy](https://github.com/sqlalchemy/sqlalchemy) - Toolkit for building high level db integrations
    * [alembic](https://github.com/sqlalchemy/alembic) - Tool for writing db migrations
    * [redis-py](https://github.com/redis/redis-py) - Redis python client
    * [Dishka](https://github.com/reagento/dishka) - DI framework
* [PostgreSQL](https://www.postgresql.org/)
* [Redis](https://redis.io/)


## How to run:

### Manually:

1. Install

```sh
pip install -e ".[web_api]"
```

2. Create [config](./config/prod_config.template.toml) file

3. Provide `CONFIG_PATH` env variable

4. Run migrations

```sh
amdb alembic upgrade head
```

5. Run worker

```sh
amdb worker
```

6. Run server

```sh
amdb web-api
```

### Using docker-compose:

1. Create [config](./config/prod_config.template.toml) file

2. Provide `CONFIG_PATH`, `REDIS_PASSWORD`, `REDIS_PORT_NUMBER`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`, `SERVER_HOST`, `SERVER_PORT` env variables

3. Run worker and server

```sh
docker-compose up web_api
```

4. Run migrations

```sh
docker exec -it amdb_backend.web_api amdb alembic upgrade head
```
