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

## How to run:

### Using docker-compose:

1. Provide `.env` file with variables from `.env.template`

2. Run docker-compose

```sh
docker-compose --env-file ./.env up web_api
```

### Manually:

1. Install

```sh
pip install -e ".[web_api,cli]"
```

2. Provide env variables from `.env.template`

3. Run server

```sh
amdb-web_api
```

4. Run cli

```sh
amdb-cli
```

## How to run migrations:

1. Provide env variables for postgres from `.env.template`

2. Run migrations:

```
amdb-cli migration alembic upgrade head
```
