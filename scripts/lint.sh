#!/usr/bin/env bash

set -x

mypy src
ruff check src