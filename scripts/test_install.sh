#!/usr/bin/env bash

set -e

setup() {
    ENVDIR=${PWD}/venv
    test -d ${ENVDIR} && rm -r ${ENVDIR}
    conda create --yes --quiet -p ${ENVDIR} pip pytest ipython cython numpy
    source activate ${ENVDIR}

    test -d build && rm -r build || true
}

teardown() {
    source deactivate
}

main() {
    echo "Setting up"
    setup
    echo "Installing"
    pip install .
    echo "Running test"
    python -c 'import transitgen'
    teardown
}

trap teardown EXIT

main
