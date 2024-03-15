import json

from gigachat.models import *


def model_to_dict(self) -> dict:
    return {
        'name': self.id_,
        'object': self.object_,
        'ownedBy': self.owned_by
    }


def models_to_dict(self) -> dict:
    return {
        'models': [model.to_dict() for model in self.data]
    }


def embedding_to_dict(self) -> dict:
    return {
        "object": self.object_,
        "embedding": self.embedding,
        "index": self.index,
        "usage": json.loads(self.usage.json())
    }


def embeddings_to_dict(self) -> dict:
    res = {
        "embeddings": [embedding.to_dict() for embedding in self.data]
    }

    try:
        res["model"] = self.model
    except AttributeError:
        pass

    return res


def usage_to_dict(self) -> dict:
    res = {
        "prompt_tokens": self.prompt_tokens
    }

    try:
        res["completion_tokens"] = self.completion_tokens
    except AttributeError:
        pass

    try:
        res["total_tokens"] = self.total_tokens
    except AttributeError:
        pass

    return res


def messages_to_dict(self) -> dict:
    return {
        "role": str(self.role),
        "content": self.content
    }


def choices_to_dict(self) -> dict:
    return {
        "message": self.message.to_dict(),
        "finish_reason": str(self.finish_reason),
        "index": self.index
    }


def chat_completion_to_dict(self) -> dict:
    return {
        "choices": [_ch.to_dict() for _ch in self.choices],
        "usage": self.usage.to_dict(),
        "model": self.model,
        "timestamp": self.created
    }


Model.to_dict = model_to_dict
Models.to_dict = models_to_dict
Embedding.to_dict = embedding_to_dict
Embeddings.to_dict = embeddings_to_dict
Usage.to_dict = usage_to_dict
Messages.to_dict = messages_to_dict
Choices.to_dict = choices_to_dict
ChatCompletion.to_dict = chat_completion_to_dict
