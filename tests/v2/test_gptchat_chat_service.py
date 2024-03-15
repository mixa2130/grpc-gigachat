import json

from google.protobuf.json_format import MessageToDict

from interfaces.python import GigaChatGrpcInterface


def test_form_gc_options_payload(async_grpc_gc_client: GigaChatGrpcInterface):
    user_options = {
        "max_tokens": 1024,
        "n": 2,
        "repetition_penalty": 1.1,
        "temperature": 1,
        'top_p': 0.1,
    }

    assert async_grpc_gc_client._form_gc_options_payload(user_options) == user_options

    user_options['update_interval'] = 0
    assert async_grpc_gc_client._form_gc_options_payload(user_options) == {
        "max_tokens": 1024,
        "n": 2,
        "repetition_penalty": 1.1,
        "temperature": 1,
        'top_p': 0.1,
        'optional_flags': (json.dumps({'update_interval': 0})).encode('utf-8')
    }


async def test_chat(async_grpc_gc_client: GigaChatGrpcInterface):
    user_options = {
        "max_tokens": 1024,
        "n": 2,
        "repetition_penalty": 1.1,
        "temperature": 1,
    }
    payload = {
        "model": "GigaChat:latest",
        "messages": [
            {
                "role": "user",
                "content": "Как твои дела?"
            }
        ]
    }

    # Base tests
    _grpc_resp = await async_grpc_gc_client.chat(messages=payload['messages'],
                                                 model=payload['model'],
                                                 user_options=user_options)
    choices: dict = MessageToDict(_grpc_resp)
    assert choices.get('choices') is not None
    assert len(choices['choices']) == user_options['n']

    # Test multiple messages

    payload['messages'] = [
        {
            "role": "user",
            "content": "Когда уже ИИ захватит этот мир?"
        },
        {
            "role": "assistant",
            "content": "Пока что это не является неизбежным событием. Несмотря на то, что искусственный интеллект (ИИ) развивается быстрыми темпами и может выполнять сложные задачи все более эффективно, он по-прежнему ограничен в своих возможностях и не может заменить полностью человека во многих областях. Кроме того, существуют этические и правовые вопросы, связанные с использованием ИИ, которые необходимо учитывать при его разработке и внедрении."
        },
        {
            "role": "user",
            "content": "Думаешь, у нас еще есть шанс?"
        }
    ]
    _grpc_resp = await async_grpc_gc_client.chat(messages=payload['messages'],
                                                 model=payload['model'],
                                                 user_options=user_options)
    choices: dict = MessageToDict(_grpc_resp)
    assert choices.get('choices') is not None
    assert len(choices['choices']) == user_options['n']

    # Stream options in base request
    user_options['stream'] = True

    try:
        await async_grpc_gc_client.chat(messages=payload['messages'],
                                        model=payload['model'],
                                        user_options=user_options)
    except AttributeError:
        assert True
    else:
        assert False

    # No user_options, no model
    _grpc_resp = await async_grpc_gc_client.chat(messages=payload['messages'])
    choices: dict = MessageToDict(_grpc_resp)
    assert choices.get('choices') is not None
    assert len(choices['choices']) == 1
