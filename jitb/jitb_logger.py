"""Standardize logging on behalf of the package.

Using the --debug command line argument will duplicate any log output, and add debug messages,
to /tmp/jitb_YYYYMMDD_HHMMSS.log.

clear; tail -f `ls /tmp/jitb_* | tail -n 1`
"""
# Standard
from datetime import datetime
from enum import IntEnum
import logging
import os
import sys
# Third Party
# Local


# pylint: disable=too-few-public-methods, no-self-argument
class LogLevel(IntEnum):
    """Defines logging levels."""
    DEBUG = logging.DEBUG     # Debug messages
    ERROR = logging.ERROR     # Error messages
    INFO = logging.INFO       # Standard messages
    JITB = logging.DEBUG + 5  # JITB DEBUG logging


class DebugHandler(logging.Filter):
    """Filters what can be logger by a specific logger."""
    def filter(self, record):
        return record.levelno in (logging.DEBUG,)


class ErrorHandler(logging.Filter):
    """Filters what can be logger by a specific logger."""
    def filter(self, record):
        return record.levelno in (logging.ERROR,)


class InfoHandler(logging.Filter):
    """Filters what can be logger by a specific logger."""
    def filter(self, record):
        return record.levelno in (logging.INFO,)


class JitbHandler(logging.Filter):
    """Filters what can be logger by a specific logger."""
    def filter(self, record):
        return record.levelno in (LogLevel.JITB,)


class Logger():
    """Logging class for the package."""

    _initialized = False  # Logging subsystem status
    _filename = ''        # Absolute debug log filename

    def __del__(self) -> None:
        """Class dtor."""
        Logger.shutdown()

    @staticmethod
    def initialize(debugging: bool = False) -> None:
        """Initializes the logging subsystem.

        Args:
            debug: [Optional] If True, sets the logging level to DEBUG and logs to
                /tmp/jitb_YYYYMMDD_HHMMSS.log.

        Function is optional as the logging class auto-initializes if called without initialization
        """
        # LOCAL VARIABLES
        debug = None                       # JITB Debug stream handler
        error = None                       # Error stream handler
        normal = None                      # Info stream handler
        root_logger = logging.getLogger()  # Root logger
        # Message formatter
        formatter = logging.Formatter(fmt='[%(asctime)s.%(msecs)03d] %(levelname)-9s - %(message)s',
                                      datefmt='%Y-%m-%d %H:%M:%S')

        # SETUP
        logging.addLevelName(LogLevel.JITB, 'DEBUGGING')
        Logger._filename = _create_filename()

        if debugging:
            normal = logging.FileHandler(Logger._filename)
            normal.addFilter(InfoHandler())
            normal.setFormatter(formatter)
            normal.setLevel(logging.INFO)

            # Separate and distinct from Logger.DEBUG because good, bad, or indifferent...
            # Selenium uses DEBUG for very verbose logging
            debug = logging.FileHandler(Logger._filename)
            debug.addFilter(JitbHandler())
            debug.setFormatter(formatter)
            debug.setLevel(LogLevel.JITB)

            error = logging.FileHandler(Logger._filename)
            error.addFilter(ErrorHandler())
            error.setFormatter(formatter)
            error.setLevel(logging.ERROR)

            root_logger.addHandler(normal)
            root_logger.addHandler(debug)
            root_logger.addHandler(error)
            root_logger.setLevel(LogLevel.JITB)
        else:
            root_logger.setLevel(logging.INFO)

        # DONE
        Logger._initialized = True

    def debug(message: str, logger: str = __name__) -> None:
        """Log debug level messages.

        Args:
            message: Message to log
            logger: Logger name if needed.
        """
        Logger._check_logger()
        Logger.log(level=LogLevel.JITB, message=message, logger=logger)

    def error(message: str, logger: str = __name__) -> None:
        """Log error level messages.

        Args:
            message: Message to log
            logger: Logger name if needed.
        """
        print(message, file=sys.stderr)
        Logger._check_logger()
        logging.getLogger(logger).error(message)

    def info(message: str, logger: str = __name__) -> None:
        """Log info level messages.

        Args:
            message: Message to log
            logger: Logger name if needed.
        """
        print(message, file=sys.stdout)
        Logger._check_logger()
        logging.getLogger(logger).info(message)

    def log(level: LogLevel, message: str = '', logger: str = __name__) -> None:
        """Log on behalf of the project.

        Args:
            level: Priority level of message
            message: Message to log
            logger: Logger name if needed.
        """
        logging.getLogger(logger).log(level, message)

    @staticmethod
    def shutdown() -> None:
        """Call logging.shutdown()."""
        logging.shutdown()

    # pylint: disable=no-method-argument
    def _check_logger() -> None:
        """Verify the logger was initialized."""
        if Logger._initialized is False:
            raise RuntimeError('Call Logger.initialize() first!')


def _create_filename() -> str:
    """Determine filename to use for logging."""
    # LOCAL VARAIBLES
    abs_log_filename = ''  # Absolute filename of the log to use
    now = datetime.now()   # Current date and time
    number = 0             # Number of times the generated filename has been detected

    # CREATE IT
    while True:
        abs_log_filename = os.path.join('/tmp',
                                        f'jitb_{now.strftime("%Y%m%d_%H%M%S")}-{str(number)}.log')
        if os.path.isfile(abs_log_filename):
            number += 1
        else:
            break

    # DONE
    return abs_log_filename
