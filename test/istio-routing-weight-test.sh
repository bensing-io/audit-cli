#!/bin/bash

cd "$(dirname "$0")"
python ../cli.py \
        -f ./target_files/Istio/istio-config-1.yml \
        -p ./resources/procedures/Istio/ \
        -o ./test_outputs/