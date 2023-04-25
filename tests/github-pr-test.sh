#!/bin/bash

cd "$(dirname "$0")"
python ../../src/nape_cli/main.py  \
  -f ./target_files/GitHub/pull-request.json \
  -p ./resources/procedures/GitHub/ \
  -o ./test_outputs/