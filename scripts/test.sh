#!/usr/bin/env bash

TEST_DATABASE_CONTAINER_NAME="amdb.tests.postgres"

run_database_container() {
    echo "Running database container..."
    podman run -d --replace \
        --name $TEST_DATABASE_CONTAINER_NAME \
        -e POSTGRES_USER=$TEST_DATABASE_PG_USER \
        -e POSTGRES_PASSWORD=$TEST_DATABASE_PG_PASSWORD \
        -e POSTGRES_DB=$TEST_DATABASE_PG_NAME \
        -p "$TEST_DATABASE_PG_PORT:5432" \
        postgres:15-alpine
    sleep 3
}

run_tests() {
    echo "Running tests..."
    pytest
}

remove_database_container() {
    echo "Removing database container..."
    podman rm -f $TEST_DATABASE_CONTAINER_NAME
}


run_database_container
run_tests
remove_database_container
