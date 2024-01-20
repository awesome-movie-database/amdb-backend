#!/usr/bin/env bash

set -x

pytest --cov=./ --cov-report=xml
