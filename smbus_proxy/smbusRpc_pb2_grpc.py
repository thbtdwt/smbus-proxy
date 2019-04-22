# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import smbusRpc_pb2 as smbusRpc__pb2


class SmbusRcpStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.open = channel.unary_unary(
        '/SmbusRcp/open',
        request_serializer=smbusRpc__pb2.open_request.SerializeToString,
        response_deserializer=smbusRpc__pb2.operation_status.FromString,
        )
    self.close = channel.unary_unary(
        '/SmbusRcp/close',
        request_serializer=smbusRpc__pb2.close_request.SerializeToString,
        response_deserializer=smbusRpc__pb2.operation_status.FromString,
        )
    self.read_byte = channel.unary_unary(
        '/SmbusRcp/read_byte',
        request_serializer=smbusRpc__pb2.read_byte_request.SerializeToString,
        response_deserializer=smbusRpc__pb2.read_byte_response.FromString,
        )
    self.write_byte = channel.unary_unary(
        '/SmbusRcp/write_byte',
        request_serializer=smbusRpc__pb2.write_byte_request.SerializeToString,
        response_deserializer=smbusRpc__pb2.operation_status.FromString,
        )
    self.read_byte_data = channel.unary_unary(
        '/SmbusRcp/read_byte_data',
        request_serializer=smbusRpc__pb2.read_byte_data_request.SerializeToString,
        response_deserializer=smbusRpc__pb2.read_byte_data_response.FromString,
        )
    self.write_byte_data = channel.unary_unary(
        '/SmbusRcp/write_byte_data',
        request_serializer=smbusRpc__pb2.write_byte_data_request.SerializeToString,
        response_deserializer=smbusRpc__pb2.operation_status.FromString,
        )
    self.read_word_data = channel.unary_unary(
        '/SmbusRcp/read_word_data',
        request_serializer=smbusRpc__pb2.read_word_data_request.SerializeToString,
        response_deserializer=smbusRpc__pb2.read_word_data_response.FromString,
        )
    self.write_word_data = channel.unary_unary(
        '/SmbusRcp/write_word_data',
        request_serializer=smbusRpc__pb2.write_word_data_request.SerializeToString,
        response_deserializer=smbusRpc__pb2.operation_status.FromString,
        )
    self.read_i2c_block_data = channel.unary_unary(
        '/SmbusRcp/read_i2c_block_data',
        request_serializer=smbusRpc__pb2.read_i2c_block_data_request.SerializeToString,
        response_deserializer=smbusRpc__pb2.read_i2c_block_data_response.FromString,
        )
    self.write_i2c_block_data = channel.unary_unary(
        '/SmbusRcp/write_i2c_block_data',
        request_serializer=smbusRpc__pb2.write_i2c_block_data_request.SerializeToString,
        response_deserializer=smbusRpc__pb2.operation_status.FromString,
        )
    self.ping = channel.unary_unary(
        '/SmbusRcp/ping',
        request_serializer=smbusRpc__pb2.keep_alive.SerializeToString,
        response_deserializer=smbusRpc__pb2.keep_alive.FromString,
        )


class SmbusRcpServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def open(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def close(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def read_byte(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def write_byte(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def read_byte_data(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def write_byte_data(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def read_word_data(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def write_word_data(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def read_i2c_block_data(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def write_i2c_block_data(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def ping(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_SmbusRcpServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'open': grpc.unary_unary_rpc_method_handler(
          servicer.open,
          request_deserializer=smbusRpc__pb2.open_request.FromString,
          response_serializer=smbusRpc__pb2.operation_status.SerializeToString,
      ),
      'close': grpc.unary_unary_rpc_method_handler(
          servicer.close,
          request_deserializer=smbusRpc__pb2.close_request.FromString,
          response_serializer=smbusRpc__pb2.operation_status.SerializeToString,
      ),
      'read_byte': grpc.unary_unary_rpc_method_handler(
          servicer.read_byte,
          request_deserializer=smbusRpc__pb2.read_byte_request.FromString,
          response_serializer=smbusRpc__pb2.read_byte_response.SerializeToString,
      ),
      'write_byte': grpc.unary_unary_rpc_method_handler(
          servicer.write_byte,
          request_deserializer=smbusRpc__pb2.write_byte_request.FromString,
          response_serializer=smbusRpc__pb2.operation_status.SerializeToString,
      ),
      'read_byte_data': grpc.unary_unary_rpc_method_handler(
          servicer.read_byte_data,
          request_deserializer=smbusRpc__pb2.read_byte_data_request.FromString,
          response_serializer=smbusRpc__pb2.read_byte_data_response.SerializeToString,
      ),
      'write_byte_data': grpc.unary_unary_rpc_method_handler(
          servicer.write_byte_data,
          request_deserializer=smbusRpc__pb2.write_byte_data_request.FromString,
          response_serializer=smbusRpc__pb2.operation_status.SerializeToString,
      ),
      'read_word_data': grpc.unary_unary_rpc_method_handler(
          servicer.read_word_data,
          request_deserializer=smbusRpc__pb2.read_word_data_request.FromString,
          response_serializer=smbusRpc__pb2.read_word_data_response.SerializeToString,
      ),
      'write_word_data': grpc.unary_unary_rpc_method_handler(
          servicer.write_word_data,
          request_deserializer=smbusRpc__pb2.write_word_data_request.FromString,
          response_serializer=smbusRpc__pb2.operation_status.SerializeToString,
      ),
      'read_i2c_block_data': grpc.unary_unary_rpc_method_handler(
          servicer.read_i2c_block_data,
          request_deserializer=smbusRpc__pb2.read_i2c_block_data_request.FromString,
          response_serializer=smbusRpc__pb2.read_i2c_block_data_response.SerializeToString,
      ),
      'write_i2c_block_data': grpc.unary_unary_rpc_method_handler(
          servicer.write_i2c_block_data,
          request_deserializer=smbusRpc__pb2.write_i2c_block_data_request.FromString,
          response_serializer=smbusRpc__pb2.operation_status.SerializeToString,
      ),
      'ping': grpc.unary_unary_rpc_method_handler(
          servicer.ping,
          request_deserializer=smbusRpc__pb2.keep_alive.FromString,
          response_serializer=smbusRpc__pb2.keep_alive.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'SmbusRcp', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
