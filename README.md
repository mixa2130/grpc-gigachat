# GigaController

## Project ENV

~~~dotenv
GIGACHAT_AUTH_TYPE=oauth2
GIGACHAT_SCOPE=...
GIGACHAT_CLIENT_SECRET=...
GIGACHAT_CREDENTIALS=...
GIGACHAT_API_BASE_URL=https://gigachat.devices.sberbank.ru/api/v1

TEST_SERVER_HOST=0.0.0.0
TEST_SERVER_PORT=50051
DEBUG_MODE=True
RETRY_LIMIT=3
RETRY_INCREMENT=2
~~~

## Guides

### Docker

~~~bash
docker build -t gigacontroller-final .
docker run -d --env-file .env --name='gigacontroller' -p 50051:50051 gigacontroller-final:latest
~~~

### Local

~~~bash
python3 src/gigacontroller/__main__.py
~~~

#### Update proto file

~~~bash
python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. service.proto
~~~

#### Tests

~~~bash
cd tests && pytest v2
~~~