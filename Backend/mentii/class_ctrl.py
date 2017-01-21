import boto3
import uuid
from boto3.dynamodb.conditions import Key, Attr
from utils.ResponseCreation import ControllerResponse
from utils import db_utils as dbUtils
from flask import g

def getActiveClassList(dynamoDBInstance, email=None):
  response = ControllerResponse()
  usersTable = dbUtils.getTable('users', dynamoDBInstance)
  classTable = dbUtils.getTable('classes', dynamoDBInstance)

  if usersTable is None or classTable is None:
    response.addError(  "Get Active Class List Failed",
                        "Unable to access users and/or classes")
  else :
    if email is None:
      email = g.authenticatedUser['email']
    classes = []
    classCodes = getClassCodesFromUser(dynamoDBInstance, email)
    #Use the class codes to get the class details for
    # each class.
    table = dbUtils.getTable('classes', dynamoDBInstance)
    if table is None:
      MentiiLogging.getLogger().error("Unable to get classes table in getActiveClassList")
      response.addError("Failed to get class list", "A database error occured");
    else:
      for code in classCodes:
        request = {"Key": {"code": code}}
        res = dbUtils.getItem(request, classTable)
        if res is not None and 'Item' in res:
          classes.append(res['Item'])
      response.addToPayload('classes', classes)
  return response

def checkClassDataValid(classData):
  return 'title' in classData.keys() and 'description' in classData.keys()

def createClass(dynamoDBInstance, classData, email=None, role=None):
  response = ControllerResponse()

  email = g.authenticatedUser['email']
  role = g.authenticatedUser['role']
  #Why are we doing this check a second time?
  if role == "S":
    response.addError("Role error", "Students cannot create classes")
  elif classData is None or not checkClassDataValid(classData):
    response.addError("createClass call Failed.", "Invalid class data given.")
  else:
    classTable = dbUtils.getTable('classes', dynamoDBInstance)
    userTable = dbUtils.getTable('users', dynamoDBInstance)
    if classTable is None or userTable is None:
      response.addError("createClass call Failed.",
                        "Unable to locate necessary table(s).")
    else:
      classCode = str(uuid.uuid4())
      newClass = {'code': classCode,
              'title': classData['title'],
              'description': classData['description']}

      if 'subtitle' in classData.keys() and classData['subtitle']:
        newClass['subtitle'] = classData['subtitle']
      if 'section' in classData.keys() and classData['section']:
        newClass['section'] = classData['section']

      result = dbUtils.putItem(newClass, classTable)

      if result is None:
        response.addError(  "createClass call Failed.",
                            "Unable to create class in classes table.")
      else:
        jsonData = {
          "Key": {"email": email},
          "UpdateExpression": "SET teaching = list_append(teaching, :i)",
          "ExpressionAttributeValues": { ":i": [classCode] },
          "ReturnValues" : "UPDATED_NEW"
        }
        res = dbUtils.updateItem(jsonData, userTable)
        #TODO: handle bad update?
        response.addToPayload('Success', 'Class Created')
  return response

def getClassCodesFromUser(dynamoDBInstance, email=None):
  classCodes = []
  if email is None:
    email = g.authenticatedUser['email']
  usersTable = dbUtils.getTable('users', dynamoDBInstance)
  if usersTable is None:
    MentiiLogging.getLogger().error("Unable to get users table in getClassCodesFromUser")
  else:
    #An active class list is the list of class codes that
    # a user has in the user table.
    request = {"Key" : {"email": email}, "AttributesToGet": ["classCodes"]}
    res = dbUtils.getItem(request, usersTable)
    #Get the class codes for the user.
    if res is not None and 'Item' in res:
      classCodes = res['Item']['classCodes']
  return classCodes

def getPublicClassList(dynamodb, email=None):
  response = ControllerResponse()
  classCodes = getClassCodesFromUser(dynamodb, email)
  classes = []
  classesTable = dbUtils.getTable('classes', dynamodb)
  if classesTable is None:
    MentiiLogging.getLogger().error("Unable to get classes table in getPublicClassList")
    response.addError("Failed to get class list", "A database error occured");
  else:
    res = classesTable.scan()
    for pclass in res.get('Items', []):
      if pclass['code'] not in classCodes and 'private' not in pclass and pclass.get('private') != True:
        classes.append(pclass)
    response.addToPayload('classes', classes)
  return response
