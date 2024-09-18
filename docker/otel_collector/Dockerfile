FROM otel/opentelemetry-collector-contrib:latest 

# copy the config file to the /etc folder
COPY ./docker/otel_collector/config/otel_collector.config.yaml /etc/otel_collector.config.yaml

# default user and group id
# otel/opentelemetry-collector-contrib image is already using 10001 for the 
# user, but none for the group, so we're setting it here
# using uid instead of user names since the base image is based on scratch
# and we can't use tools like groupadd or useradd
ARG USER_UID=10001
ARG USER_GID=10001

# define the running user
USER ${USER_UID}:${USER_GID}

# otel_collector env vars
# OTLP upstream endpoint used by the collector to centralize traces and metrics 
ENV OTEL_EXPORTER_OTLP_ENDPOINT=jaeger:4317
ENV OTEL_EXPORTER_OTLP_INSECURE=true

# represents a label to tag logging and tracing data with the environment name
ENV TRACING_ENVIRONMENT=dev

# we're binding to all interfaces, so we need to disable the UseLocalHostAsDefaultHost feature gate
CMD ["--config", "/etc/otel_collector.config.yaml", "--feature-gates", "-component.UseLocalHostAsDefaultHost"]