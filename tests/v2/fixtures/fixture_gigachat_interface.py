import os
import typing as tp
import pytest

from interfaces.python import GigaChatGrpcInterface
from dotenv import load_dotenv

load_dotenv()


@pytest.fixture(scope="session")
async def async_grpc_gc_client() -> tp.AsyncGenerator[GigaChatGrpcInterface, None]:
    gc_interface = GigaChatGrpcInterface(
        socker_addr=f"{os.getenv('TEST_SERVER_HOST')}:{os.getenv('TEST_SERVER_PORT')}")

    await gc_interface.on_startup()
    yield gc_interface
    await gc_interface.on_shutdown()
