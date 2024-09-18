FROM 0x6f677548/nginx-unit:1.32.1-python3.12-slim

# note on user permissions
# although the container runs as root, unit runs as the unit user
# this is important to note when setting permissions on files and directories

RUN mkdir /app

COPY ./.dependencies /app/.dependencies
COPY ./dist /app/dist

# install any dependencies that are required by the application and were provided as whl files
# this may include dependencies that are not available in the public pypi repository (if any)
RUN pip install --no-cache-dir /app/.dependencies/*.whl

# install the application itself (this requires that the application is packaged as a whl file)
# ensure that the application is packaged as a whl file and is present in the /app/dist folder
# Packaging can be done by running hatch build in the root of the application
RUN pip install --no-cache-dir /app/dist/*.whl

# extract the whl files to /app
# this is done so that the application can be run by nginx unit
RUN pip install --no-deps --target /app /app/dist/*.whl

# provide access to the application to the unit user
RUN chown -R unit:unit /app

# set the environment variables
# used by api_server to identify itself on logs, otel, etc.
ENV SERVICE_NAME=server.api.intellireading
ENV VERSION=dev
ENV INSTANCE_ID=dev-1

# API key for request validation
ENV API_KEY="dev-api-key"

# Turnstile configuration
ENV TURNSTILE_ENABLED=false
ENV TURNSTILE_SECRET_KEY=<turnstile-secret-key>

# OpenTelemetry configuration
ENV OTEL_ENABLED=true
ENV OTEL_TRACING_ENABLED=true
ENV OTEL_METRICS_ENABLED=false

# OpenTelemetry exporter configuration
ENV OTEL_EXPORTER_OTLP_ENDPOINT=otel_collector:4317
ENV OTEL_EXPORTER_OTLP_INSECURE=true

# Configuration file path used when booting
ENV CONFIG_FILE=/app/intellireading/api_server/config/api_server.config.json


# copy the nginx config file to the /docker-entrypoint.d folder
# this is where nginx unit will look for the config file
RUN cp /app/intellireading/api_server/config/nginx.unit.config.json /docker-entrypoint.d/

# copy the entrypoint.sh file to the /app folder, make it executable and set it as the entrypoint
COPY ./docker/api_server/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]