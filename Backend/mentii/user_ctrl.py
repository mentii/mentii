import boto3
import re
from flask_mail import Message
from boto3.dynamodb.conditions import Key, Attr
from utils.ResponseCreation import ControllerResponse
from utils import db_utils as dbUtils
import utils.MentiiLogging as MentiiLogging
import uuid
import hashlib


def register(jsonData, mailer, dbInstance):
  response = ControllerResponse()
  if not validateRegistrationJSON(jsonData):
    response.addError("Register Validation Error", "The json data did not have an email or did not have a password")
    return response

  email = parseEmail(jsonData)
  password = parsePassword(jsonData)

  if not isEmailValid(email):
    response.addError("Email invalid", "The email is invalid")

  if not isPasswordValid(password):
    response.addError("Password Invalid", "The password is invalid")

  if isEmailInSystem(email, dbInstance) and isUserActive(getUserByEmail(email, dbInstance)):
    response.addError("Email Already Active in System", "The email is in the system already")

  if not response.hasErrors():
    hashedPassword = hashPassword(parsePassword(jsonData))
    activationId = addUserAndSendEmail(email, hashedPassword, mailer, dbInstance)
    if activationId is not None:
      response.addToPayload("activationId", activationId)
    else:
      response.addError("Activation Id is None", "Could not create an activation Id")

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

def addUserAndSendEmail(email, password, mailer, dbInstance):
  activationId = str(uuid.uuid4())
  table = dbUtils.getTable('users', dbInstance)

  jsonData = {
    'email': email,
    'password': password,
    'activationId': activationId,
    'active': "F",
    'classCodes' : [],
    'userRole': "student"
  }
  if table is None:
    MentiiLogging.getLogger().error("Unable to get table users in addUserAndSendEmail")
    return None

  #This will change an existing user with the same email.
  response = dbUtils.putItem(jsonData,table)

  if response is None:
    MentiiLogging.getLogger().error("Unable to add user to table users in addUserAndSendEmail")
    return None

  try:
    sendEmail(email, activationId, mailer)
  except Exception as e:
    MentiiLogging.getLogger().exception(e)
    return None

  return activationId

def deleteUser(email, dbInstance):
  table = dbUtils.getTable('users', dbInstance)
  key = {'email': email}
  response = dbUtils.deleteItem(key, table)
  return response

def sendEmail(email, activationId, mailer):
  '''
  Create a message and send it from our email to
  the passed in email. The message should contain
  a link built with the activationId
  '''
  #Build Message
  msg = Message('Mentii: Thank You for Creating an Account!', recipients=[email])
  msg.body = "Here is your activationId link: api.mentii.me/activate/{0}".format(activationId)

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
    MentiiLogging.getLogger().error("Unable to get table users in activate")
    response.addError("Could not access table. Error", "The DB did not give us the table")
    return response

  #Scan for the email associated with this activationId
  scanResponse = dbUtils.scanFilter("activationId", activationId, table)

  if scanResponse is not None:
    #scanResponse is a dictionary that has a list of 'Items'
    items = scanResponse['Items']

  if not items or 'email' not in items[0].keys():
    response.addError("No user with activationid", "The DB did not return a user with the passed in activationId")
  else:
    email = items[0]['email']

    jsonData = {
      "Key": {"email": email},
      "UpdateExpression": "SET active = :a",
      "ExpressionAttributeValues": { ":a": "T" },
      "ReturnValues" : "UPDATED_NEW"
    }

    #Update using the email we have
    res = dbUtils.updateItem(jsonData, table)
    response.addToPayload("status", "Success")

  return response

def isUserActive(user):
  return user != None and 'active' in user.keys() and user['active'] == 'T'

def getUserByEmail(email, dbInstance):
  user = None

  table = dbUtils.getTable('users', dbInstance)
  if table is None:
    MentiiLogging.getLogger().error("Unable to get table users in getUserByEmail")
    return None

  key = {"Key" : {"email": email}}
  result = dbUtils.getItem(key, table)
  if result is None:
    MentiiLogging.getLogger().error("Unable to get the user with email: " + email + " in getUserByEmail ")
    return None

  if 'Item' in result.keys():
    user = result['Item']

  return user

def getUserRole(email, dbInstance):
  role = None

  userTable = dbUtils.getTable('users', dbInstance)
  if userTable is None:
    MentiiLogging.getLogger().error("Unable to get table users in getUserRole")
    return None

  data = {
    "Key" : {"email": email},
    "ProjectionExpression" : "userRole"
  }
  result = dbUtils.getItem(data, userTable)

  if result is None:
    MentiiLogging.getLogger().error("Unable to get the user with email: " + email + " in getUserRole ")
    return None

  print(result)
  role = result['Item']['userRole']

  return role

def changeUserRole(email, role, dbInstance):
  userTable = dbUtils.getTable('users', dbInstance)
  if userTable is None:
    MentiiLogging.getLogger().error("Unable to get table users in changeUserRole")
    return None

  if role == "S":
    ur = "student"
  elif role == "T":
    ur = "teacher"
  elif role == "A":
    ur = "admin"
  else:
    MentiiLogging.getLogger().error("Invalid role: " + role + " specified. Unable to change user role")
    return None

  data = {
      "Key": {"email": email},
      "UpdateExpression": "SET userRole = :ur",
      "ExpressionAttributeValues": { ":ur": ur },
      "ReturnValues" : "UPDATED_NEW"
  }

  result = dbUtils.updateItem(data, userTable)

  if result is None:
    MentiiLogging.getLogger().error("Unable to update the user with email: " + email + " in changeUserRole")
    return None

  return result

