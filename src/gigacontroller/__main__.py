import typing as tp

import asyncio
import grpc

from . import api


async def grpc_server(cleanup_coroutines: tp.List[tp.Coroutine]) -> tp.NoReturn:
    from gigacontroller.context import APP_CTX

    server = grpc.aio.server()
    gigachat_grpc_services = api.V2GigaChatServices(APP_CTX.gc_client, APP_CTX.logger, APP_CTX.gc_call_retry)
    await gigachat_grpc_services.add_services(server)

    server.add_insecure_port(APP_CTX.socket_addr)
    await server.start()

    APP_CTX.logger.info(f"Server started, listening on {APP_CTX.socket_addr}")

    async def server_graceful_shutdown():
        APP_CTX.logger.info("Starting graceful shutdown...")
        # Shuts down the server with 5 seconds of grace period. During the
        # grace period, the server won't accept new connections and allow
        # existing RPCs to continue within the grace period.
        await server.stop(5)

    cleanup_coroutines.append(server_graceful_shutdown())
    await server.wait_for_termination()


def main():
    from gigacontroller.context import APP_CTX

    APP_CTX.on_startup()

    # Coroutines to be invoked when the event loop is shutting down.
    _cleanup_coroutines = []

    APP_CTX.logger.info("running the gRPC server")
    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(grpc_server(_cleanup_coroutines))
    finally:
        loop.run_until_complete(*_cleanup_coroutines)
        loop.close()


if __name__ == "__main__":
    main()
