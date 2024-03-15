import json

import grpc
from google.protobuf.json_format import MessageToDict

from . import utils, base
from .protobufs import *


class ChatService(pb2_grpc.ChatServiceServicer, base.BaseServiceTemplate):

    async def Chat(self, request: pb2.ChatRequest, context: grpc.ServicerContext) -> pb2.ChatResponse:
        self.logger.debug('Gigachat chat call')

        options: dict = MessageToDict(request.options, preserving_proto_field_name=True)
        if request.options.HasField('optional_flags'):
            _raw = request.options.optional_flags.decode('utf-8')
            _extra_options = json.loads(_raw)

            options.pop('optional_flags')
            options = {**options, **_extra_options}

        messages = [MessageToDict(_msg) for _msg in request.messages]
        payload = {
            'model': request.model,
            'messages': messages,
            **options
        }

        async with base.GcResponseManager(logger=self.logger, context=context):
            chat_completion = await utils.chat(*self.gc_base_args, payload=payload)
            return pb2.ChatResponse(**chat_completion)
