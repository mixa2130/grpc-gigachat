import os
import typing as tp

from dotenv import load_dotenv

load_dotenv()


def common_env_validator(env_name) -> str:
    value = os.getenv(env_name)

    if value is None:
        raise ValueError(f"Required parameter {env_name} is not specified")

    return value


class GigaChatMtls(tp.NamedTuple):
    cert_file: str
    key_file: str
    ca_bundle_file: str
    base_url: str


class GigaChatOauth2(tp.NamedTuple):
    scope: str
    credentials: str
    base_url: str
    verify_ssl_certs: bool = False


class Secrets:

    @property
    def log_lvl(self):
        if self.debug_mode is True:
            return 'DEBUG'
        else:
            return 'INFO'

    @property
    def gigachat_auth_creds(self) -> GigaChatOauth2 | GigaChatMtls:
        return self._gc_auth_creds

    @gigachat_auth_creds.setter
    def gigachat_auth_creds(self, value: str):
        _gigachat_api_url = common_env_validator('GIGACHAT_API_BASE_URL')

        if value == 'oauth2':
            _gigachat_scope = common_env_validator('GIGACHAT_SCOPE')
            _gigachat_token = common_env_validator('GIGACHAT_CREDENTIALS')

            self._gc_auth_creds = GigaChatOauth2(scope=_gigachat_scope,
                                                 credentials=_gigachat_token,
                                                 base_url=_gigachat_api_url)
        else:
            _gigachat_api_cert_file_path = self.path_from_env_validator('GIGACHAT_API_CERT_FILE')
            _gigachat_api_key_file_path = self.path_from_env_validator('GIGACHAT_API_KEY_FILE')
            _gigachat_api_ca_file_path = self.path_from_env_validator('GIGACHAT_API_CA_BUNDLE')

            self._gc_auth_creds = GigaChatMtls(cert_file=_gigachat_api_cert_file_path,
                                               key_file=_gigachat_api_key_file_path,
                                               ca_bundle_file=_gigachat_api_ca_file_path,
                                               base_url=_gigachat_api_url)

    def __init__(self):
        self.debug_mode = self.str2bool_validator(os.getenv('DEBUG_MODE', False))
        self.app_host = os.getenv('APP_HOST', '0.0.0.0')
        self.app_port = os.getenv('APP_PORT', 50051)

        self.gigachat_auth_creds = common_env_validator('GIGACHAT_AUTH_TYPE')
        self.retry_limit = self.int_validator('RETRY_LIMIT', 3)
        self.retry_increment = self.int_validator('RETRY_INCREMENT', 2)

    @staticmethod
    def str2bool_validator(str_val: str | bool) -> bool:
        """Converts str boolean value to python bool"""
        if isinstance(str_val, bool):
            return str_val

        _str_val = str_val.strip().lower()
        if _str_val == 'true':
            return True
        if _str_val == 'false':
            return False

        raise ValueError('Boolean value expected for DEBUG_MODE')

    @staticmethod
    def path_from_env_validator(env_name: str):
        value = common_env_validator(env_name)

        if not os.path.exists(value):
            raise ValueError(f"Specified in {env_name} path doesn't exist")

        return value

    @staticmethod
    def int_validator(env_name: str, default_value: int):
        try:
            value = int(os.getenv(env_name, default_value))

            if value == 0:
                raise TypeError
        except TypeError | ValueError:
            raise ValueError(f"Please specify in {env_name} correct integer value")

        return value
