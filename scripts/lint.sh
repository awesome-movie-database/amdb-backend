#!/usr/bin/env bash

set -x

ruff check src
ruff check tests
mypy src
mypy tests --ignore-missing-imports
