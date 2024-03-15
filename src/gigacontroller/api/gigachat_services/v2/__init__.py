from .models_service import ModelsService
from .chat_service import ChatService
from .embeddings_service import EmbeddingsService
from .protobufs import gptchat_v2_pb2_grpc as pb2_grpc


class Services:
    def __init__(self, gc_client, logger, gc_call_retry):
        self.models_service = ModelsService(gc_client, logger, gc_call_retry)
        self.embeddings_service = EmbeddingsService(gc_client, logger, gc_call_retry)
        self.chat_service = ChatService(gc_client, logger, gc_call_retry)

    async def add_services(self, server):
        pb2_grpc.add_ModelsServiceServicer_to_server(self.models_service, server)
        pb2_grpc.add_EmbeddingsServiceServicer_to_server(self.embeddings_service, server)
        pb2_grpc.add_ChatServiceServicer_to_server(self.chat_service, server)


__all__ = [
    'Services'
]
