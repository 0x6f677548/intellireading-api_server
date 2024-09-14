""" Main module for the API server. """

import logging
import os

import uvicorn
from fastapi import FastAPI, Request
from intellireading.api_server.middleware.cors import CORSMiddleware
from intellireading.api_server.middleware.exceptions import ExceptionHandlerMiddleware
from intellireading.api_server.middleware.logcall import LogCallMiddleware
from intellireading.api_server.middleware.requestid import RequestIdMiddleware
from intellireading.api_server.middleware.responsetime import ResponseTimeMiddleware
from intellireading.api_server.monitoring.instrumentation import (
    current_span_set_error,
    init_global_meter_provider,
    init_global_tracer_provider,
)
from intellireading.api_server.monitoring.logutils import init_logging_from_json_file
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.trace import Span
from intellireading.api_server.routers.authentication import init_authentication
from intellireading.api_server.routers.metaguiding import router as metaguiding_router
from intellireading.api_server.utils.configuration import ConfigDict

# region configuration loading
# check if the config file exists and load it.
# all code that uses server_config should check if it is None

_server_config = {}


# load the config file from environment variable API_SERVER_CONFIG_FILE.
# if the environment variable is not set, use the default config file
# which is located in ../config/api_server.config.json
_SERVER_CONFIG_FILE = os.environ.get(
    "API_SERVER_CONFIG_FILE", "./config/api_server.config.json"
)

# check if we have a relative path and if so, make it absolute
if not os.path.isabs(_SERVER_CONFIG_FILE):
    _SERVER_CONFIG_FILE = os.path.abspath(
        os.path.join(os.path.dirname(__file__), _SERVER_CONFIG_FILE)
    )


# region configure logging
#   this should be done before loading _server_config
#   to ensure that the logging is configured before the config is loaded

init_logging_from_json_file(_SERVER_CONFIG_FILE)
_logger = logging.getLogger(__name__)
_logger.info("Starting server")
# endregion


if os.path.exists(_SERVER_CONFIG_FILE):
    _server_config = ConfigDict.from_json_file(_SERVER_CONFIG_FILE)
# endregion


# region instrumentation

init_global_tracer_provider(_server_config)

init_global_meter_provider(_server_config)


def _server_request_hook(span: Span, scope: dict):
    """
    This function is called by the FastAPI instrumentation when a request is received.
    It is used to inject the request id into the span
    This is important as we will auto instrument the application, and a span will already
    be in-progress when the routers are called.
    """

    # TODO: this can be done dynamically by using config somehow # pylint: disable=fixme
    # ex: what if we want to inject the user id into the span?
    if span and span.is_recording():
        # inject request_id into span
        if "state" in scope:
            state = scope["state"]
            if "request_id" in state:
                request_id = state["request_id"]
                span.set_attribute("X-Request-ID", request_id)

        # inject headers into span
        headers_to_inject = ["x-forwarded-for", "x-real-ip", "origin"]
        if scope["headers"]:
            for header in scope["headers"]:
                _header_name = header[0].decode("utf-8")
                if _header_name in headers_to_inject:
                    _header_value = header[1].decode("utf-8")
                    span.set_attribute(_header_name, _header_value)


app: FastAPI = FastAPI()
FastAPIInstrumentor.instrument_app(app, server_request_hook=_server_request_hook)
# endregion

# region init authentication module
init_authentication(_server_config)
# endregion

# region import routers
app.include_router(metaguiding_router)
# endregion


# region adding middleware to the pipeline.
# order is important: the first middleware added will be the last one to be executed

# CORS configuration and middleware
app.add_middleware(CORSMiddleware, config=_server_config)

# Response time middleware
app.add_middleware(ResponseTimeMiddleware, config=_server_config)

# Logging middleware

app.add_middleware(LogCallMiddleware, config=_server_config)

# Request id middleware

app.add_middleware(RequestIdMiddleware, config=_server_config)

# Exception handler middleware

app.add_middleware(ExceptionHandlerMiddleware, config=_server_config)
# endregion

_logger.info("Server started, routers included and instrumentation added")


@app.exception_handler(Exception)
async def exception_callback(request: Request, exc: Exception):
    """
    This is the default exception handler for FastAPI.
    It is called when an exception is raised in the server
    and it is not handled by any other exception handler.
    If ExceptionHandlerMiddleware is the last middleware in the pipeline,
    this handler will be called only if the exception
    happens inside the middleware itself. Otherwise, the exception
    will be handled by ExceptionHandlerMiddleware.
    Otherwise, the exception will be handled by the default exception
    handler of FastAPI (which is the same as this one)
    """
    # try to get the request id from the request state
    request_id = (
        request.state.request_id if hasattr(request.state, "request_id") else None
    )
    _logger.exception(
        "Request id %s: Critical exception '%s' \
                      occurred while processing request for %s",
        request_id,
        exc,
        request.url,
    )

    # set the status of the current span to error

    current_span_set_error(exc)

def entrypoint():
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    entrypoint()
