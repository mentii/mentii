import os
import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime

FILE = '/mentiilog.log'

def setupLogger(path):
  path += FILE
  prepareLogfile(path)

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
  logger.info("Logfile Created.")

def getLogger():
  return logging.getLogger('Backend')

def prepareLogfile(path):
  if not os.path.exists(os.path.dirname(path)):
    os.makedirs(os.path.dirname(path))
  elif os.path.isfile(path):
    # Rename old logfile
    modifiedTime = os.path.getmtime(path) 
    timeStamp =  datetime.fromtimestamp(modifiedTime).strftime("%b-%d-%y-%H:%M:%S")
    os.rename(path,path+".old."+timeStamp)
