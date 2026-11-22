import logging
import sys


class SafeFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        message = record.getMessage()
        record.msg = message.replace("\r", "\\r").replace("\n", "\\n")
        record.args = None
        return super().format(record)


class Logger:
    def __init__(self):
        self.logger = logging.getLogger("sicna")

        if not self.logger.handlers:
            handler = logging.StreamHandler(sys.stdout)

            formatter = SafeFormatter(
                fmt="%(asctime)s | %(levelname)s | %(message)s",
                datefmt="%H:%M:%S",
            )

            handler.setFormatter(formatter)

            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)
            self.logger.propagate = False

    def info(self, msg: str, *args):
        self.logger.info(msg, *args)

    def warning(self, msg: str, *args):
        self.logger.warning(msg, *args)

    def error(self, msg: str, *args, exc_info=None):
        self.logger.error(
            msg,
            *args,
            exc_info=exc_info,
        )

    def fatal(self, msg: str, *args):
        self.logger.critical(msg, *args)


logger = Logger()