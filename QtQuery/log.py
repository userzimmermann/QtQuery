import logging

from moretools import cached


LEVELS = ['DEBUG', 'INFO', 'WARN', 'ERROR', 'FATAL']


class Handler(logging.Handler):
    def __init__(self, qlogger):
        logging.Handler.__init__(self)
        self.qlogger = qlogger

    def emit(self, record):
        self.qlogger.append(record.levelno, self.format(record))


@cached
def logger(Q):
    class Logger(Q.PlainTextEdit):
        def __init__(self):
            Q.PlainTextEdit.__init__(self, readOnly=True)
            self.logger = logging.Logger(self.id, logging.INFO)
            self.loghandler = Handler(qlogger=self)
            self.logger.addHandler(self.loghandler)
            self.log = self.logger.log
            for levelname in LEVELS:
                levelname = levelname.lower()
                setattr(self, levelname, getattr(self.logger, levelname))

        def append(self, level, msg):
            scrollbar = self.verticalScrollBar
            scroll = scrollbar.value == scrollbar.maximum
            self.appendPlainText(msg)
            if scroll:
                scrollbar.value = scrollbar.maximum

        def setLevel(self, level):
            self.logger.setLevel(level)

        def level(self):
            return self.logger.level

        def setFormatter(self, formatter):
            self.loghandler.setFormatter(formatter)

        def formatter(self):
            return self.loghandler.formatter

    return Logger
