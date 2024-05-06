import sys

from loguru import logger as _logger

from taitriscore.const import PROJECT_ROOT


def define_log_level(print_level="INFO", logfile_level="DEBUG"):
    _logger.remove()
    simple_format = "{message}"
    _logger.add(sys.stderr, level=print_level, format=simple_format)
    _logger.add(
        PROJECT_ROOT / "logs/log.txt", level=logfile_level, format=simple_format
    )
    return _logger


logger = define_log_level()
