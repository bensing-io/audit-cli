#!/bin/bash

cd "$(dirname "$0")"
python ../src/main.py  \
        -f ./target_files/Dockerfile \
        -p ./resources/procedures/local_machine/ \
        -o ./test_outputs/