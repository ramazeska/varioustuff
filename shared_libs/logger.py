import logging
import sys


class SharedLogger:
    def __init__(self, name=None):
        stdouthandler = logging.StreamHandler(sys.stdout)
        basicFormatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s -%(message)s')
        stdouthandler.setFormatter(basicFormatter)
        self.log = logging.getLogger(self.__class__.__name__)
        if name is not None:
            self.log = logging.getLogger(name)
        self.log.setLevel(logging.DEBUG)
        if not self.log.handlers:
            self.log.addHandler(stdouthandler)

    def log_info(self, message):
        return self.log.info(message)

    def log_warning(self, message):
        return self.log.warning(message)

    def log_error(self, message):
        return self.log.error(message)

    def log_critical(self, message):
        return self.log.critical(message)
