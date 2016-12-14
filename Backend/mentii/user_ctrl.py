import boto3
import re
from flask_mail import Message
from boto3.dynamodb.conditions import Key, Attr
import uuid
import hashlib

def register(jsonData, mailer, dbInstance):
  if validateRegistrationJSON(jsonData):
    email = parseEmail(jsonData)
    hashedPassword = hashlib.md5( parsePassword(jsonData) ).hexdigest()
    activationId = addUserAndSendEmail(email, hashedPassword, mailer, dbInstance)
    return activationId
  else:
    return 'Failing Registration Validation'

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
  if isEmailValid(email) and isPasswordValid(password) and not isEmailInSystem(email, dbInstance):
    activationId = str(uuid.uuid4())
    dynamodb = dbInstance
    table = dynamodb.Table('users')

    #This will change an existing user with the same email.
    response = table.put_item(
      Item={
        'email': email,
        'password': password,
        'activationId': activationId
      }
    )
    sendEmail(email, activationId, mailer)
    return activationId
  else:
    return 'none'

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
  result = table.get_item(Key={'email': email}, AttributesToGet=['active'])
  return 'Item' in result.keys() and 'active' in result['Item'].keys() and result['Item']['active'] == 'T'

def activate(activationId, dbInstance):
  dynamodb = dbInstance
  table = dynamodb.Table('users')
  items = []

  #Scan for the email associated with this activationId
  scanResponse = table.scan(FilterExpression=Attr('activationId').eq(activationId))

  if scanResponse is not None:
    #scanResponse is a dictionary that has a list of 'Items'
    items = scanResponse['Items']

  if not items and 'email' in items[0].keys():
    return "Error!! Could not find an item with that code."
  else:
    email = items[0]['email']

    #Update using the email we have
    response = table.update_item(
    Key={
        'email': email,
      },
      UpdateExpression="SET active = :a",
      ExpressionAttributeValues={
        ':a': 'T'
      },
      ReturnValues='UPDATED_NEW'
    )
    return "Success"
