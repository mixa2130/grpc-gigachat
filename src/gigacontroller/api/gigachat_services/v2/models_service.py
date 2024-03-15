import grpc

from . import utils, base
from .protobufs import *


class ModelsService(pb2_grpc.ModelsServiceServicer, base.BaseServiceTemplate):

    async def ListModels(self, request: pb2.ListModelsRequest,
                         context: grpc.ServicerContext) -> pb2.ListModelsResponse:
        self.logger.debug('Start listing models')

        async with base.GcResponseManager(logger=self.logger, context=context):
            models: dict = await utils.list_models(*self.gc_base_args)
            return pb2.ListModelsResponse(**models)

    async def RetrieveModel(self, request: pb2.RetrieveModelRequest,
                            context: grpc.ServicerContext) -> pb2.RetrieveModelResponse:
        self.logger.debug('Gigachat model info call')

        async with base.GcResponseManager(logger=self.logger, context=context):
            model_info: dict = await utils.get_model_info(*self.gc_base_args,
                                                          model_id=request.name)
            return pb2.RetrieveModelResponse(model=model_info)
