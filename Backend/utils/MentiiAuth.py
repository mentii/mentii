from flask import g
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from boto3.dynamodb.conditions import Key, Attr
import hashlib
import ConfigParser as cp
from mentii import user_ctrl
import utils.MentiiLogging as MentiiLogging

def buildUserObject(userData):
  '''
  Builds a standard user object to return to the client for all authenticated calls
  '''
  if not userDataValid(userData):
    # Anything other than raising an exception here would be a security flaw.
    # If the code executes to this point and userData does not contain an email
    # then something is very bad. If only 'None' was returned then the faulty
    # user would still be given access to resources that they shouldnt be allowed
    MentiiLogging.getLogger().error('Invalid User Data for buildUserObject:' + str(userData))
    raise ValueError('This should not be called anywhere other than within MentiiAuthentication. If email is not an attribute of userData then somehow the user has managed to bypass authentication without an email and should be stopped.')
  else:
    return {'email': userData['email'], 'userRole': userData['userRole']}

def userDataValid(userData):
  return (  'email' in userData.keys() and userData['email'] and
            'userRole' in userData.keys() and userData['userRole'] )

def generateAuthToken(userCredentials, appSecret=None, expiration = 86400):
  '''
  Generates the auth token based off of the user's email and password with a default expiration duration.
  Default token will last 1 day.
  '''
  if appSecret == None:
    raise ValueError('appSecret cannot be none')

  retval = None

  if userCredentialsValid(userCredentials):
    try:
      s = Serializer(appSecret, expires_in = expiration)
      retval = s.dumps({    'email': userCredentials['email'],
                            'password': userCredentials['password'],
                            'userRole': userCredentials['userRole']})
    except Exception as e:
      MentiiLogging.getLogger().exception(e)
      retval = None
  return retval

def userCredentialsValid(userCredentials):
  valid = userDataValid(userCredentials)
  if 'password' not in userCredentials.keys() or not userCredentials['password']:
    valid = False
  return valid

def verifyAuthToken(token, appSecret=None):
  '''
  Reads the auth token to make sure it has not been modified and that it is not expired
  '''
  if appSecret == None:
    raise ValueError('appSecret cannot be none')
  retval = None
  s = Serializer(appSecret)
  try:
    user = s.loads(token)
    retval = user # user from token
  except (SignatureExpired, BadSignature) as e:
    MentiiLogging.getLogger().exception(e)
    retval = None
  return retval

def passwordValid(user, password):
  '''
  Checks that supplied password matches password in database
  '''
  isPasswordValid = False
  if 'password' in user:
    hashedPassword = user['password']
    testPassword = hashlib.md5(password).hexdigest()
    if hashedPassword == testPassword:
      isPasswordValid = True
  return isPasswordValid

def verifyPassword(emailOrToken, password, dynamoDBInstance, appSecret=None):
  '''
  Verifies the user's credentials for all authenticated calls. This is called by the @auth.login_required
  decorator. Reads from information passed in through a Basic Authentication HTTP header. Username is
  either email or the token. If the token is passed as the username the password field is unused.
  '''
  if appSecret == None:
    raise ValueError('appSecret cannot be none')
  user = verifyAuthToken(emailOrToken, appSecret)
  isPasswordVerified = False
  if not user:
    if emailOrToken != '' and password != '':
      userFromDB = user_ctrl.getUserByEmail(emailOrToken, dynamoDBInstance) # user object from db
      if userFromDB != None and user_ctrl.isUserActive(userFromDB) and passwordValid(userFromDB, password):
        g.authenticatedUser = buildUserObject(userFromDB)
        isPasswordVerified = True
  else:
    g.authenticatedUser = buildUserObject(user)
    isPasswordVerified = True
  return isPasswordVerified
