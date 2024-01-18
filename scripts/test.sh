#!/usr/bin/env bash

TEST_POSTGRES_CONTAINER_NAME="amdb.tests.postgres"

run_database_container() {
    echo "Running postgres container..."
    podman run -d --replace \
        --name $TEST_POSTGRES_CONTAINER_NAME \
        -e POSTGRES_USER=$TEST_POSTGRES_USER \
        -e POSTGRES_PASSWORD=$TEST_POSTGRES_PASSWORD \
        -e POSTGRES_DB=$TEST_POSTGRES_NAME \
        -p "$TEST_POSTGRES_HOST:$TEST_POSTGRES_PORT:5432" \
        postgres:15-alpine
    sleep 3
}

run_tests() {
    echo "Running tests..."
    pytest
}

remove_database_container() {
    echo "Removing postgres container..."
    podman rm -f $TEST_POSTGRES_CONTAINER_NAME
}


run_database_container
run_tests
remove_database_container
