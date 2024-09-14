import logging
from fastapi.middleware.cors import CORSMiddleware as fastapi_CORSMiddleware


class CORSMiddleware(fastapi_CORSMiddleware):
    _logger = logging.getLogger(__name__)
    middleware_config = None
    middleware_enabled = True

    allow_origins: list[str] = []
    allow_origins_regex = None
    allow_methods: list[str] = []
    allow_headers: list[str] = []
    allow_credentials = False
    max_age = 600
    expose_headers: list[str] = []

    def set_fields(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __init__(self, app, config: dict):
        self.middleware_name = self.__class__.__name__

        if config is None:
            config = {}

        _middleware_section_configuration = config.get("middleware", {})
        self.middleware_config = _middleware_section_configuration.get(
            self.middleware_name, {}
        )

        if self.middleware_config:
            self._logger.info(
                "Enabling %s middleware with the following configuration: %s",
                self.middleware_name,
                self.middleware_config,
            )
        else:
            self._logger.info(
                "Enabling %s middleware with default configuration",
                self.middleware_name,
            )

        self.set_fields(**self.middleware_config.get("kwargs", {}))
        super().__init__(
            app,
            allow_origins=self.allow_origins,
            allow_methods=self.allow_methods,
            allow_headers=self.allow_headers,
            allow_credentials=self.allow_credentials,
            allow_origin_regex=self.allow_origins_regex,
            max_age=self.max_age,
            expose_headers=self.expose_headers,
        )
