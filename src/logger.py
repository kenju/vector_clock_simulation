from enum import IntEnum


class LogLevel(IntEnum):
    TRACE = 1
    DEBUG = 2
    INFO = 3
    WARN = 4
    ERROR = 5


class Logger():
    def __init__(self, level: LogLevel):
        self._level = level
        self._logfile = None

    def set_logfile(self, logfile: str):
        self._logfile = logfile
        # clear file contents
        open(self._logfile, 'w', encoding="utf-8").close()

    def debug(self, message):
        if self._level <= LogLevel.DEBUG:
            print(message)
            if self._logfile:
                with open(self._logfile, "a", encoding="utf-8") as logfile:
                    logfile.write(f'{message}\n')
