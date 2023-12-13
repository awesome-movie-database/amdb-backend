#!/usr/bin/env bash

set -x

mypy src
mypy tests --ignore-missing-imports
ruff check src
ruff check tests
