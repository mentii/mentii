import os
import time
import logging
from logging.handlers import TimedRotatingFileHandler

PATH = '../logs/metniilog.log'

def setupLogger():
  confirmLogDir()

  logger = logging.getLogger('Backend')
  logger.setLevel(logging.DEBUG)

  handler = TimedRotatingFileHandler(PATH,
    when='midnight',
    interval=1,
    backupCount=0,
    encoding=None,
    delay=False,
    utc=False)
  formatter = logging.Formatter('[%(levelname)-8s][%(name)-8s][%(asctime)s] : %(message)s')
  handler.setFormatter(formatter)
  logger.addHandler(handler)

  return logger

def confirmLogDir():
  if not os.path.exists(os.path.dirname(PATH)):
    os.makedirs(os.path.dirname(PATH))
