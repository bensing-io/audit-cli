#!/bin/bash

cd "$(dirname "$0")"
python ../../src/nape_cli/main.py \
        -f ./target_files/Dockerfile \
        -p ./resources/procedures/Dockerfile/ \
        -o ./test_outputs/