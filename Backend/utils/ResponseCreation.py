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
    value = self.prepForJsonification(value)
    self.payload[attribute] = value

  def prepForJsonification(self, item):
    isDict = None
    isList = None
    if isinstance(item, dict):
      isDict = True
    elif isinstance(item, set):
      #set to list
      item = list(item)
      isList = True
    elif isinstance(item, list):
      isList = True
    #lists or dicts can be jsonified, contents are handled recursively
    if isDict or isList :
      #iterator though dict or list
      iterator = item if isDict else xrange(len(item))
      for i in iterator:
        #recursive call
        item[i] = self.prepForJsonification(item[i])
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
