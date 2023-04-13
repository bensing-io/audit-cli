#!/bin/bash

cd "$(dirname "$0")"
python ../audit-cli.py \
  -f ./target_files/GitHub/pull-request.json \
  -p ./resources/procedures/GitHub/