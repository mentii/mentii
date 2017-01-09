import os
import time
import logging
from logging.handlers import TimedRotatingFileHandler

FILE = '/metniilog.log'

def setupLogger(path):
  path += FILE
  confirmLogDir(path)

  logger = logging.getLogger('Backend')
  logger.setLevel(logging.DEBUG)

  handler = TimedRotatingFileHandler(
    path,
    when='midnight',
    interval=1,
    backupCount=0,
    encoding=None,
    delay=False,
    utc=False)
  formatter = logging.Formatter('[%(levelname)-8s][%(name)-8s][%(asctime)s] : %(message)s')
  handler.setFormatter(formatter)
  logger.addHandler(handler)

def getLogger():
  return logging.getLogger('Backend')

def confirmLogDir(path):
  if not os.path.exists(os.path.dirname(path)):
    os.makedirs(os.path.dirname(path))
