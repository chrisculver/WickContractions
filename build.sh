#!/bin/bash

# linting with flake
# stop the build if there are Python syntax errors or undefined names
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
ret=$?
# exit-zero treats all errors as warnings. The GitHub editor is 127 chars wide
#flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

if [ $ret -ne 0 ]
then
    echo "Error while linting"
    exit
fi

# show status of testing
coverage run -m --source=src/wick,src/ops,src/diags,src/laph pytest
coverage report -m --skip-covered