#!/bin/bash

script_dir=$(dirname "${BASH_SOURCE[0]}")

export PYTHONPATH=${script_dir}/..

python3 ${script_dir}/test_server.py &
server_pid=$!

python3 ${script_dir}/test_client.py -v
kill $server_pid