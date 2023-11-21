#!/usr/bin/env bash

set -x

mypy src
flake8 src