# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from . import gptchat_v1_pb2 as gptchat__v1__pb2


class GPTChatStub(object):
    """Service definition. 1 per file
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.get_models = channel.unary_unary(
                '/giga.controller.v1.GPTChat/get_models',
                request_serializer=gptchat__v1__pb2.request_models_msg.SerializeToString,
                response_deserializer=gptchat__v1__pb2.model_response_msg.FromString,
                )
        self.get_model_info = channel.unary_unary(
                '/giga.controller.v1.GPTChat/get_model_info',
                request_serializer=gptchat__v1__pb2.request_model_info_msg.SerializeToString,
                response_deserializer=gptchat__v1__pb2.model_info_msg.FromString,
                )
        self.post_chat = channel.unary_unary(
                '/giga.controller.v1.GPTChat/post_chat',
                request_serializer=gptchat__v1__pb2.request_chat_msg.SerializeToString,
                response_deserializer=gptchat__v1__pb2.gpt_answer_msg.FromString,
                )


class GPTChatServicer(object):
    """Service definition. 1 per file
    """

    def get_models(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def get_model_info(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def post_chat(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_GPTChatServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'get_models': grpc.unary_unary_rpc_method_handler(
                    servicer.get_models,
                    request_deserializer=gptchat__v1__pb2.request_models_msg.FromString,
                    response_serializer=gptchat__v1__pb2.model_response_msg.SerializeToString,
            ),
            'get_model_info': grpc.unary_unary_rpc_method_handler(
                    servicer.get_model_info,
                    request_deserializer=gptchat__v1__pb2.request_model_info_msg.FromString,
                    response_serializer=gptchat__v1__pb2.model_info_msg.SerializeToString,
            ),
            'post_chat': grpc.unary_unary_rpc_method_handler(
                    servicer.post_chat,
                    request_deserializer=gptchat__v1__pb2.request_chat_msg.FromString,
                    response_serializer=gptchat__v1__pb2.gpt_answer_msg.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'giga.controller.v1.GPTChat', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class GPTChat(object):
    """Service definition. 1 per file
    """

    @staticmethod
    def get_models(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/giga.controller.v1.GPTChat/get_models',
            gptchat__v1__pb2.request_models_msg.SerializeToString,
            gptchat__v1__pb2.model_response_msg.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def get_model_info(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/giga.controller.v1.GPTChat/get_model_info',
            gptchat__v1__pb2.request_model_info_msg.SerializeToString,
            gptchat__v1__pb2.model_info_msg.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def post_chat(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/giga.controller.v1.GPTChat/post_chat',
            gptchat__v1__pb2.request_chat_msg.SerializeToString,
            gptchat__v1__pb2.gpt_answer_msg.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
