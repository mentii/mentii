from flask import g
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from boto3.dynamodb.conditions import Key, Attr
import hashlib
import ConfigParser as cp
from mentii import user_ctrl

class MentiiAuthentication:

  def __init__(self):
    return

  @staticmethod
  def build_user_object(userData):
    '''
    Builds a standard user object to return to the client for all authenticated calls
    '''
    return {'email': userData['email']}

  @staticmethod
  def get_app_secret():
    '''
    Reads from the prodConfig.ini file for the appSecret
    '''
    parser = cp.ConfigParser()
    parser.read("/config/prodConfig.ini")
    return parser.get('MentiiAuthentication', 'appSecret')

  @staticmethod
  def generate_auth_token(userCredentials, expiration = 86400):
    '''
    Generates the auth token based off of the user's email and password with a default expiration duration.
    Default token will last 1 day.
    '''
    retval = None
    try:
      appSecret = MentiiAuthentication.get_app_secret()
      s = Serializer(appSecret, expires_in = expiration)
      email = userCredentials['email']
      password = userCredentials['password']
      retval = s.dumps({ 'email': email, 'password': password })
    except:
      retval = None
    return retval

  @staticmethod
  def verify_auth_token(token):
    '''
    Reads the auth token to make sure it has not been modified and that it is not expired
    '''
    retval = None
    appSecret = MentiiAuthentication.get_app_secret()
    s = Serializer(appSecret)
    try:
      user = s.loads(token)
      retval = user # user from token
    except SignatureExpired:
      retval = None # valid token, but expired
    except BadSignature:
      retval = None # invalid token
    return retval

  @staticmethod
  def isPasswordValid(user, password):
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

  @staticmethod
  def verify_password(emailOrToken, password, dynamoDBInstance):
    '''
    Verifies the user's credentials for all authenticated calls. This is called by the @auth.login_required
    decorator. Reads from information passed in through a Basic Authentication HTTP header. Username is
    either email or the token. If the token is passed as the username the password field is unused.
    '''
    user = MentiiAuthentication.verify_auth_token(emailOrToken)
    isPasswordVerified = False
    if not user:
      if emailOrToken != '' and password != '':
        userFromDB = user_ctrl.getUserByEmail(emailOrToken, dynamoDBInstance) # user object from db
        if userFromDB != None and user_ctrl.isUserActive(userFromDB) and MentiiAuthentication.isPasswordValid(userFromDB, password):
          g.authenticatedUser = MentiiAuthentication.build_user_object(userFromDB)
          isPasswordVerified = True
    else:
      g.authenticatedUser = MentiiAuthentication.build_user_object(user)
      isPasswordVerified = True
    return isPasswordVerified
