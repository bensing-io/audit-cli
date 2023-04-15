#!/bin/bash

cd "$(dirname "$0")"
python ../cli.py \
  -f ./target_files/GitHub/pull-request.json \
  -p ./resources/procedures/GitHub/