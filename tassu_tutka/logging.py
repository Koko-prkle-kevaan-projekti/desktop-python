import tassu_tutka.error as error
import logging
from logging import config


def setup_logging(options: "tassu_tutka.argparse.Namespace"):
    f = options.log_file
    match options.log_level:
        case "debug":
            dbg = logging.DEBUG
        case "info":
            dbg = logging.INFO
        case "warning":
            dbg = logging.WARNING
        case "error":
            dbg = logging.ERROR
        case "critical":
            dbg = logging.CRITICAL
        case _:
            raise error.ServerError("Invalid log level")
