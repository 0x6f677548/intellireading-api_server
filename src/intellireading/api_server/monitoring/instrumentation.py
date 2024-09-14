from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry import metrics
from opentelemetry.trace.status import Status, StatusCode
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.resources import (
    SERVICE_NAME,
    Resource,
    SERVICE_VERSION,
    SERVICE_INSTANCE_ID,
)
from intellireading.api_server.utils.dynamicloading import create_class_from_config

import logging

_logger = logging.getLogger(__name__)


# region config
def _get_section(config, section_name) -> tuple:
    """
    Returns a dictionary with:
    - the section config
    - a boolean indicating if the section is enabled
    - the instrumentation config
    - a boolean indicating if the instrumentation is enabled
    """
    if config is None:
        config = {}

    _instrumentation_config = config.get("instrumentation", {})

    # get the instrumentation enabled flag and make sure it is a boolean
    # _instrumentation_enabled = get_bool_value(_instrumentation_config, 'enabled', False)
    _instrumentation_enabled = _instrumentation_config.get("enabled", False)

    if _logger.isEnabledFor(logging.DEBUG):
        _logger.debug("Instrumentation config: %s", config)

    _section_config = _instrumentation_config.get(section_name, {})

    _section_enabled = _section_config.get("enabled", False)
    _logger.info(
        "Instrumentation %s enabled: %s, instrumentation enabled: %s",
        section_name,
        _section_enabled,
        _instrumentation_enabled,
    )
    return (
        _section_config,
        _section_enabled,
        _instrumentation_config,
        _instrumentation_enabled,
    )


def _get_resource(instrumentation_config):
    """
    Returns a resource with the service name, version and instance id
    """
    return Resource(
        attributes={
            SERVICE_NAME: instrumentation_config.get(
                "service_name", "server.api.intellireading"
            ),
            SERVICE_VERSION: instrumentation_config.get("service_version", "0.1.0"),
            SERVICE_INSTANCE_ID: instrumentation_config.get(
                "service_instance_id", "server.api.intellireading-1"
            ),
        }
    )


# endregion


# region span helpers
def _if_span_valid(span, f):
    if span is not None and span is not trace.INVALID_SPAN:
        f()


def current_span_set_attribute(attribute_name: str, attribute_value: str):
    _span = trace.get_current_span()
    _if_span_valid(_span, lambda: _span.set_attribute(attribute_name, attribute_value))


def current_span_add_warning_event(event_name: str, message: str):
    _span = trace.get_current_span()
    _if_span_valid(_span, lambda: _span.add_event(event_name, {"message": message}))
    _if_span_valid(_span, lambda: _span.set_attribute("warning", True))


def current_span_set_error(e: Exception):
    _span = trace.get_current_span()
    _if_span_valid(_span, lambda: _span.set_status(Status(StatusCode.ERROR)))
    _if_span_valid(_span, lambda: _span.record_exception(e))


# endregion


# region Metrics


def _create_metric_reader(reader_config):
    return create_class_from_config(reader_config)


def init_global_meter_provider(config):
    """
    Initializes the global meter provider with the given config.
    It checks if the instrumentation section is enabled and if the metrics section is enabled.
    """
    (
        _metrics_config,
        _metrics_enabled,
        _instrumentation_config,
        _instrumentation_enabled,
    ) = _get_section(config, "metrics")

    if not _instrumentation_enabled or not _metrics_enabled:
        return

    _resource = _get_resource(_instrumentation_config)

    _logger.info("Metrics: Service name: %s", _resource.attributes[SERVICE_NAME])
    _logger.info("Metrics: Service version: %s", _resource.attributes[SERVICE_VERSION])
    _logger.info(
        "Metrics: Service instance id: %s", _resource.attributes[SERVICE_INSTANCE_ID]
    )

    _metric_readers_config = _metrics_config.get("readers", [])
    _metric_readers = []
    for _reader_config in _metric_readers_config:
        if _reader_config.get("enabled", True):
            _logger.info("Adding metric reader with config: %s", _reader_config)
            _metric_readers.append(_create_metric_reader(_reader_config))

    metrics.set_meter_provider(
        MeterProvider(metric_readers=_metric_readers, resource=_resource)
    )


# endregion

# region Tracing


def _create_span_processor(span_processor_config):
    return create_class_from_config(span_processor_config)


def init_global_tracer_provider(config):
    """
    Initializes the global tracer provider with the given config.
    """

    (
        _tracing_config,
        _tracing_enabled,
        _instrumentation_config,
        _instrumentation_enabled,
    ) = _get_section(config, "tracing")
    if not _instrumentation_enabled or not _tracing_enabled:
        return

    _resource = _get_resource(_instrumentation_config)

    _logger.info("Tracing: Service name: %s", _resource.attributes[SERVICE_NAME])
    _logger.info("Tracing: Service version: %s", _resource.attributes[SERVICE_VERSION])
    _logger.info(
        "Tracing: Service instance id: %s", _resource.attributes[SERVICE_INSTANCE_ID]
    )

    _provider = TracerProvider(resource=_resource)

    _span_processors_enabled_count = 0
    _span_processors = _tracing_config.get("span_processors", [])
    for _span_processor_config in _span_processors:
        if _span_processor_config.get("enabled", True):
            _logger.info(
                "Adding span processor with config: %s", _span_processor_config
            )
            _span_processor = _create_span_processor(_span_processor_config)
            _provider.add_span_processor(_span_processor)
            _span_processors_enabled_count += 1

    _logger.info("Span processors enabled: %s", _span_processors_enabled_count)

    trace.set_tracer_provider(_provider)


# endregion
