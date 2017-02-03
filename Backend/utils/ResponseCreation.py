import json
from flask import Response, g
import utils.MentiiLogging as MentiiLogging
from numbers import Number


class ControllerResponse:
  '''
  An object to handle managment of
  the JSON response that we want REST calls
  to return.
  '''
  def __init__(self):
    self.errors = []
    self.payload = {}
    self.hasError = False
    self.user = {}
    if g:
      self.user = g.get('authenticatedUser', {})

  def addError(self, title, message):
    MentiiLogging.getLogger().error('%s : %s', title, message)
    tmpErrorDict = {"title" : title, "message" : message}
    self.errors.append(tmpErrorDict)
    self.hasError = True

  def addToPayload(self, attribute, value):
    value = self.setsToLists(value)
    print '####################################################################'
    print value
    self.payload[attribute] = value

  def setsToLists(self, item):
    #if not valid json type except for Array which is handled recursively
    if (not None and
        not isinstance(item, basestring) and
        not isinstance(item, Number) and
        not isinstance(item, bool)) :
      #sets to lists
      if isinstance(item, set) :
        item = list(item)
      #iterate though list or dict
      iterator = item if isinstance(item, dict) else xrange(len(item))
      for i in iterator:
        #recursive call
        item[i] = self.setsToLists(item[i])
    return item

  def hasErrors(self):
    return self.hasError

  def getResponseString(self):
    responseDict = {'user': self.user, 'payload': self.payload, 'errors': self.errors}
    return json.dumps(responseDict)

def createResponse(controllerResponse, statusCode):
  '''
  Create the Flask response object
  '''
  responseString = controllerResponse.getResponseString()
  response = Response(response=responseString, status=statusCode, mimetype='application/json')
  return response

def createEmptyResponse(statusCode):
  '''
  Create the Flask response object
  '''
  responseString = ""
  response = Response(response=responseString, status=statusCode, mimetype='application/json')
  return response
