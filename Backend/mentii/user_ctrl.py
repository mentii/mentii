import boto3
import re
from flask_mail import Message
from boto3.dynamodb.conditions import Key, Attr
import uuid

def register(jsonData, mailer):
  if validateRegistrationJSON(jsonData):
    email = parseEmail(jsonData)
    activationId = addUserAndSendEmail(email, parsePassword(jsonData), mailer)
    return activationId
  else:
    return 'Failing Registration Validation'

def validateRegistrationJSON(jsonData):
  '''
  Validate that the JSON object contains
  an email and password attributes
  '''
  try:
    email = parseEmail(jsonData)
    password = parsePassword(jsonData)
  except Exception as e:
    print e
    return False
  
  return True

def parseEmail(jsonData):
  return jsonData['email']

def parsePassword(jsonData):
  return jsonData['password']

def isEmailValid(email):
  '''
  Validate that thee email is matches the
  format required.
  '''
  emailRegex = re.compile(r"[^@]+@[^@]+\.[^@]+")
  return emailRegex.match(email)

def isPasswordValid(password):
  return len(password) >= 8

def addUserAndSendEmail(email, password, mailer):
  if isEmailValid(email) and isPasswordValid(password) and not isEmailInSystem(email):
    activationId = str(uuid.uuid4())
    dynamodb = boto3.resource('dynamodb')
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
  msg.body = "Here is your activationId link: api.mentii.me/activate/{}".format(activationId)

  #Send Email
  mailer.send(msg)

def isEmailInSystem(email):
  dynamodb = boto3.resource('dynamodb')
  table = dynamodb.Table('users')

  #Result is a dictionary that will have the key Item if
  # it was able to find an item.
  result = table.get_item(Key={'email': email}, AttributesToGet=['active'])
  return 'Item' in result.keys() and 'active' in result['Item'].keys() and result['Item']['active'] == 'T'

def activate(activationId):
  dynamodb = boto3.resource('dynamodb')
  table = dynamodb.Table('users')

  #Scan for the email associated with this activationId
  scanResponse = table.scan(FilterExpression=Attr('activationId').eq(activationId))

  if scanResponse is not None:
    #scanResponse is a dictionary that has a list of 'Items'
    items = scanResponse['Items']

  if len(items) != 1:
    return "Error!! Could not find an item with that code."
  else:
    email = items[0]['email']

    #Update using the email we have
    response = table.update_item(
    Key={
        'email': email,
      },
      UpdateExpression="SET active = :a, activationId = :aid",
      ExpressionAttributeValues={
        ':a': 'T',
        ':aid': 'none'
      },
      ReturnValues='UPDATED_NEW'
    )
    return "Success"
