from flask import g
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from boto3.dynamodb.conditions import Key, Attr
import hashlib
import ConfigParser as cp

class MentiiAuthentication:

  def __init__(self):
    return

  @staticmethod
  def build_user_object(userData):
    '''
    Builds a standard user object to return to the client for all authenticated calls
    '''
    #Eventually add role to this packet
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
  def generate_auth_token(userCredentials, expiration = 600):
    '''
    Generates the auth token based off of the user's email and password with a default expiration duration
    '''
    appSecret = MentiiAuthentication.get_app_secret()
    s = Serializer(appSecret, expires_in = expiration)
    email = userCredentials['email']
    password = userCredentials['password']
    return s.dumps({ 'email': email, 'password': password })

  @staticmethod
  def verify_auth_token(token):
    '''
    Reads the auth token to make sure it has not been modified and that it is not expired
    '''
    appSecret = MentiiAuthentication.get_app_secret()
    s = Serializer(appSecret)
    try:
      data = s.loads(token)
    except SignatureExpired:
      print 'signature expired' # TODO: throw exception
      return None # valid token, but expired
    except BadSignature:
      print 'bad signature' # TODO: throw exception
      return None # invalid token
    user = data
    return user

  @staticmethod
  def verify_password(emailOrToken, password, dynamoDBInstance):
    '''
    Verifies the user's credentials for all authenticated calls. This is called by the @auth.login_required
    decorator. Reads from information passed in through a Basic Authentication HTTP header. Username is
    either email or the token. If the token is passed as the username the password field is unused.
    '''
    user = MentiiAuthentication.verify_auth_token(emailOrToken)
    if not user:
      if emailOrToken == '' or password == '':
        return False
      table = dynamoDBInstance.Table('users')
      # Eventually add the user's role to this so we can read if they are an admin or not by the token
      result = table.get_item(Key={'email': emailOrToken}, AttributesToGet=['email', 'active', 'password'])
      if 'Item' not in result:
        return False
      if result['Item']['active'] != 'T':
        return False
      hashedPassword = result['Item']['password']
      testPassword = hashlib.md5(password).hexdigest()
      if hashedPassword != testPassword:
        return False
      else:
        g.authenticatedUser = MentiiAuthentication.build_user_object(result['Item'])
    else:
      g.authenticatedUser = MentiiAuthentication.build_user_object(user)
    return True
