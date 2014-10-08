#!/usr/bin/env bash

set -e

setup() {
    ENVDIR=${PWD}/venv
    test -d ${ENVDIR} && rm -r ${ENVDIR}
    conda create --yes --quiet -p ${ENVDIR} pip pytest ipython numpy matplotlib scipy pandas cython
    source activate ${ENVDIR}

    test -d build && rm -r build || true
}

teardown() {
    source deactivate
    rm -rf ${ENVDIR}
}

main() {
    echo "Setting up"
    setup >/dev/null
    echo "Installing"
    pip install .
    echo "Running test"
    python -c 'import transitgen'
    teardown >/dev/null
}

trap teardown EXIT

main
