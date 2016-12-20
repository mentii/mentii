import boto3
import re
from flask_mail import Message
from boto3.dynamodb.conditions import Key, Attr
from utils.ResponseCreation import ControllerResponse
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
  
  if isEmailInSystem(email, dbInstance) and isUserActive(email, dbInstance):
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
  except Exception:
    return None

def parsePassword(jsonData):
  try:
    password = jsonData['password']
    return password
  except Exception:
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
  dynamodb = dbInstance
  table = dynamodb.Table('users')

  #This will change an existing user with the same email.
  response = table.put_item(
    Item={
      'email': email,
      'password': password,
      'activationId': activationId,
      'active': "F"
    }
  )
  try:
    sendEmail(email, activationId, mailer)
  except:
    return None 

  return activationId

def deleteUser(email, dbInstance):
  table = dbInstance.Table('users')
  response = table.delete_item(
    Key={'email': email}
  )

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
  dynamodb = dbInstance
  table = dynamodb.Table('users')

  #Result is a dictionary that will have the key Item if
  # it was able to find an item.
  result = table.get_item(Key={'email': email}, ProjectionExpression='email')
  return 'Item' in result.keys() and 'email' in result['Item'].keys()

def activate(activationId, dbInstance):
  response = ControllerResponse()
  dynamodb = dbInstance
  table = dynamodb.Table('users')
  items = []

  #Scan for the email associated with this activationId
  scanResponse = table.scan(FilterExpression=Attr('activationId').eq(activationId))

  if scanResponse is not None:
    #scanResponse is a dictionary that has a list of 'Items'
    items = scanResponse['Items']

  if not items or 'email' not in items[0].keys():
    response.addError("No user with activationid", "The DB did not return a user with the passed in activationId")
  else:
    email = items[0]['email']

    #Update using the email we have
    res = table.update_item(
    Key={
        'email': email,
      },
      UpdateExpression="SET active = :a",
      ExpressionAttributeValues={
        ':a': 'T'
      },
      ReturnValues='UPDATED_NEW'
    )
    response.addToPayload("status", "Success")

  return response

def isUserActive(email, dbInstance):
  dynamodb = dbInstance
  table = dynamodb.Table('users')

  #Result is a dictionary that will have the key Item if
  # it was able to find an item.
  result = table.get_item(Key={'email': email}, ProjectionExpression='active')
  return 'Item' in result.keys() and 'active' in result['Item'].keys() and result['Item']['active'] == 'T'
