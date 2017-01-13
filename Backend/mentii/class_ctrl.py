import boto3
import uuid
import utils.MentiiLogging as MentiiLogging
from boto3.dynamodb.conditions import Key, Attr
from utils.ResponseCreation import ControllerResponse
from utils import db_utils as dbUtils
from flask import g

def getActiveClassList(dynamoDBInstance, email=None):
  response = ControllerResponse()
  usersTable = dbUtils.getTable('users', dynamoDBInstance)

  if email is None:
    email = g.authenticatedUser['email']
  if usersTable is None:
    MentiiLogging.getLogger().error("Unable to get users table in getActiveClassList")
    return None
  classCodes = []
  classes = []
  #An active class list is the list of class codes that
  # a user has in the user table.
  request = {"Key" : {"email": email}, "AttributesToGet": ["classCodes"]}
  res = dbUtils.getItem(request, usersTable)
  #Get the class codes for the user.
  if res is not None and 'Item' in res:
    classCodes = res['Item']['classCodes']

  #Use the class codes to get the class details for
  # each class.
  classesTable = dbUtils.getTable('classes', dynamoDBInstance)
  if classesTable is None:
    MentiiLogging.getLogger().error("Unable to get classes table in getActiveClassList")
    return None
  for code in classCodes:
    request = {"Key": {"code": code}}
    res = dbUtils.getItem(request, classesTable)
    if res is not None and 'Item' in res:
      classes.append(res['Item'])

  response.addToPayload('classes', classes)
  return response

def checkClassData(classData):
  return 'code' in classData.keys() and 'title' in classData.keys() and 'subtitle' in classData.keys() and 'description' in classData.keys()

def createClass(dynamoDBInstance, classData):
  response = ControllerResponse()

  if classData is not None and checkClassData(classData):
    item = {'code': classData['code'],
            'title': classData['title'],
            'subtitle': classData['subtitle'],
            'description': classData['description']}
    table = dbUtils.getTable('classes', dynamoDBInstance)

    if table is not None:
      result = dbUtils.putItem(item, table)
      if result is not None:
        response.addToPayload('success', 'Successfully created class')
      else:
        error_message = "Unable to create class in classes table."
        response.addError("createClass call Failed.", error_message)
        MentiiLogging.getLogger().error(error_message)
    else:
      error_message = "Unable to locate classes table."
      response.addError("createClass call Failed.", error_message)
      MentiiLogging.getLogger().error(error_message)
  else:
    error_message = "Invalid class data given."
    response.addError("createClass call Failed.", error_message)
    MentiiLogging.getLogger().error(error_message)

  return response
