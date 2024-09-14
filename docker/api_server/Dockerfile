#FROM nginx/unit:1.29.1-python3.11 
#FROM unit:1.29.1-python3.11
FROM unit:python3.12
#FROM 0x6f677548/nginx-unit:1.29.1-python3.11-slim
RUN mkdir /app

COPY ./.dependencies /app/.dependencies
COPY ./dist /app/dist

# install any dependencies that are required by the application and were provided as whl files
# this may include dependencies that are not available in the public pypi repository (if any)
RUN pip install --no-cache-dir /app/.dependencies/*.whl

# install the application itself (this requires that the application is packaged as a whl file)
# ensure that the application is packaged as a whl file and is present in the /app/dist folder
# that can be done by running hatch build in the root of the application
RUN pip install --no-cache-dir /app/dist/*.whl

# extract the whl files to /app
# this is done so that the application can be run by nginx unit
RUN pip install --no-deps --target /app /app/dist/*.whl

# provide access to the application to the unit user
RUN chown -R unit:unit /app

# copy the config file to the /docker-entrypoint.d folder
# this is where nginx unit will look for the config file
RUN cp /app/intellireading/api_server/config/nginx.unit.config.json /docker-entrypoint.d/

# copy the run.sh file to the /app folder, make it executable and set it as the entrypoint
COPY ./docker/api_server/run.sh /app/run.sh
RUN chmod +x /app/run.sh
ENTRYPOINT ["/app/run.sh"]


##############
# Define build arguments
#ARG USER_UID=999
#ARG USER_GID=999

# Create a group and user with the specified UID and GID
##RUN groupadd -g ${USER_GID} mygroup \
##    && useradd -u ${USER_UID} -g ${USER_GID} -m myuser

# Create necessary directories and set permissions
#RUN mkdir -p /var/run \
#    && chown -R ${USER_UID}:${USER_GID} /var/run \
#    && mkdir -p /var/lib/unit/certs/ \
#    && chown -R ${USER_UID}:${USER_GID} /var/lib/unit

# Switch to the new user
#USER ${USER_UID}:${USER_GID}
