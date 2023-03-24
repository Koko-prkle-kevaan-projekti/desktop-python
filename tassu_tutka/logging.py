import argparse
import logging
import logging.config as config


def setup_logging(options: argparse.Namespace):
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
            raise Server
