import functools
from flask import request
import ResponseCreation as ResponseCreation

def handleOptionsRequest(endpoint):
  @functools.wraps(endpoint)
  def optionsDecorator(*args, **kws):
    if request.method =='OPTIONS':
      return ResponseCreation.createEmptyResponse(statusCode=200)
    else:
      return endpoint(*args, **kws)
  return optionsDecorator
