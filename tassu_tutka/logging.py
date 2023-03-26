import tassu_tutka.error as error
import logging
from logging import basicConfig
import argparse


def setup_logging(options: "argparse.Namespace"):
    f = options.log_file
    print(options.log_level)
    match options.log_level:
        case "debug":
            debug_level = logging.DEBUG
        case "info":
            debug_level = logging.INFO
        case "warning":
            debug_level = logging.WARNING
        case "error":
            debug_level = logging.ERROR
        case "critical":
            debug_level = logging.CRITICAL
        case _:
            raise error.ServerError("Invalid log level")
    basicConfig(format="{levelname:7} {message}", style="{", level=debug_level)
