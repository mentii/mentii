import boto3
import re
from flask import render_template
from flask_mail import Message
from boto3.dynamodb.conditions import Key, Attr
from utils.ResponseCreation import ControllerResponse
from utils import db_utils as dbUtils
import utils.MentiiLogging as MentiiLogging
import uuid
import hashlib
import class_ctrl as class_ctrl
from flask import g

def sendForgotPasswordEmail(httpOrigin, jsonData, mailer, dbInstance):
  email = jsonData.get('email', None)
  resetPasswordId = str(uuid.uuid4())
  success = addResetPasswordIdToUser(email, resetPasswordId, dbInstance)
  if success == True:
    host = getProperEnvironment(httpOrigin)
    url = host + '/reset-password/{0}'.format(resetPasswordId)
    message = render_template('forgotPasswordEmail.html', url=url)
    #Build Message
    msg = Message('Mentii: Reset Password', recipients=[email], extra_headers={'Content-Transfer-Encoding': 'quoted-printable'}, html=message)
    #Send Email
    mailer.send(msg)

def addResetPasswordIdToUser(email, resetPasswordId, dbInstance):
  success = False;
  table = dbUtils.getTable('users', dbInstance)
  if table is not None:
    user = getUserByEmail(email,dbInstance)
    if user is not None:
      jsonData = {
        'Key': {'email': email},
        'UpdateExpression': 'SET resetPasswordId = :a',
        'ExpressionAttributeValues': { ':a': resetPasswordId },
        'ReturnValues' : 'UPDATED_NEW'
      }
      dbUtils.updateItem(jsonData, table)
      success = True
  return success

def resetUserPassword(jsonData, dbInstance):
  response = ControllerResponse()
  email = jsonData.get('email', None)
  password = jsonData.get('password', None)
  resetPasswordId = jsonData.get('id', None)
  if email is not None and password is not None and resetPasswordId is not None:
    res = updatePasswordForEmailAndResetId(email, password, resetPasswordId, dbInstance)
    if res is not None:
      response.addToPayload('status', 'Success')
    else:
      response.addError('Failed to Reset Password', 'We were unable to update the password for this account.')
  else:
    response.addError('Failed to Reset Password', 'We were unable to update the password for this account.')
  return response

def updatePasswordForEmailAndResetId(email, password, resetPasswordId, dbInstance):
  res = None
  user = getUserByEmail(email, dbInstance)
  if user is not None:
    storedResetPasswordId = user.get('resetPasswordId', None)
    if storedResetPasswordId == resetPasswordId:
      table = dbUtils.getTable('users', dbInstance)
      if table is not None:
        hashedPassword = hashPassword(password)
        jsonData = {
          'Key': {'email': email},
          'UpdateExpression': 'SET password = :a REMOVE resetPasswordId',
          'ExpressionAttributeValues': { ':a': hashedPassword },
          'ReturnValues' : 'UPDATED_NEW'
        }
        res = dbUtils.updateItem(jsonData, table)
  return res

def getProperEnvironment(httpOrigin):
  host = ''
  if httpOrigin.find('stapp') != -1:
    host = 'http://stapp.mentii.me'
  elif httpOrigin.find('app') != -1:
    host = 'http://app.mentii.me'
  else:
    host = 'http://localhost:3000'
  return host

def register(httpOrigin, jsonData, mailer, dbInstance):
  response = ControllerResponse()
  if not validateRegistrationJSON(jsonData):
    response.addError('Register Validation Error', 'The json data did not have an email or did not have a password')
  else:
    email = parseEmail(jsonData)
    password = parsePassword(jsonData)

    if not isEmailValid(email):
      response.addError('Email invalid', 'The email is invalid')

    if not isPasswordValid(password):
      response.addError('Password Invalid', 'The password is invalid')

    if isEmailInSystem(email, dbInstance) and isUserActive(getUserByEmail(email, dbInstance)):
      response.addError('Registration Failed', 'We were unable to register this user')

    if not response.hasErrors():
      hashedPassword = hashPassword(parsePassword(jsonData))
      activationId = addUserAndSendEmail(httpOrigin, email, hashedPassword, mailer, dbInstance)
      if activationId is None:
        response.addError('Activation Id is None', 'Could not create an activation Id')

  return response

def hashPassword(password):
  return hashlib.md5( password ).hexdigest()

def validateRegistrationJSON(jsonData):
  '''
  Validate that the JSON object contains
  an email and password attributes
  '''
  if jsonData is not None:
    return 'password' in jsonData.keys() and 'email' in jsonData.keys()
  return False

def parseEmail(jsonData):
  try:
    email = jsonData['email']
    return email
  except Exception as e:
    MentiiLogging.getLogger().exception(e)
    return None

def parsePassword(jsonData):
  try:
    password = jsonData['password']
    return password
  except Exception as e:
    MentiiLogging.getLogger().exception(e)
    return None

def isEmailValid(email):
  '''
  Validate that thee email is matches the
  format required.
  '''
  emailRegex = re.compile(r"[^@]+@[^@]+\.[^@]+")
  return emailRegex.match(email) is not None

def isPasswordValid(password):
  return len(password) >= 8

def addUserAndSendEmail(httpOrigin, email, password, mailer, dbInstance):
  activationId = str(uuid.uuid4())
  table = dbUtils.getTable('users', dbInstance)

  jsonData = {
    'email': email,
    'password': password,
    'activationId': activationId,
    'active': 'F',
    'userRole' : "student"
  }
  if table is None:
    MentiiLogging.getLogger().error('Unable to get table users in addUserAndSendEmail')
    activationId = None

  #This will change an existing user with the same email.
  response = dbUtils.putItem(jsonData,table)

  if response is None:
    MentiiLogging.getLogger().error('Unable to add user to table users in addUserAndSendEmail')
    activationId = None

  try:
    sendEmail(httpOrigin, email, activationId, mailer)
  except Exception as e:
    MentiiLogging.getLogger().exception(e)

  return activationId

def deleteUser(email, dbInstance):
  table = dbUtils.getTable('users', dbInstance)
  key = {'email': email}
  response = dbUtils.deleteItem(key, table)
  return response

def sendEmail(httpOrigin, email, activationId, mailer):
  '''
  Create a message and send it from our email to
  the passed in email. The message should contain
  a link built with the activationId
  '''
  if activationId is None:
    return
  #Change the URL to the appropriate environment
  host = getProperEnvironment(httpOrigin)
  url = host + '/activation/{0}'.format(activationId)
  message = render_template('registrationEmail.html', url=url)
  #Build Message
  msg = Message('Mentii: Thank You for Creating an Account!', recipients=[email],
      extra_headers={'Content-Transfer-Encoding': 'quoted-printable'}, html=message)
  #Send Email
  mailer.send(msg)

def isEmailInSystem(email, dbInstance):
  user = getUserByEmail(email, dbInstance)
  return user != None and 'email' in user.keys()

def activate(activationId, dbInstance):
  response = ControllerResponse()
  table = dbUtils.getTable('users', dbInstance)
  items = []

  if table is None:
    MentiiLogging.getLogger().error('Unable to get table users in activate')
    response.addError('Could not access table. Error', 'The DB did not give us the table')
    return response

  #Scan for the email associated with this activationId
  scanResponse = dbUtils.scanFilter('activationId', activationId, table)

  if scanResponse is not None:
    #scanResponse is a dictionary that has a list of 'Items'
    items = scanResponse['Items']

  if not items or 'email' not in items[0].keys():
    response.addError('No user with activationid', 'The DB did not return a user with the passed in activationId')
  else:
    email = items[0]['email']

    jsonData = {
      'Key': {'email': email},
      'UpdateExpression': 'SET active = :a',
      'ExpressionAttributeValues': { ':a': 'T' },
      'ReturnValues' : 'UPDATED_NEW'
    }

    #Update using the email we have
    res = dbUtils.updateItem(jsonData, table)
    response.addToPayload('status', 'Success')

  return response

def isUserActive(user):
  return user != None and 'active' in user.keys() and user['active'] == 'T'

def getUserByEmail(email, dbInstance):
  user = None

  table = dbUtils.getTable('users', dbInstance)
  if table is None:
    MentiiLogging.getLogger().error('Unable to get table users in getUserByEmail')
  else:
    key = {'Key' : {'email': email}}
    result = dbUtils.getItem(key, table)
    if result is None:
      MentiiLogging.getLogger().error('Unable to get the user with email: ' + email + ' in getUserByEmail ')
    elif 'Item' in result.keys():
      user = result['Item']

  return user

def changeUserRole(jsonData, dbInstance, adminRole=None):
  response = ControllerResponse()

  #g will be not be available during testing
  #and adminRole will need to be passed to the function
  if g: # pragma: no cover
    adminRole = g.authenticatedUser['userRole']
  #adminRole is confirmed here incase changeUserRole is called from somewhere
  #other than app.py changeUserRole()
  if adminRole != 'admin':
    response.addError('Role Error', 'Only admins can change user roles')
  elif 'email' not in jsonData.keys() or 'userRole' not in jsonData.keys():
    response.addError('Key Missing Error', 'Email or role missing from json data')
  else:
    email = jsonData['email']
    userRole = jsonData['userRole']

    userTable = dbUtils.getTable('users', dbInstance)
    if userTable is None:
      MentiiLogging.getLogger().error('Unable to get table "users" in changeUserRole')
      response.addError('No Access to Data', 'Unable to get data from database')
    else:
      if userRole != 'student' and userRole != 'teacher' and userRole != 'admin':
        MentiiLogging.getLogger().error('Invalid role: ' + userRole + ' specified. Unable to change user role')
        response.addError('Invalid Role Type', 'Invaid role specified')
      else:

        data = {
            'Key': {'email': email},
            'UpdateExpression': 'SET userRole = :ur',
            'ExpressionAttributeValues': { ':ur': userRole },
            'ReturnValues' : 'UPDATED_NEW'
        }

        result = dbUtils.updateItem(data, userTable)

        if result is None:
          MentiiLogging.getLogger().error('Unable to update the user with email: ' + email + ' in changeUserRole')
          response.addError('Result Update Error', 'Could not update the user role in database')
        else:
          response.addToPayload('Result:', result)
          response.addToPayload('success', 'true')

  return response

def getRole(userEmail, dynamoDBInstance):
  '''
  Returns the role of the user whose email is pased. If we are unable to get
  this information from the DB the role None is returned. Calling code must
  grant only student permissions in this case.
  '''

  userRole = None
  table = dbUtils.getTable('users', dynamoDBInstance)
  if table is None:
    MentiiLogging.getLogger().error('Could not get user table in getUserRole')
  else:
    request = {"Key" : {"email": userEmail}, "ProjectionExpression": "userRole"}
    res = dbUtils.getItem(request, table)
    if res is None or 'Item' not in res:
      MentiiLogging.getLogger().error('Could not get role for user ' + userEmail)
    else:
      userRole = res['Item']['userRole']

  return userRole

def joinClass(jsonData, dynamoDBInstance, email=None):
  response = ControllerResponse()
  #g will be not be available during testing
  #and email will need to be passed to the function
  if g: # pragma: no cover
    email = g.authenticatedUser['email']
  if 'code' not in jsonData.keys() or not jsonData['code']:
    response.addError('Key Missing Error', 'class code missing from data')
  else:
    classCode = jsonData['code']
    updatedClassCodes = addClassCodeToStudent(email, classCode, dynamoDBInstance)
    if not updatedClassCodes:
      response.addError('joinClass call Failed', 'Unable to update user data')
    else:
      updatedClass = addStudentToClass(classCode, email, dynamoDBInstance)
      if not updatedClass:
        response.addError('joinClass call Failed', 'Unable to update class data')
      else:
        response.addToPayload('title', updatedClass['title'])
        response.addToPayload('code', updatedClass['code'])
  return response

def leaveClass(jsonData, dynamoDBInstance, email=None):
  response = ControllerResponse()
  data = None
  if g: # pragma: no cover
    email = g.authenticatedUser['email']
  if 'code' not in jsonData.keys() or not jsonData['code']:
    response.addError('Key Missing Error', 'class code missing from data')
  else:
    classCode = jsonData['code']
    data = {
      'email': email,
      'classCode': classCode
    }
  return class_ctrl.removeStudent(dynamoDBInstance, data, response=response, userRole=None)

def addClassCodeToStudent(email, classCode, dynamoDBInstance):
  userTable = dbUtils.getTable('users', dynamoDBInstance)
  if userTable:
    codeSet = set([classCode])
    addClassToUser = {
      'Key': {'email': email},
      'UpdateExpression': 'ADD classCodes :i',
      'ExpressionAttributeValues': { ':i': codeSet },
      'ReturnValues' : 'UPDATED_NEW'
    }
    res = dbUtils.updateItem(addClassToUser, userTable)
    if (  res and
          'Attributes' in res and
          'classCodes' in res['Attributes'] and
          classCode in res['Attributes']['classCodes']
    ):
      return res['Attributes']['classCodes']
  return None

def addStudentToClass(classCode, email, dynamoDBInstance):
  classTable = dbUtils.getTable('classes', dynamoDBInstance)
  if classTable:
    emailSet = set([email])
    addUserToClass = {
      'Key': {'code': classCode},
      'UpdateExpression': 'ADD students :i',
      'ExpressionAttributeValues': { ':i': emailSet },
      'ReturnValues' : 'ALL_NEW'
    }
    res = dbUtils.updateItem(addUserToClass, classTable)
    if (  res and
          'Attributes' in res and
          'students' in res['Attributes'] and
          email in res['Attributes']['students'] and
          'title' in res['Attributes']
    ):
      return res['Attributes']
  return None
