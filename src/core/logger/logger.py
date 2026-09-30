import logging
import sys


class Logger:
    def __init__(self):
        self.logger = logging.getLogger("sicna")

        if not self.logger.handlers:
            handler = logging.StreamHandler(sys.stdout)

            formatter = logging.Formatter(
                fmt="%(asctime)s | %(levelname)s | %(message)s",
                datefmt="%H:%M:%S",
            )

            handler.setFormatter(formatter)

            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)

    def info(self, msg: str, *args):
        self.logger.info(msg, *args)

    def error(self, msg: str, *args, exc_info=None):
        self.logger.error(
            msg,
            *args,
            exc_info=exc_info,
        )

    def fatal(self, msg: str, *args):
        self.logger.critical(msg, *args)


logger = Logger()