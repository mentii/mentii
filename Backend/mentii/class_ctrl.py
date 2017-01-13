import boto3
from boto3.dynamodb.conditions import Key, Attr
from utils.ResponseCreation import ControllerResponse
from utils import db_utils as dbUtils
import uuid
from flask import g
import utils.MentiiLogging as MentiiLogging

def getActiveClassList(dynamoDBInstance, email=None):
  response = ControllerResponse()
  if email is None:
    email = g.authenticatedUser['email']
  dynamodb = dynamoDBInstance
  table = dbUtils.getTable('users', dynamodb)
  if table is None:
    MentiiLogging.getLogger().error("Unable to get users table in getActiveClassList")
    return None
  classCodes = []
  classes = []
  #An active class list is the list of class codes that
  # a user has in the user table.
  request = {"Key" : {"email": email}, "AttributesToGet": ["classCodes"]}
  res = dbUtils.getItem(request, table)
  #Get the class codes for the user.
  if res is not None and 'Item' in res:
    classCodes = res['Item']['classCodes']

  #Use the class codes to get the class details for
  # each class.
  table = dbUtils.getTable('classes', dynamodb)
  if table is None:
    MentiiLogging.getLogger().error("Unable to get classes table in getActiveClassList")
    return None
  for code in classCodes:
    request = {"Key": {"code": code}}
    res = dbUtils.getItem(request, table)
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
      res = dbUtils.putItem(item, table)
      if res is not None:
        response.addToPayload('success', 'Successfully added classs')
      else:
        response.addError("Unable to add clsas", "unable to add class to the table")
        MentiiLogging.getLogger().error("Unable to add class! Could not add class in createClass")
    else:
      response.addError("Unable to access DB", "unable to access the db table classes")
      MentiiLogging.getLogger().error("Unable to access the DB! Could not access table classes in createClass")
  else:
    response.addError("Class data none or invalid.", "json passed class data is none or invalid")
    MentiiLogging.getLogger().error("Class data was invalid in createClass!")

  return response
    

    

