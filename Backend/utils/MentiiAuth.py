from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

class MentiiAuthentication:

  def __init__(self):
    self.secret = 'SECRET_KEY'

  def generate_auth_token(self, user_credentials, expiration = 600):
    s = Serializer('SECRET_KEY', expires_in = expiration)
    email = user_credentials['email']
    password = user_credentials['password']
    return s.dumps({ 'email': email, 'password': password })

  @staticmethod
  def verify_auth_token(token):
    s = Serializer('SECRET_KEY')
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
