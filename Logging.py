import logging
from logging import Formatter
import sys

from TermColors import AnsiColor


class AnsiColorFormatter(Formatter):
    def __init__(self, fmt=None, datefmt=None, style='%'):
        super().__init__(fmt, datefmt, style)

    def format(self, record):
        base_formatted = super().format(record)
        return AnsiColor.colorize(base_formatted)


def setup_logging():
    from settings import DEBUG

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG if DEBUG else logging.INFO)


def get_main_logger():
    from settings import DEBUG, LOG_FORMAT

    main_logger = logging.getLogger("MainLogger")
    main_logger.setLevel(logging.DEBUG if DEBUG else logging.INFO)

    if main_logger.hasHandlers():
        return main_logger

    log_formatter = AnsiColorFormatter(LOG_FORMAT)

    stdout_stream_handler = logging.StreamHandler(sys.stdout)
    stdout_stream_handler.setLevel(logging.DEBUG if DEBUG else logging.INFO)
    stdout_stream_handler.setFormatter(log_formatter)

    main_logger.addHandler(stdout_stream_handler)

    return main_logger


def create_policy_logger(policy_name):
    from settings import DEBUG, POLICY_LOG_FORMAT

    log_formatter = AnsiColorFormatter(POLICY_LOG_FORMAT.format(policy_name.upper()))

    stdout_stream_handler = logging.StreamHandler(sys.stdout)
    stdout_stream_handler.setLevel(logging.DEBUG if DEBUG else logging.INFO)
    stdout_stream_handler.setFormatter(log_formatter)

    policy_logger = logging.getLogger(policy_name)
    policy_logger.setLevel(logging.DEBUG if DEBUG else logging.INFO)
    policy_logger.addHandler(stdout_stream_handler)

    return policy_logger
