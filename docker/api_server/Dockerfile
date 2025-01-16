FROM python:3-slim AS builder

RUN mkdir /app
WORKDIR /app

RUN pip install --no-cache --upgrade pip
RUN pip install --no-cache hatch

# COPY the project files to the container and build the .whl files
COPY . /app
RUN hatch build



FROM python:3-slim

RUN mkdir /app
WORKDIR /app

RUN pip install --no-cache --upgrade pip 


# copy and install any dependencies that are required by the application and were provided as whl files
# this may include dependencies that are not available in the public pypi repository (if any)
COPY  ./.dependencies /app/.dependencies
RUN pip install --no-cache-dir /app/.dependencies/*.whl



# copy and install the application itself (this requires that the application is packaged as a whl file)
# ensure that the application is packaged as a whl file and is present in the /app/dist folder
# Packaging can be done by running hatch build in the root of the application
COPY --from=builder /app/dist /app/dist
RUN pip install --no-cache-dir /app/dist/*.whl

#-------
# IF the config file needs to be changed at runtime, uncomment the following lines

# extract the whl files to /app
# this is done so source and config files are available in the container
#RUN pip install --no-deps --target /app /app/dist/*.whl
# Configuration file path used when booting
#ENV CONFIG_FILE=/app/intellireading/api_server/config/api_server.config.json
#-------

RUN addgroup --system app && adduser --system --group app 


# set the environment variables
# API key for request validation
ENV API_SERVER_API_KEY="devapikey"

# Turnstile configuration
ENV TURNSTILE_ENABLED=false
ENV TURNSTILE_SECRET_KEY=<turnstile-secret-key>


USER app
CMD ["api-server"]
