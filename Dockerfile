########################### Builder ############################
FROM python:3.11 as builder

RUN apt-get update

ENV POETRY_HOME=/opt/poetry \
    POETRY_VENV=/opt/poetry-venv

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_INDEX_URL=${ARTIFACT_URL} \
    PIP_CERT=${SBEROSC_TRUSTED_CERT} \
    POETRY_VERSION=1.6.0

# Install poetry separated from system interpreter
RUN python3 -m venv ${POETRY_VENV} \
    && ${POETRY_VENV}/bin/pip install -U pip setuptools \
    && ${POETRY_VENV}/bin/pip install poetry==${POETRY_VERSION}

# Add `poetry` to PATH
ENV PATH="${PATH}:${POETRY_VENV}/bin"

WORKDIR /app

COPY poetry.lock pyproject.toml ./
COPY src/ ./src/


RUN poetry check
RUN poetry build && ${POETRY_VENV}/bin/pip install dist/*.whl

########################### Финальный образ ############################
FROM python:3.11-slim-bookworm as final

ENV TZ=Europe/Moscow

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    POETRY_VENV=/opt/poetry-venv \
    PATH="${PATH}:${POETRY_VENV}/bin"


COPY --from=builder ${POETRY_VENV} ${POETRY_VENV}
RUN ln -snf ${POETRY_VENV}/bin/giga-controller /usr/local/bin/

ENTRYPOINT ["giga-controller"]
EXPOSE 50051