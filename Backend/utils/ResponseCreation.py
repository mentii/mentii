import json
from flask import Response, g
import utils.MentiiLogging as MentiiLogging


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
    self.user = g.get('authenticatedUser', {})

  # def addUser(self):
  #   self.user = g.authenticatedUser

  def addError(self, title, message):
    MentiiLogging.getLogger().error('%s : %s', title, message)
    tmpErrorDict = {"title" : title, "message" : message}
    self.errors.append(tmpErrorDict)
    self.hasError = True

  def addToPayload(self, attribute, value):
    self.payload[attribute] = value

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
