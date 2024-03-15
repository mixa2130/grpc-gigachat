import json

from gigacontroller.context import APP_CTX
from . import gptchat_v1_pb2_grpc as pb2_grpc, gptchat_v1_pb2 as pb2


# A class for handling GPTChat service
class GPTChat(pb2_grpc.GPTChatServicer):

    async def get_models(self, request, context):
        APP_CTX.logger.debug('Gigachat model list call')

        res = await APP_CTX.gc_client.aget_models()
        models = res.json()
        APP_CTX.logger.debug('Successfully retrieved models list')

        return pb2.model_response_msg(data=models.encode('utf-8'))

    async def get_model_info(self, request, context):
        APP_CTX.logger.debug('Gigachat model info call')

        model_id = request.name
        res = await APP_CTX.gc_client.aget_model(model=model_id)
        model = res.json()
        APP_CTX.logger.debug(f'Successfully retrieved {model_id} info')

        return pb2.model_info_msg(data=model.encode('utf-8'))

    async def post_chat(self, request, context):
        APP_CTX.logger.debug('Gigachat chat call')
        payload = {}

        if request.HasField('chat_settings'):
            _chat_settings: dict = json.loads(request.chat_settings.decode('utf-8'))
            payload = {**_chat_settings}

        if request.HasField('model_name'):
            payload["model"] = request.model_name

        payload['messages'] = json.loads(request.messages.decode('utf-8'))
        res = await APP_CTX.gc_client.achat(payload=payload)
        chat_answer = res.json()
        APP_CTX.logger.debug('Successfully called chat')

        return pb2.gpt_answer_msg(data=chat_answer.encode('utf-8'))
