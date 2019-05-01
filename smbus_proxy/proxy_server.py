# -*- coding: utf-8 -*-

from concurrent import futures
import grpc
from smbus_proxy import smbusRpc_pb2
from smbus_proxy import smbusRpc_pb2_grpc
from smbus_proxy import loop_thread
import time
import datetime
import hashlib
import logging


class Client(object):
    """
    This class describs the client
    it is used to know last activity of each client.
    """
    def __init__(self, bus_context):
        self.last_activity = time.time()
        self.bus_context = bus_context

    def update(self):
        self.last_activity = time.time()

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


class SmbusRcpServicer(smbusRpc_pb2_grpc.SmbusRcpServicer):
    """
    This class converts rpc messages to i2c operations
    """
    def __init__(self, smbus_cls, log_level=logging.INFO):
        """
        Constructor
        :param smbus_cls: Class used to manage i2c bus
        """
        self.logger = self._configure_logger(log_level)
        self.smbus_cls = smbus_cls
        self.opened_busses = dict()
        self.clients = dict()

        self.keep_alive_thread = loop_thread.LoopThread(target=self._keep_alive_handler, period=10)
        self.keep_alive_thread.setDaemon(True)
        self.keep_alive_thread.start()

        self.logger.info('Server started')

    def _configure_logger(self, level):
        logger = logging.getLogger('SmbusRcpServer')
        logger.setLevel(level)
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(level)
        stream_handler.setFormatter(logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s'))
        logger.addHandler(stream_handler)
        return logger

    def _keep_alive_handler(self):
        """
        Check last activity of each client and delete them if it's too old.
        :return:
        """
        now = time.time()
        to_be_deleted = []
        for key in self.clients:
            delta_last_activity = now - self.clients[key].last_activity
            if delta_last_activity >= 5:
                 to_be_deleted.append(key)

        for i in to_be_deleted:
            self.logger.info('No activity from client %s since 5 sec delete it' % i)
            del self.clients[i]


    def open(self, request, context):
        """
        Open i2c bus
        :param request: rpc request
        :param context: rpc context
        :return: rpc response
        """
        i2c_bus = request.i2c_bus
        response = smbusRpc_pb2.operation_status(code=0, exception='')
        client_id = self._generate_id(context)
        self.logger.info('New client(%s) requests bus %d' % (client_id, i2c_bus))

        try:
            if i2c_bus in self.opened_busses:
                self.clients[client_id] = Client(self.opened_busses[i2c_bus])
            else:
                self.opened_busses[i2c_bus] = BusContext(i2c_bus, self.smbus_cls(i2c_bus))
                self.clients[client_id] = Client(self.opened_busses[i2c_bus])
            context.set_trailing_metadata((('client_id', client_id),))
        except Exception as e:
            response.code = 1
            response.exception = 'proxy server: ' + str(e)
        return response

    def _generate_id(self, context):
        """
        Generate client if from context
        :param context: grpc context
        :return: client id
        """
        tmp = datetime.datetime.now()
        tmp = tmp.strftime('%Y%m%d%H%M%S%f')
        tmp += context.peer()
        m = hashlib.md5()
        m.update(tmp.encode('utf-8'))
        return str(m.hexdigest())

    def _get_client_id(self, context):
        """
        Get client id from context
        :param context: grpc context
        :return: client id
        """
        for key, value in context.invocation_metadata():
            if key == 'client_id':
                return value
        raise Exception('client id not found')


    def close(self, request, context):
        """
        Close i2c bus
        :param request: rpc request
        :param context: rpc context
        :return: rpc response
        """
        response = smbusRpc_pb2.operation_status(code=0, exception='')
        try:
            client_id = self._get_client_id(context)
            bus_context = self.clients[client_id].bus_context
            self.logger.info('Client(%s) release bus %d' % (client_id, bus_context.i2c_bus))
            del self.clients[client_id]
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
            client_id = self._get_client_id(context)
            self.logger.info('Client(%s) read_byte at 0x%x' % (client_id, i2c_addr))
            i2c_data = self.clients[client_id].bus_context.smbus.read_byte(i2c_addr)
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
            client_id = self._get_client_id(context)
            self.logger.info('Client(%s) write_byte (0x%x) at 0x%x' % (client_id, value, i2c_addr))
            self.clients[client_id].bus_context.smbus.write_byte(i2c_addr, value)
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
            client_id = self._get_client_id(context)
            self.logger.info('Client(%s) read_byte_data at 0x%x register 0x%x' % (client_id, i2c_addr, i2c_register))
            i2c_data = self.clients[client_id].bus_context.smbus.read_byte_data(i2c_addr, i2c_register)
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
            client_id = self._get_client_id(context)
            self.logger.info('Client(%s) write_byte (0x%x) at 0x%x register 0x%x' % (client_id, i2c_value, i2c_addr,
                                                                                     i2c_register))
            self.clients[client_id].bus_context.smbus.write_byte_data(i2c_addr, i2c_register, i2c_value)
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
            client_id = self._get_client_id(context)
            self.logger.info('Client(%s) read_word_data at 0x%x register 0x%x' % (client_id,  i2c_addr, i2c_register))
            i2c_data = self.clients[client_id].bus_context.smbus.read_word_data(i2c_addr, i2c_register)
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
            client_id = self._get_client_id(context)
            self.logger.info('Client(%s) write_word_data (0x%x) at 0x%x register 0x%x' % (client_id, i2c_value, i2c_addr,
                                                                                          i2c_register))
            self.clients[client_id].bus_context.smbus.write_word_data(i2c_addr, i2c_register, i2c_value)
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
            client_id = self._get_client_id(context)
            self.logger.info('Client(%s) read_i2c_block_data at 0x%x register 0x%x' % (client_id, i2c_addr,
                                                                                              i2c_register))
            i2c_data = self.clients[client_id].bus_context.smbus.read_i2c_block_data(i2c_addr, i2c_register)
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
            client_id = self._get_client_id(context)
            self.logger.info('Client(%s) write_i2c_block_data at 0x%x register 0x%x' % (client_id, i2c_addr, i2c_register))
            self.clients[client_id].bus_context.smbus.write_i2c_block_data(i2c_addr, i2c_register, list(i2c_data))
        except Exception as e:
            status_response.code = 1
            status_response.exception = 'proxy server: ' + str(e)
        return status_response

    def ping(self, request, context):
        """
        Update client activity
        :param request: rpc request
        :param context: rpc context
        :return:
        """
        status_response = smbusRpc_pb2.operation_status(code=0, exception='')
        try:
            client_id = self._get_client_id(context)
            self.clients[client_id].update()
            self.logger.debug('Ping from client(%s)' % client_id)
        except Exception as e:
            status_response.code = 1
            status_response.exception = 'proxy server: ' + str(e)
        return status_response


class ProxyServer:
    """
    This class creates a server to manage i2c bus.
    """
    def __init__(self, ip, smbus_cls, max_workers=4, log_level=logging.INFO):
        """
        Construtor
        :param ip: Ip address and port to listen
        :param smbus_cls: Class used to manage i2c bus
        """
        self.smbus_cls = smbus_cls
        self.grpc_server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
        smbusRpc_pb2_grpc.add_SmbusRcpServicer_to_server(
            SmbusRcpServicer(self.smbus_cls, log_level), self.grpc_server)
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
