'''
Contains boiler plate for simple logging
Suitable when using multiple modules

how to use 
import Logger
creating an instance of Logger using default values will make a file logger with the level name and default format
more file, stream/console handlers can be added with different levels and foramts

severity of levels:
debug < info < warning < error < critical

*when set to lower level it can log higher levels but

eg -    from xlogger import Logger
        xlogger = Logger(__name__, 'debug')
        logger = xlogger.log
        logger.debug('Message')
'''
import logging

levels = {
    'debug': logging.DEBUG,
    'error': logging.ERROR,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'critical': logging.CRITICAL 
}

class Logger:
    log = None 
    defaultFormat = '%(asctime)s:%(name)s:%(levelname)s:%(message)s'

    def __init__(self, name, level, filelevel = None, filename = None, format = defaultFormat):
        self.log = logging.getLogger(name)
        self.log.setLevel(levels[level])
        if not filelevel:
            filelevel = level
        self.makeFileHandler(filelevel, filename, format)
        if level == 'debug':
            self.makeStreamHandler()

    def makeFileHandler(self, filelevel, filename = None, format = defaultFormat):
        if not filename:
            filename = filelevel + '.log'
        file_handler = logging.FileHandler(filename)
        file_handler.setLevel(levels[filelevel])
        formatter = logging.Formatter(format)
        file_handler.setFormatter(formatter)
        self.log.addHandler(file_handler)

    def makeStreamHandler(self, streamlevel = logging.DEBUG, format = defaultFormat):
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(streamlevel)
        formatter = logging.Formatter(format)
        stream_handler.setFormatter(formatter)
        self.log.addHandler(stream_handler)

#testing
# L = Logger(__name__, 'debug').log
# L.debug("Testing multi logger same file")