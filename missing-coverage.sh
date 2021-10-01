#!/bin/bash
coverage run -m --source=src/wick,src/ops,src/diags,src/laph pytest
coverage report -m --skip-covered
