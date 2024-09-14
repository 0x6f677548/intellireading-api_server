FROM otel/opentelemetry-collector-contrib:latest 

# default user and group id
# otel/opentelemetry-collector-contrib image is already using 10001 for the 
# user, but none for the group, so we're setting it here
# using uid instead of user names since the base image is based on scratch
# and we can't use tools like groupadd or useradd
ARG USER_UID=10001
ARG USER_GID=10001

# define the running user
USER ${USER_UID}:${USER_GID}

# we're binding to all interfaces, so we need to disable the UseLocalHostAsDefaultHost feature gate
CMD ["--config", "/etc/otel_collector.config.yaml", "--feature-gates", "-component.UseLocalHostAsDefaultHost"]