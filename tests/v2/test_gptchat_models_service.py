import json

import grpc
from google.protobuf.json_format import MessageToJson

from interfaces.python import GigaChatGrpcInterface


async def test_list_models(async_grpc_gc_client: GigaChatGrpcInterface):
    # Basic test
    _grpc_resp = await async_grpc_gc_client.list_models()
    models = json.loads(MessageToJson(_grpc_resp))

    assert models.get('models') is not None
    assert len(models['models']) > 0


async def test_get_model_info(async_grpc_gc_client: GigaChatGrpcInterface):
    # Basic test
    _grpc_resp = await async_grpc_gc_client.get_model_info('GigaChat:latest')
    model_info = json.loads(MessageToJson(_grpc_resp))

    assert model_info.get('model') is not None
    assert model_info['model'].get('object') is not None

    # Model doesn't exist
    try:
        await async_grpc_gc_client.get_model_info('GigaChat9913')
    except grpc.RpcError as error:
        assert error.code() is grpc.StatusCode.NOT_FOUND
