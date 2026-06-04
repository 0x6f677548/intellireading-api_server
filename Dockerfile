ARG UV_VERSION=0.11.18
FROM ghcr.io/astral-sh/uv:${UV_VERSION} AS uv-dist

FROM python:3.13-slim AS builder
ENV PIP_ROOT_USER_ACTION=ignore

WORKDIR /app

COPY --from=uv-dist /uv /uvx /usr/local/bin/

COPY pyproject.toml uv.lock README.md ./
COPY .dependencies /app/.dependencies
COPY src src/

RUN uv export --no-dev --no-emit-project -o requirements.txt \
 && uv build

FROM python:3.13-slim
ENV PIP_ROOT_USER_ACTION=ignore

LABEL org.opencontainers.image.source=https://github.com/hugobatista/intellireading-api_server

RUN addgroup --system app && adduser --system --group app

COPY --from=builder /app/requirements.txt ./
RUN pip install --no-cache --upgrade pip \
 && pip install --no-cache -r ./requirements.txt

# Install private .whl dependencies
COPY --from=builder /app/.dependencies /app/.dependencies
RUN if ls -1 /app/.dependencies/*.whl >/dev/null 2>&1; then \
    pip install --no-cache-dir /app/.dependencies/*.whl; \
  fi

COPY --from=builder /app/dist/*.whl /tmp/
RUN pip install --no-cache-dir /tmp/*.whl && rm /tmp/*.whl

ENV API_SERVER_API_KEY="devapikey"
ENV TURNSTILE_ENABLED=false

USER app
CMD ["api-server"]
