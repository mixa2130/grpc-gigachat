import grpc

from . import utils, base
from .protobufs import *


class EmbeddingsService(pb2_grpc.EmbeddingsServiceServicer, base.BaseServiceTemplate):

    async def Embeddings(self, request: pb2.EmbeddingsRequest, context: grpc.ServicerContext) -> pb2.EmbeddingsResponse:
        self.logger.debug('Get embeddings')

        kwargs = {'texts': list(request.input)}

        if request.HasField('model'):
            kwargs['model'] = request.model

        async with base.GcResponseManager(logger=self.logger, context=context):
            embeddings: dict = await utils.get_embeddings(*self.gc_base_args,
                                                          kwargs=kwargs)
            return pb2.EmbeddingsResponse(**embeddings)
