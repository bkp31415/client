# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from wandb.proto import wandb_internal_pb2 as wandb_dot_proto_dot_wandb__internal__pb2
from wandb.proto import wandb_server_pb2 as wandb_dot_proto_dot_wandb__server__pb2


class InternalServiceStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.RunUpdate = channel.unary_unary(
        '/wandb_internal.InternalService/RunUpdate',
        request_serializer=wandb_dot_proto_dot_wandb__internal__pb2.RunRecord.SerializeToString,
        response_deserializer=wandb_dot_proto_dot_wandb__internal__pb2.RunUpdateResult.FromString,
        )
    self.RunExit = channel.unary_unary(
        '/wandb_internal.InternalService/RunExit',
        request_serializer=wandb_dot_proto_dot_wandb__internal__pb2.RunExitRecord.SerializeToString,
        response_deserializer=wandb_dot_proto_dot_wandb__internal__pb2.RunExitResult.FromString,
        )
    self.Log = channel.unary_unary(
        '/wandb_internal.InternalService/Log',
        request_serializer=wandb_dot_proto_dot_wandb__internal__pb2.HistoryRecord.SerializeToString,
        response_deserializer=wandb_dot_proto_dot_wandb__internal__pb2.HistoryResult.FromString,
        )
    self.Summary = channel.unary_unary(
        '/wandb_internal.InternalService/Summary',
        request_serializer=wandb_dot_proto_dot_wandb__internal__pb2.SummaryRecord.SerializeToString,
        response_deserializer=wandb_dot_proto_dot_wandb__internal__pb2.SummaryResult.FromString,
        )
    self.Config = channel.unary_unary(
        '/wandb_internal.InternalService/Config',
        request_serializer=wandb_dot_proto_dot_wandb__internal__pb2.ConfigRecord.SerializeToString,
        response_deserializer=wandb_dot_proto_dot_wandb__internal__pb2.ConfigResult.FromString,
        )
    self.Output = channel.unary_unary(
        '/wandb_internal.InternalService/Output',
        request_serializer=wandb_dot_proto_dot_wandb__internal__pb2.OutputRecord.SerializeToString,
        response_deserializer=wandb_dot_proto_dot_wandb__internal__pb2.OutputResult.FromString,
        )
    self.ServerShutdown = channel.unary_unary(
        '/wandb_internal.InternalService/ServerShutdown',
        request_serializer=wandb_dot_proto_dot_wandb__server__pb2.ServerShutdownRequest.SerializeToString,
        response_deserializer=wandb_dot_proto_dot_wandb__server__pb2.ServerShutdownResult.FromString,
        )
    self.ServerStatus = channel.unary_unary(
        '/wandb_internal.InternalService/ServerStatus',
        request_serializer=wandb_dot_proto_dot_wandb__server__pb2.ServerStatusRequest.SerializeToString,
        response_deserializer=wandb_dot_proto_dot_wandb__server__pb2.ServerStatusResult.FromString,
        )


class InternalServiceServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def RunUpdate(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def RunExit(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Log(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Summary(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Config(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Output(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def ServerShutdown(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def ServerStatus(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_InternalServiceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'RunUpdate': grpc.unary_unary_rpc_method_handler(
          servicer.RunUpdate,
          request_deserializer=wandb_dot_proto_dot_wandb__internal__pb2.RunRecord.FromString,
          response_serializer=wandb_dot_proto_dot_wandb__internal__pb2.RunUpdateResult.SerializeToString,
      ),
      'RunExit': grpc.unary_unary_rpc_method_handler(
          servicer.RunExit,
          request_deserializer=wandb_dot_proto_dot_wandb__internal__pb2.RunExitRecord.FromString,
          response_serializer=wandb_dot_proto_dot_wandb__internal__pb2.RunExitResult.SerializeToString,
      ),
      'Log': grpc.unary_unary_rpc_method_handler(
          servicer.Log,
          request_deserializer=wandb_dot_proto_dot_wandb__internal__pb2.HistoryRecord.FromString,
          response_serializer=wandb_dot_proto_dot_wandb__internal__pb2.HistoryResult.SerializeToString,
      ),
      'Summary': grpc.unary_unary_rpc_method_handler(
          servicer.Summary,
          request_deserializer=wandb_dot_proto_dot_wandb__internal__pb2.SummaryRecord.FromString,
          response_serializer=wandb_dot_proto_dot_wandb__internal__pb2.SummaryResult.SerializeToString,
      ),
      'Config': grpc.unary_unary_rpc_method_handler(
          servicer.Config,
          request_deserializer=wandb_dot_proto_dot_wandb__internal__pb2.ConfigRecord.FromString,
          response_serializer=wandb_dot_proto_dot_wandb__internal__pb2.ConfigResult.SerializeToString,
      ),
      'Output': grpc.unary_unary_rpc_method_handler(
          servicer.Output,
          request_deserializer=wandb_dot_proto_dot_wandb__internal__pb2.OutputRecord.FromString,
          response_serializer=wandb_dot_proto_dot_wandb__internal__pb2.OutputResult.SerializeToString,
      ),
      'ServerShutdown': grpc.unary_unary_rpc_method_handler(
          servicer.ServerShutdown,
          request_deserializer=wandb_dot_proto_dot_wandb__server__pb2.ServerShutdownRequest.FromString,
          response_serializer=wandb_dot_proto_dot_wandb__server__pb2.ServerShutdownResult.SerializeToString,
      ),
      'ServerStatus': grpc.unary_unary_rpc_method_handler(
          servicer.ServerStatus,
          request_deserializer=wandb_dot_proto_dot_wandb__server__pb2.ServerStatusRequest.FromString,
          response_serializer=wandb_dot_proto_dot_wandb__server__pb2.ServerStatusResult.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'wandb_internal.InternalService', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
