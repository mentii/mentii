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
    response.addError(  'Get Active Class List Failed',
                        'Unable to access users and/or classes')
  else :
    if email is None:
      email = g.authenticatedUser['email']
    classes = []
    classCodes = getClassCodesFromUser(dynamoDBInstance, email)

    for code in classCodes:
      request = {'Key': {'code': code}}
      res = dbUtils.getItem(request, classTable)
      if res is not None and 'Item' in res:
        classes.append(res['Item'])
    response.addToPayload('classes', classes)
  return response

def checkClassDataValid(classData):
  return 'title' in classData.keys() and 'description' in classData.keys()

def createClass(dynamoDBInstance, classData, email=None, userRole=None):
  response = ControllerResponse()

  #g will be not be avliable durring testing,
  #and email and userRole will need to be passed to the function
  if g:
    email = g.authenticatedUser['email']
    userRole = g.authenticatedUser['userRole']
  #role is confirmed here incase createClass is called from somewhere other
  #than app.py create_class()
  if userRole != 'teacher' and userRole != 'admin':
    response.addError('Role error', 'Only teachers can create classes')
  elif classData is None or not checkClassDataValid(classData):
    response.addError('createClass call Failed.', 'Invalid class data given.')
  else:
    classTable = dbUtils.getTable('classes', dynamoDBInstance)
    userTable = dbUtils.getTable('users', dynamoDBInstance)
    if classTable is None or userTable is None:
      response.addError('createClass call Failed.', 'Unable to locate necessary table(s).')
    else:
      classCode = str(uuid.uuid4())
      newClass = {
        'code': classCode,
        'title': classData['title'],
        'description': classData['description']
      }

      if 'department' in classData.keys() and classData['department']:
        newClass['department'] = classData['department']
      if 'section' in classData.keys() and classData['section']:
        newClass['section'] = classData['section']

      result = dbUtils.putItem(newClass, classTable)

      if result is None:
        response.addError('createClass call Failed.', 'Unable to create class in classes table.')
      else:
        # Note: if teaching attribute does not previously exist, a set of class codes will be created
        # otherwise, the class code will be added to the set of class codes
        codeSet = set([classCode])
        jsonData = {
          'Key': {'email': email},
          'UpdateExpression': 'ADD teaching :classCode',
          'ExpressionAttributeValues': { ':classCode': codeSet },
          'ReturnValues' : 'UPDATED_NEW'
        }
        res = dbUtils.updateItem(jsonData, userTable)
        if res is None:
          response.addError('createClass call failed', 'Unable to update user data')
        else:
          response.addToPayload('Success', 'Class Created')
  return response

def getClassCodesFromUser(dynamoDBInstance, email=None):
  classCodes = []
  if email is None:
    email = g.authenticatedUser['email']
  usersTable = dbUtils.getTable('users', dynamoDBInstance)
  if usersTable is None:
    MentiiLogging.getLogger().error('Unable to get users table in getClassCodesFromUser')
  else:
    #An active class list is the list of class codes that
    # a user has in the user table.
    request = {"Key" : {"email": email}, "ProjectionExpression": "classCodes"}
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
    MentiiLogging.getLogger().error('Unable to get classes table in getPublicClassList')
    response.addError('Failed to get class list', 'A database error occured');
  else:
    res = classesTable.scan()
    for pclass in res.get('Items', []):
      if pclass['code'] not in classCodes and 'private' not in pclass and pclass.get('private') != True:
        classes.append(pclass)
    response.addToPayload('classes', classes)
  return response
