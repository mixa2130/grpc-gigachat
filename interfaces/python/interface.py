import typing as tp
import json

import asyncio
import grpc
from loguru import logger

from gigacontroller.api.gigachat_services.v2.protobufs import *

_MAX_MESSAGE_LENGTH = 41943040


class GigaChatGrpcInterface:

    async def __aenter__(self):
        await self.on_startup()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_val is not None:
            self.logger.error(f"{exc_type}: {exc_val}")

        await self.on_shutdown()

    def __init__(self, socker_addr: str):
        self._channel = None
        self.models_stub = None
        self.embeddings_stub = None
        self.chat_stub = None

        self.logger = logger

        self._socket: str = socker_addr

    async def _init_grpc_stuff(self):
        self._channel = grpc.aio.insecure_channel(self._socket,
                                                  options=[
                                                      ('grpc.max_send_message_length', _MAX_MESSAGE_LENGTH),
                                                      ('grpc.max_receive_message_length', _MAX_MESSAGE_LENGTH),
                                                  ],
                                                  compression=grpc.Compression.Gzip)
        self.models_stub = pb2_grpc.ModelsServiceStub(self._channel)
        self.embeddings_stub = pb2_grpc.EmbeddingsServiceStub(self._channel)
        self.chat_stub = pb2_grpc.ChatServiceStub(self._channel)

        self.logger.info(f'gRPC Channel created: {self._socket}')

    async def on_startup(self):
        self.logger.debug("Initialising gRPC")
        await self._init_grpc_stuff()

    async def on_shutdown(self):
        self.logger.debug(f'Closing channel: {self._socket}..')
        await self._channel.close()
        self.logger.info(f'Successfully closed gRPC channel {self._socket}')

    async def list_models(self) -> pb2.ListModelsResponse:
        response: pb2.ListModelsResponse = await self.models_stub.ListModels(pb2.ListModelsRequest())
        return response

    async def get_model_info(self, model_id: str) -> pb2.RetrieveModelResponse:
        response: pb2.RetrieveModelResponse = await self.models_stub.RetrieveModel(
            pb2.RetrieveModelRequest(name=model_id))
        return response

    @staticmethod
    def _form_gc_options_payload(user_options: tp.Optional[dict]) -> dict:
        gc_options = {
            "n": 1,
            "max_tokens": 1024,
            "repetition_penalty": 1
        }

        if user_options is None:
            return gc_options

        optional_flags = dict()
        base_keys = {'temperature': 0,
                     'top_p': 0,
                     'n': 0,
                     'max_tokens': 0,
                     'repetition_penalty': 0,
                     'optional_flags': 0}

        for option_key in user_options.keys():
            if base_keys.get(option_key) is not None:
                gc_options[option_key] = user_options[option_key]
            else:
                optional_flags[option_key] = user_options[option_key]

        if optional_flags:
            gc_options['optional_flags'] = (json.dumps(optional_flags)).encode('utf-8')
        return gc_options

    async def chat(self, messages: list, user_options: tp.Optional[dict] = None,
                   model: str = "GigaChat:latest") -> pb2.ChatResponse:
        if user_options is not None and \
                (user_options.get('stream') is not None or user_options.get('update_interval') is not None):
            self.logger.error("'stream' and 'update_interval' can be used only in stream method")
            raise AttributeError("'stream' and 'update_interval' can be used only in stream method")

        options_payload = self._form_gc_options_payload(user_options)

        request = pb2.ChatRequest(model=model,
                                  messages=messages,
                                  options=options_payload)
        response: pb2.ChatResponse = await self.chat_stub.Chat(request)
        return response

    async def get_embeddings(self, texts: str | list[str], model: str = 'Embeddings'):
        self.logger.warning("It's a part of EXPERIMENTAL API")

        if isinstance(texts, str):
            texts = [texts]

        response: pb2.EmbeddingsResponse = await self.embeddings_stub.Embeddings(pb2.EmbeddingsRequest(
            input=texts,
            model=model
        ))
        return response

    def __del__(self):
        self.logger.debug("Closing client session")
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                loop.create_task(self.on_shutdown())
            else:
                loop.run_until_complete(self.on_shutdown())

            self.logger.info("Client session was successfully closed")
        except Exception as exc:
            self.logger.error(f"Unable to close client session cause of {repr(exc)}")
