# -*- coding: utf-8 -*-

from concurrent import futures
import grpc
from smbus_proxy import smbusRpc_pb2
from smbus_proxy import smbusRpc_pb2_grpc


class BusContext(object):
    """
    This class provides info:
    - Bus number.
    - Access to the bus.
    """
    def __init__(self, i2c_bus, smbus):
        """
        Constructor
        :param i2c_bus: i2c bus number
        :param smbus: The way to access to i2c bus
        """
        self.i2c_bus = i2c_bus
        self.smbus = smbus
        self.ref_count = 1  # count the number of clients who use this bus


class SmbusRcpServicer(smbusRpc_pb2_grpc.SmbusRcpServicer):
    """
    This class converts rpc messages to i2c operations
    """
    def __init__(self, smbus_cls):
        """
        Constructor
        :param smbus_cls: Class used to manage i2c bus
        """
        self.smbus_cls = smbus_cls
        self.opened_busses = dict()
        self.clients = dict()

    def open(self, request, context):
        """
        Open i2c bus
        :param request: rpc request
        :param context: rpc context
        :return: rpc response
        """
        i2c_bus = request.i2c_bus
        response = smbusRpc_pb2.operation_status(code=0, exception='')
        try:
            if i2c_bus in self.opened_busses:
                self.clients[context.peer()] = self.opened_busses[i2c_bus]
                self.opened_busses[i2c_bus].ref_count += 1
            else:
                self.opened_busses[i2c_bus] = BusContext(i2c_bus, self.smbus_cls(i2c_bus))
                self.clients[context.peer()] = self.opened_busses[i2c_bus]
        except Exception as e:
            response.code = 1
            response.exception = 'proxy server: ' + str(e)
        return response

    def close(self, request, context):
        """
        Close i2c bus
        :param request: rpc request
        :param context: rpc context
        :return: rpc response
        """
        response = smbusRpc_pb2.operation_status(code=0, exception='')
        try:
            bus_context = self.clients[context.peer()]
            del self.clients[context.peer()]
            bus_context.ref_count -= 1

            if bus_context.ref_count == 0:
                # This bus is no used anymore, close and remove it.
                del self.opened_busses[bus_context.i2c_bus]
            del bus_context
        except Exception as e:
            response.code = 1
            response.exception = 'proxy server: ' + str(e)
        return response

    def read_byte(self, request, context):
        """
        Read byte
        :param request: rpc request
        :param context: rpc context
        :return: rpc response
        """
        status_response = smbusRpc_pb2.operation_status(code=0, exception='')
        i2c_addr = request.i2c_addr
        i2c_data = None
        try:
            i2c_data = self.clients[context.peer()].smbus.read_byte(i2c_addr)
        except Exception as e:
            status_response.code = 1
            status_response.exception = 'proxy server: ' + str(e)
        return smbusRpc_pb2.read_byte_response(status=status_response, data=i2c_data)

    def write_byte(self, request, context):
        """
        Write byte
        :param request: rpc request
        :param context: rpc context
        :return: rpc response
        """
        status_response = smbusRpc_pb2.operation_status(code=0, exception='')
        i2c_addr = request.i2c_addr
        value = request.value
        try:
            self.clients[context.peer()].smbus.write_byte(i2c_addr, value)
        except Exception as e:
            status_response.code = 1
            status_response.exception = 'proxy server: ' + str(e)
        return status_response

    def read_byte_data(self, request, context):
        """
        Read byte from a given register
        :param request: rpc request
        :param context: rpc context
        :return: rpc response
        """
        status_response = smbusRpc_pb2.operation_status(code=0, exception='')
        i2c_addr = request.i2c_addr
        i2c_register = request.register
        i2c_data = None
        try:
            i2c_data = self.clients[context.peer()].smbus.read_byte_data(i2c_addr, i2c_register)
        except Exception as e:
            status_response.code = 1
            status_response.exception = 'proxy server: ' + str(e)
        return smbusRpc_pb2.read_byte_data_response(status=status_response, data=i2c_data)

    def write_byte_data(self, request, context):
        """
        Read byte to a given register
        :param request: rpc request
        :param context: rpc context
        :return: rpc response
        """
        status_response = smbusRpc_pb2.operation_status(code=0, exception='')
        i2c_addr = request.i2c_addr
        i2c_register = request.register
        i2c_value = request.value
        try:
            self.clients[context.peer()].smbus.write_byte_data(i2c_addr, i2c_register, i2c_value)
        except Exception as e:
            status_response.code = 1
            status_response.exception = 'proxy server: ' + str(e)
        return status_response

    def read_word_data(self, request, context):
        """
        Read word from a given register
        :param request: rpc request
        :param context: rpc context
        :return: rpc response
        """
        status_response = smbusRpc_pb2.operation_status(code=0, exception='')
        i2c_addr = request.i2c_addr
        i2c_register = request.register
        i2c_data = None
        try:
            i2c_data = self.clients[context.peer()].smbus.read_word_data(i2c_addr, i2c_register)
        except Exception as e:
            status_response.code = 1
            status_response.exception = 'proxy server: ' + str(e)
        return smbusRpc_pb2.read_word_data_response(status=status_response, data=i2c_data)

    def write_word_data(self, request, context):
        """
        Write word to a given register
        :param request: rpc request
        :param context: rpc context
        :return: rpc response
        """
        status_response = smbusRpc_pb2.operation_status(code=0, exception='')
        i2c_addr = request.i2c_addr
        i2c_register = request.register
        i2c_value = request.value
        try:
            self.clients[context.peer()].smbus.write_word_data(i2c_addr, i2c_register, i2c_value)
        except Exception as e:
            status_response.code = 1
            status_response.exception = 'proxy server: ' + str(e)
        return status_response

    def read_i2c_block_data(self, request, context):
        """
        Read i2c block from a given register
        :param request: rpc request
        :param context: rpc context
        :return: rpc response
        """
        status_response = smbusRpc_pb2.operation_status(code=0, exception='')
        i2c_addr = request.i2c_addr
        i2c_register = request.register
        i2c_data = None
        try:
            i2c_data = self.clients[context.peer()].smbus.read_i2c_block_data(i2c_addr, i2c_register)
        except Exception as e:
            status_response.code = 1
            status_response.exception = 'proxy server: ' + str(e)
        return smbusRpc_pb2.read_i2c_block_data_response(status=status_response, data=bytes(i2c_data))

    def write_i2c_block_data(self, request, context):
        """
        Write i2c block to a given register
        :param request: rpc request
        :param context: rpc context
        :return: rpc response
        """
        status_response = smbusRpc_pb2.operation_status(code=0, exception='')
        i2c_addr = request.i2c_addr
        i2c_register = request.register
        i2c_data = request.data
        try:
            self.clients[context.peer()].smbus.write_i2c_block_data(i2c_addr, i2c_register, list(i2c_data))
        except Exception as e:
            status_response.code = 1
            status_response.exception = 'proxy server: ' + str(e)
        return status_response


class ProxyServer:
    """
    This class creates a server to manage i2c bus.
    """
    def __init__(self, ip, smbus_cls, max_workers):
        """
        Construtor
        :param ip: Ip address and port to listen
        :param smbus_cls: Class used to manage i2c bus
        """
        self.smbus_cls = smbus_cls
        self.grpc_server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
        smbusRpc_pb2_grpc.add_SmbusRcpServicer_to_server(
            SmbusRcpServicer(self.smbus_cls), self.grpc_server)
        self.grpc_server.add_insecure_port(ip)

    def serve(self):
        """
        Start the server
        :return:
        """
        self.grpc_server.start()

    def stop(self):
        """
        Stop the server
        :return:
        """
        self.grpc_server.stop(0)
