#!/usr/bin/env bash

DATABASE_CONTAINER_NAME="amdb.tests.database"

run_database_container() {
    echo "Running database container..."
    podman run -d \
        --name $DATABASE_CONTAINER_NAME \
        -e POSTGRES_USER=$TEST_DATABASE_PG_USER \
        -e POSTGRES_PASSWORD=$TEST_DATABASE_PG_PASSWORD \
        -e POSTGRES_DB=$TEST_DATABASE_PG_NAME \
        -p "5432:5432" \
        --replace \
        postgres:15-alpine
    sleep 3  # FIXME: Do it properly
}

run_tests() {
    echo "Running tests..."
    pytest -vv
}

remove_database_container() {
    echo "Removing database container..."
    podman rm -f $DATABASE_CONTAINER_NAME
}


run_database_container
run_tests
remove_database_container
