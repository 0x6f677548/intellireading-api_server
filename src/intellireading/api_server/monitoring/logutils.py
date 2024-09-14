import logging
import logging.config
from intellireading.api_server.utils.configuration import ConfigDict


def init_default_logging():
    """Configures logging to the console."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s.%(msecs)03d %(name)-20s %(levelname)-8s %(message)s",
        datefmt="%Y-%m-%d,%H:%M:%S",
    )


def init_logging_from_file(filename: str = "logging.conf"):
    """Configures logging from a configuration file. If the file does not exist,
    it configures logging to the console.
    filename: the name of the configuration file
    """

    # check if the config file exists
    import os

    if not os.path.exists(filename):
        init_default_logging()
    else:
        # read the logging configuration from the config file
        logging.config.fileConfig(filename)


def init_logging_from_json_file(
    filename: str = "config.json", section: str = "logging"
):
    """Configures logging from a configuration file. If the file does not exist,
    it configures logging to the console.
    filename: the name of the configuration file
    """

    # check if the config file exists
    import os

    if not os.path.exists(filename):
        init_default_logging()
    else:

        # read the logging configuration from the config file
        # using the ConfigDict class to replace environment variables
        _config = ConfigDict.from_json_file(filename)
        init_logging_from_config(_config, section)


def init_logging_from_config(config: dict, section: str = "logging"):
    """Initializes logging from a configuration dictionary.
    config: a dictionary containing the logging configuration.
    """

    if config is None or section not in config:
        init_default_logging()
    else:
        _logging_settings = config[section]
        logging.config.dictConfig(_logging_settings)


def log_memory_usage(logger: logging.Logger, level: int = logging.DEBUG):
    from os import sysconf
    import resource

    logger.log(
        level,
        "Memory usage (RUSAGE_SELF): %s",
        resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
    )
    logger.log(
        level,
        "Memory usage (RUSAGE_CHILDREN): %s",
        resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
    )
    logger.log(
        level,
        "Memory usage (RUSAGE_THREAD): %s",
        resource.getrusage(resource.RUSAGE_THREAD).ru_maxrss,
    )
    logger.log(
        level,
        "Free memory: %sGB",
        sysconf("SC_PAGE_SIZE") * sysconf("SC_AVPHYS_PAGES") / (1024.0**3),
    )
