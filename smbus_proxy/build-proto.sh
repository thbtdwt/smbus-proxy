#!/bin/bash

script_dir=$(dirname "${BASH_SOURCE[0]}")
protos_dir=${script_dir}/protos


python -m grpc_tools.protoc -I${protos_dir} --python_out=${script_dir}/ --grpc_python_out=${script_dir} ${protos_dir}/smbusRpc.proto