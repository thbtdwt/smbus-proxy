from concurrent import futures
import grpc
from smbus_proxy import smbusRpc_pb2
from smbus_proxy import smbusRpc_pb2_grpc


class BusContext(object):

    def __init__(self, i2c_bus, smbus):
        self.i2c_bus = i2c_bus
        self.smbus = smbus
        self.ref_count = 1


class SmbusRcpServicer (smbusRpc_pb2_grpc.SmbusRcpServicer):

    def __init__(self, smbus_cls):
        self.smbus_cls = smbus_cls
        self.opened_busses = dict()
        self.clients = dict()

    def open(self, request, context):
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
        response = smbusRpc_pb2.operation_status(code=0, exception='')
        try:
            bus_context = self.clients[context.peer()]
            del self.clients[context.peer()]
            bus_context.ref_count -= 1

            if bus_context.ref_count == 0:
                del self.opened_busses[bus_context.i2c_bus]
            del bus_context

        except Exception as e:
            response.code = 1
            response.exception = 'proxy server: ' + str(e)

        return response

    def read_byte(self, request, context):
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
        status_response = smbusRpc_pb2.operation_status(code=0, exception='')
        i2c_addr = request.i2c_addr
        i2c_register = request.register
        i2c_data = None

        try:
            i2c_data = self.clients[context.peer()].smbus.read_i2c_block_data(i2c_addr, i2c_register)
        except Exception as e:
            status_response.code = 1
            status_response.exception = 'proxy server: ' + str(e)

        return smbusRpc_pb2.read_i2c_block_data_response(status=status_response, data=i2c_data)

    def write_i2c_block_data(self, request, context):
        status_response = smbusRpc_pb2.operation_status(code=0, exception='')
        i2c_addr = request.i2c_addr
        i2c_register = request.register
        i2c_data = request.data

        try:
            self.clients[context.peer()].smbus.write_i2c_block_data(i2c_addr, i2c_register, i2c_data)
        except Exception as e:
            status_response.code = 1
            status_response.exception = 'proxy server: ' + str(e)

        return status_response


class ProxyServer:
    def __init__(self, ip, smbus_cls):
        self.smbus_cls = smbus_cls
        self.grpc_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        smbusRpc_pb2_grpc.add_SmbusRcpServicer_to_server(
            SmbusRcpServicer(self.smbus_cls), self.grpc_server)
        self.grpc_server.add_insecure_port(ip)



    def serve(self):
        self.grpc_server.start()

    def stop(self):
        self.grpc_server.stop(0)
