#!/usr/bin/env bash

set -x

ruff format src
ruff format tests
