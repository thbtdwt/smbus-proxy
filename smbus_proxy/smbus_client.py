import grpc

from smbus_proxy import smbusRpc_pb2
from smbus_proxy import smbusRpc_pb2_grpc


class SmbusClient:
    def __init__(self, server_address, i2c_bus):
        self.i2c_bus = i2c_bus
        self.channel = None
        self.stub = None

        try:
            self.channel = grpc.insecure_channel(server_address)
            grpc.channel_ready_future(self.channel).result(timeout=5)
            self.stub = smbusRpc_pb2_grpc.SmbusRcpStub(self.channel)
        except Exception as e:
            raise Exception('Connect to %s failed: %s'%(server_address,str(e)))

        status = self.stub.open(smbusRpc_pb2.open_request(i2c_bus=self.i2c_bus))
        if status.code:
            raise Exception(status.exception)

    def __del__(self):
        if self.stub:
            status = self.stub.close(smbusRpc_pb2.close_request())
            if status.code:
                raise Exception(status.exception)

    def read_byte(self, i2c_addr):
        response = self.stub.read_byte(smbusRpc_pb2.read_byte_request(i2c_addr=i2c_addr))
        if response.status.code == 0:
            return response.data
        else:
            raise Exception(response.status.exception)

    def write_byte(self, i2c_addr, value):
        status = self.stub.write_byte(smbusRpc_pb2.write_byte_request(i2c_addr=i2c_addr, value=value))
        print(status)
        if status.code:
            raise Exception(status.exception)

    def read_byte_data(self, i2c_addr, register):
        response = self.stub.read_byte_data(smbusRpc_pb2.read_byte_data_request(i2c_addr=i2c_addr, register=register))
        if response.status.code == 0:
            return response.data
        else:
            raise Exception(response.status.exception)

    def write_byte_data(self, i2c_addr, register, value):
        status = self.stub.write_byte_data(smbusRpc_pb2.write_byte_data_request(i2c_addr=i2c_addr, register=register,
                                                                           value=value))
        if status.code:
            raise Exception(status.exception)

    def read_word_data(self, i2c_addr, register):
        response = self.stub.read_word_data(smbusRpc_pb2.read_word_data_request(i2c_addr=i2c_addr, register=register))
        if response.status.code == 0:
            return response.data
        else:
            raise Exception(response.status.exception)

    def write_word_data(self, i2c_addr, register, value):
        status = self.stub.write_word_data(smbusRpc_pb2.write_word_data_request(i2c_addr=i2c_addr, register=register,
                                                                           value=value))
        if status.code:
            raise Exception(status.exception)

    def read_i2c_block_data(self, i2c_addr, register):
        response = self.stub.read_i2c_block_data(smbusRpc_pb2.read_i2c_block_data_request(i2c_addr=i2c_addr,
                                                                                          register=register))
        if response.status.code == 0:
            return response.data
        else:
            raise Exception(response.status.exception)

    def write_i2c_block_data(self, i2c_addr, register, value):
        status = self.stub.write_i2c_block_data(smbusRpc_pb2.write_i2c_block_data_request(i2c_addr=i2c_addr,
                                                                                         register=register, data=value))
        if status.code:
            raise Exception(status.exception)