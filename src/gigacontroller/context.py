import sys
import httpx
import logging

from loguru import logger as async_logger
from gigachat import GigaChat
import tenacity
from gigachat.exceptions import AuthenticationError, ResponseError

from gigacontroller.config import Secrets


class AppContext:

    def __init__(self, secrets: Secrets):
        self.socket_addr = f"{secrets.app_host}:{secrets.app_port}"
        self.debug_mode = secrets.debug_mode

        async_logger.remove(0)
        async_logger.add(sys.stdout, level=secrets.log_lvl)

        self.logger = async_logger
        self.gc_client: GigaChat = GigaChat(
            **secrets.gigachat_auth_creds._asdict()
        )
        # ADD AUTH check after making connections

        self.gc_call_retry = tenacity.retry(
            stop=tenacity.stop_after_attempt(secrets.retry_limit),
            after=tenacity.after_log(self.logger, logging.WARNING),
            before=tenacity.before_log(self.logger, logging.DEBUG),
            retry=tenacity.retry_if_exception_type((ResponseError, AuthenticationError)),
            wait=tenacity.wait_incrementing(start=secrets.retry_increment, increment=secrets.retry_increment),
            reraise=True
        )
        self.logger.info(f"Retry options: limit={secrets.retry_limit}, increment={secrets.retry_increment}")

    def _check_gigachat_connection(self):
        try:
            models = self.gc_client.get_models()
            self.logger.info("Successfully authorized gigachat service")

            _available_models = '\n'.join(model.id_ for model in models.data)
            self.logger.info(f"Available models: \n{_available_models}")
        except AuthenticationError as exc:
            self.logger.error("Failed to authenticate at gigachat mtls service. Please check your auth certs")
            raise exc
        except httpx.ConnectError as exc:
            self.logger.error("GigaChat host unavailable")
            raise exc

    def on_startup(self):
        self._check_gigachat_connection()


APP_CTX = AppContext(Secrets())

__all__ = [
    'APP_CTX',
    'AppContext'
]
