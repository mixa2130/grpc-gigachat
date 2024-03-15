from types import FunctionType

import grpc
from gigachat import GigaChat

from . import schemas


def rest2grpc_codes(status_code: int):
    if status_code == 400:
        return grpc.StatusCode.INVALID_ARGUMENT

    elif status_code == 403:
        return grpc.StatusCode.PERMISSION_DENIED

    elif status_code == 404:
        return grpc.StatusCode.NOT_FOUND

    elif status_code == 422:
        return grpc.StatusCode.FAILED_PRECONDITION

    else:
        return grpc.StatusCode.INTERNAL


async def list_models(gc_client: GigaChat, logger, gc_call_retry: FunctionType) -> dict:
    @gc_call_retry
    async def _wrap() -> schemas.Models:
        return await gc_client.aget_models()

    models = await _wrap()
    logger.debug('Successfully retrieved models list')

    return models.to_dict()


async def get_model_info(gc_client: GigaChat, logger, gc_call_retry: FunctionType, model_id: str) -> dict:
    @gc_call_retry
    async def _wrap() -> schemas.Model:
        return await gc_client.aget_model(model=model_id)

    model_info = await _wrap()
    logger.debug(f'Successfully retrieved {model_id} info')

    return model_info.to_dict()


async def get_embeddings(gc_client: GigaChat, logger, gc_call_retry: FunctionType, kwargs: dict) -> dict:
    @gc_call_retry
    async def _wrap() -> schemas.Embeddings:
        return await gc_client.aembeddings(**kwargs)

    embeddings = await _wrap()
    logger.debug('Successfully retrieved embeddings')

    return embeddings.to_dict()


async def chat(gc_client: GigaChat, logger, gc_call_retry: FunctionType, payload: dict) -> dict:
    @gc_call_retry
    async def _wrap() -> schemas.ChatCompletion:
        return await gc_client.achat(payload=payload)

    chat_completion = await _wrap()
    logger.debug("Successfully got chat response")

    return chat_completion.to_dict()


__all__ = [
    'list_models',
    'get_model_info',
    'get_embeddings'
]
