import grpc
from google.protobuf.json_format import MessageToDict

from interfaces.python import GigaChatGrpcInterface


async def test_embeddings(async_grpc_gc_client: GigaChatGrpcInterface):
    # Basic test
    _grpc_resp = await async_grpc_gc_client.get_embeddings(['Что ты такое?', 'Как дела?'])
    embeddings: dict = MessageToDict(_grpc_resp)

    assert embeddings.get('embeddings') is not None
    assert len(embeddings['embeddings']) == 2

    # Params validation check
    _grpc_resp = await async_grpc_gc_client.get_embeddings('Что ты такое?')
    embeddings: dict = MessageToDict(_grpc_resp)

    assert embeddings.get('embeddings') is not None

    # Incorrect Embeddings model
    try:
        await async_grpc_gc_client.get_embeddings('Что ты такое?', model='GigaChat')
    except grpc.RpcError as error:
        assert error.code() is grpc.StatusCode.NOT_FOUND
