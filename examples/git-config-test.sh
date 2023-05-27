#!/bin/bash

cd "$(dirname "$0")"
python ../src/main.py \
        -f ./target_files/local_machine/git-config.txt \
        -p ./resources/procedures/local_machine/git \
        -o ./test_outputs/