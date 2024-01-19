#!/usr/bin/env bash

TEST_POSTGRES_CONTAINER_NAME="amdb.tests.postgres"
TEST_REDIS_CONTAINER_NAME="amdb.tests.redis"

create_and_run_containers() {
    echo "Running postgres container..."
    podman run -d --replace \
        --name $TEST_POSTGRES_CONTAINER_NAME \
        -e POSTGRES_USER=$TEST_POSTGRES_USER \
        -e POSTGRES_PASSWORD=$TEST_POSTGRES_PASSWORD \
        -e POSTGRES_DB=$TEST_POSTGRES_NAME \
        -p "$TEST_POSTGRES_HOST:$TEST_POSTGRES_PORT:5432" \
        postgres:15-alpine

    echo "Running redis container..."
    podman run -d --replace \
        --name $TEST_REDIS_CONTAINER_NAME \
        -e ALLOW_EMPTY_PASSWORD=yes \
        -e REDIS_DATABASE=$TEST_REDIS_DATABASE \
        -p "$TEST_REDIS_HOST:$TEST_REDIS_PORT:6379" \
        bitnami/redis:7.2

    sleep 3
}

run_tests() {
    echo "Running tests..."
    pytest
}

remove_containers() {
    echo "Removing containers..."
    podman rm -f $TEST_POSTGRES_CONTAINER_NAME $TEST_REDIS_CONTAINER_NAME
}


create_and_run_containers
run_tests
remove_containers
