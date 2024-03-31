ARG VARIANT="3"

FROM mcr.microsoft.com/vscode/devcontainers/python:${VARIANT}

ARG POETRY_VERSION="1.2.1"
ARG POETRY_SRC="https://install.python-poetry.org"

USER vscode
WORKDIR /home/vscode

RUN curl -sSL "${POETRY_SRC}" | python3 - --version ${POETRY_VERSION}

RUN mkdir -p .config/git \
 && echo ".vscode/*" >> .config/git/ignore \
 && echo "*.code-workspace" >> .config/git/ignore \
 && echo ".history/" >> .config/git/ignore
