#!/bin/bash

script_dir=$(dirname "${BASH_SOURCE[0]}")
protos_dir=${script_dir}/
python_dir=${script_dir}/../smbus_proxy

python -m grpc_tools.protoc -I${protos_dir} --python_out=${python_dir} --grpc_python_out=${python_dir} ${protos_dir}/smbusRpc.proto