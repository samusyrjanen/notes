#!/bin/bash

set -xeoa pipefail

#######################################################################################
# RUN TESTS
#######################################################################################

echo Starting tests.
echo
pip3 install -r tests/requirements-tests.txt

echo Including ~/.local/bin in PATH
export PATH=~/.local/bin:$PATH

echo
echo Waiting for deployment to become ready.
python3 tests/wait_deployment_ready.py --timeout 600

echo
echo All resources up!
echo Starting unittests...
pytest --log-cli-level="$LOG_LEVEL_TESTS"

exit 0