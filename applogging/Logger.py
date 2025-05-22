import logging
import socket
import getpass
from datetime import datetime

class Logger:
    _logger = None

    @classmethod
    def _init_logger(cls):
        if cls._logger is None:
            LOG_FORMAT = "%(levelname)s %(asctime)s [%(hostname)s:%(username)s] - %(message)s"
            logging.basicConfig(
                filename="c:\\bevolkingsregister\\logbestand.log",
                level=logging.DEBUG,
                format=LOG_FORMAT
            )
            cls._logger = logging.getLogger()
            cls._logger = logging.LoggerAdapter(cls._logger, {
                'hostname': socket.gethostname(),
                'username': getpass.getuser()
            })

    @classmethod
    def _log(cls, level, message):
        cls._init_logger()
        log_method = getattr(cls._logger, level)
        log_method(message)

    @classmethod
    def debug(cls, message): cls._log('debug', message)
    @classmethod
    def info(cls, message): cls._log('info', message)
    @classmethod
    def warning(cls, message): cls._log('warning', message)
    @classmethod
    def error(cls, message): cls._log('error', message)
    @classmethod
    def critical(cls, message): cls._log('critical', message)
