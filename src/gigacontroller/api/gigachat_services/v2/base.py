import json
import httpx

import grpc
from gigachat.exceptions import ResponseError

from . import utils


class BaseServiceTemplate:

    def __init__(self, gc_client, logger, gc_call_retry):
        self.gc_base_args = (gc_client, logger, gc_call_retry)
        self.logger = logger

    def _gigachat_response_error_handler(self, exc) -> (grpc.StatusCode, str):
        message: str = ''

        _code = int(exc.args[1])
        _description = exc.args[2].decode('utf-8')

        if _description is not None and _description:

            try:
                _description = json.loads(_description)

                if _description.get('message') is not None:
                    message = _description['message']
            except json.JSONDecodeError:
                self.logger.debug(f'Failed to convert {_description} to json')

        return utils.rest2grpc_codes(_code), message


class GcResponseManager:

    def __init__(self, logger, context):
        self.logger = logger
        self.context = context

    async def __aenter__(self):
        pass

    async def __aexit__(self, exc_type, exc_val, exc_tb):

        if exc_type is ResponseError:
            self.logger.opt(depth=1).error(f"Response error: {str(exc_val)}")
            await self.context.abort(*self._gigachat_response_error_handler(exc_val))

        elif exc_type in (httpx.ConnectError, httpx.TimeoutException, httpx.ConnectTimeout):
            _error_msg = f"Gigachat host is unavailable: {str(exc_val)}"

            self.logger.opt(depth=1).error(_error_msg)
            await self.context.abort(grpc.StatusCode.UNAVAILABLE, _error_msg)

    def _gigachat_response_error_handler(self, exc) -> (grpc.StatusCode, str):
        message: str = ''

        _code = int(exc.args[1])
        _description = exc.args[2].decode('utf-8')

        if _description is not None and _description:

            try:
                _description = json.loads(_description)

                if _description.get('message') is not None:
                    message = _description['message'].strip()
            except json.JSONDecodeError:
                self.logger.warning(f'Failed to convert {_description} to json')
                message = _description.strip()

        message += '. Url:' + str(exc.args[0])
        return utils.rest2grpc_codes(_code), message
