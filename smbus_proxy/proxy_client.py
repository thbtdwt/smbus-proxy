# -*- coding: utf-8 -*-


import grpc
from smbus_proxy import smbusRpc_pb2
from smbus_proxy import smbusRpc_pb2_grpc
from smbus_proxy import loop_thread
import logging

class ProxyClient:
    """
    As SMBus, this claas provides function to access to an i2c device.
    """
    def __init__(self, server_address, i2c_bus, log_level=logging.INFO):
        """
        Constructor
        :param server_address: ip + port of the server
        :param i2c_bus: i2c bus number
        """
        self.i2c_bus = i2c_bus
        self.channel = None
        self.stub = None
        self.id = None
        self.keep_alive_thread = None
        self.logger = self._configure_logger(log_level)
        try:
            self.channel = grpc.insecure_channel(server_address)
            self.stub = smbusRpc_pb2_grpc.SmbusRcpStub(self.channel)
        except Exception as e:
            raise Exception('Connect to %s failed: %s'%(server_address,str(e)))
        status, call = self.stub.open.with_call(smbusRpc_pb2.open_request(i2c_bus=self.i2c_bus))

        for key, value in call.trailing_metadata():
            if key == 'client_id':
                self.id = value
                break
        self.logger.debug('Get id %s' % self.id)

        self.keep_alive_thread = loop_thread.LoopThread(target=self._keep_alive_handler, period=1)
        self.keep_alive_thread.setDaemon(True)
        self.keep_alive_thread.start()

        if status.code:
            raise Exception(status.exception)

        self.logger.debug('Client ready')

    def _keep_alive_handler(self):
        """
        Send ping regularly
        :return:
        """
        try:
            self.stub.ping(smbusRpc_pb2.keep_alive(info='request'), metadata=(('client_id', self.id),))
        except Exception as e:
            print(e)

    @staticmethod
    def _configure_logger(level):
        """
        Configure the logger format
        :param self:
        :param level: logging level, INFO, DEBUG etc
        :return: logger
        """
        logger = logging.getLogger('ProxyClient')
        logger.setLevel(level)
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(level)
        stream_handler.setFormatter(logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s'))
        logger.addHandler(stream_handler)
        return logger

    def close(self):
        """
        Close communication with server
        :return:
        """
        if self.keep_alive_thread:
            self.keep_alive_thread.cancel()

        if self.id and self.stub:
            status = self.stub.close(smbusRpc_pb2.close_request(), metadata=(('client_id', self.id),))
            if status.code:
                raise Exception(status.exception)


    def read_byte(self, i2c_addr: int):
        """
        Read byte from a i2c device.
        :param i2c_addr: i2c device address.
        :return: int32
        """
        response = self.stub.read_byte(smbusRpc_pb2.read_byte_request(i2c_addr=i2c_addr),
                                       metadata=(('client_id', self.id),))
        if response.status.code == 0:
            return response.data
        else:
            raise Exception(response.status.exception)

    def write_byte(self, i2c_addr: int, value: int):
        """
        Write byte to an i2c device.
        :param i2c_addr: i2c device address.
        :param value: byte value.
        :return:
        """
        status = self.stub.write_byte(smbusRpc_pb2.write_byte_request(i2c_addr=i2c_addr, value=value),
                                      metadata=(('client_id', self.id),))
        print(status)
        if status.code:
            raise Exception(status.exception)

    def read_byte_data(self, i2c_addr: int, register: int):
        """
        Read byte from an address of i2c device.
        :param i2c_addr: i2c device address.
        :param register: register address.
        :return: int32
        """
        response = self.stub.read_byte_data(smbusRpc_pb2.read_byte_data_request(i2c_addr=i2c_addr, register=register),
                                            metadata=(('client_id', self.id),))
        if response.status.code == 0:
            return response.data
        else:
            raise Exception(response.status.exception)

    def write_byte_data(self, i2c_addr: int, register: int, value: int):
        """
        Read byte to an address of i2c device.
        :param i2c_addr: i2c device address.
        :param register: register address.
        :param value: byte value.
        :return:
        """
        status = self.stub.write_byte_data(smbusRpc_pb2.write_byte_data_request(i2c_addr=i2c_addr, register=register,
                                                                                value=value),
                                           metadata=(('client_id', self.id),))
        if status.code:
            raise Exception(status.exception)

    def read_word_data(self, i2c_addr: int, register: int):
        """
        Read word to an address of i2c device.
        :param i2c_addr: i2c device address.
        :param register: register address.
        :return: int32
        """
        response = self.stub.read_word_data(smbusRpc_pb2.read_word_data_request(i2c_addr=i2c_addr, register=register),
                                            metadata=(('client_id', self.id),))
        if response.status.code == 0:
            return response.data
        else:
            raise Exception(response.status.exception)

    def write_word_data(self, i2c_addr: int, register: int, value: int):
        """
        Write word to an address of i2c device.
        :param i2c_addr: i2c device address.
        :param register: register address.
        :param value: word value.
        :return:
        """
        status = self.stub.write_word_data(smbusRpc_pb2.write_word_data_request(i2c_addr=i2c_addr, register=register,
                                                                           value=value),
                                           metadata=(('client_id', self.id),))
        if status.code:
            raise Exception(status.exception)

    def read_i2c_block_data(self, i2c_addr: int, register: int):
        """
        Read i2c block from an address of i2c device.
        :param i2c_addr: i2c device address.
        :param register: register address.
        :return: bytes
        """
        response = self.stub.read_i2c_block_data(smbusRpc_pb2.read_i2c_block_data_request(i2c_addr=i2c_addr,
                                                                                          register=register),
                                                 metadata=(('client_id', self.id),))
        if response.status.code == 0:
            return list(response.data)
        else:
            raise Exception(response.status.exception)

    def write_i2c_block_data(self, i2c_addr: int, register: int, data: [int]):
        """
        Write i2c block to an address of i2c device.
        :param i2c_addr: i2c device address.
        :param register: register address.
        :param data: bytes data
        :return:
        """
        status = self.stub.write_i2c_block_data(smbusRpc_pb2.write_i2c_block_data_request(i2c_addr=i2c_addr,
                                                                                          register=register,
                                                                                          data=bytes(data)),
                                                metadata=(('client_id', self.id),))
        if status.code:
            raise Exception(status.exception)
