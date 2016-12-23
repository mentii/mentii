import unittest
from contextlib import contextmanager
from flask import appcontext_pushed, g, Flask

import db_utils as db
from botocore.exceptions import ClientError

import boto3
import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from mentii import user_ctrl
from utils import MentiiAuth

app = Flask(__name__)

#local DynamoDB
dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')

class MentiiAuthTests(unittest.TestCase):

  @classmethod
  def setUpClass(self):
    settingsName = "table_settings.json"
    mockData = "mock_data.json"

    try:
      table = db.createTableFromFile("./tests/"+settingsName, dynamodb)
    except ClientError:
      db.getTable('users', dynamodb).delete()
      table = db.createTableFromFile("./tests/"+settingsName, dynamodb)

    db.preloadData("./tests/"+mockData, table)

  @classmethod
  def tearDownClass(self):
    table = db.getTable('users', dynamodb).delete()

  def test_verify_password(self):
    print("Running MentiiAuth.verify_password test")
    emailActive = 'test3@mentii.me'
    emailNotActive = 'test4@mentii.me'
    with app.app_context():
      self.assertTrue(MentiiAuth.verify_password(emailActive, 'testing1', dynamodb, 'test_app_secret'))
      self.assertFalse(MentiiAuth.verify_password(emailActive, 'wrongpassword', dynamodb, 'test_app_secret'))
      self.assertFalse(MentiiAuth.verify_password(emailActive, '', dynamodb, 'test_app_secret'))
      self.assertFalse(MentiiAuth.verify_password(emailNotActive, 'testing1', dynamodb, 'test_app_secret'))
      self.assertFalse(MentiiAuth.verify_password(emailNotActive, 'wrongpassword', dynamodb, 'test_app_secret'))
      self.assertFalse(MentiiAuth.verify_password(emailNotActive, '', dynamodb, 'test_app_secret'))

  def test_isPasswordValid(self):
    print("Running MentiiAuth.isPasswordValid test")
    email = 'test3@mentii.me'
    user = user_ctrl.getUserByEmail(email, dynamodb)
    self.assertTrue(MentiiAuth.isPasswordValid(user, 'testing1'))
    self.assertFalse(MentiiAuth.isPasswordValid(user, 'wrongpassword'))

  def test_verify_auth_token(self):
    print("Running MentiiAuth.verify_auth_token test")
    email = 'test3@mentii.me'
    user = user_ctrl.getUserByEmail(email, dynamodb)
    userCredentials = {"email": user['email'], "password": user['password']}
    testRetVal = {"email": 'test3@mentii.me', "password": '6b7330782b2feb4924020cc4a57782a9'}
    auth_token = MentiiAuth.generate_auth_token(userCredentials, 'test_app_secret')
    fake_auth_token = 'eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ4MjQ1NTU2MywiaWF0IjoxNDgyMzY5MTYzfQ.eyJwYXNzd29yZCI6InRlc3RpbmcxIiwiZW1haWwiOiJqb25tZDI0QGdtYWlsLmNvbSJ9.GWmgu7P5Ro-sHQBSEuL322sldst7McEHvXqY897K9N'
    self.assertEqual(MentiiAuth.verify_auth_token(auth_token, 'test_app_secret'), testRetVal)
    self.assertIsNone(MentiiAuth.verify_auth_token(fake_auth_token, 'test_app_secret'))

  def test_generate_auth_token(self):
    print("Running MentiiAuthentication.generate_auth_token test")
    email = 'test3@mentii.me'
    user = user_ctrl.getUserByEmail(email, dynamodb)
    userCredentials = {"email": user['email'], "password": user['password']}
    auth_token = MentiiAuth.generate_auth_token(userCredentials, 'test_app_secret')
    self.assertIsNotNone(MentiiAuth.verify_auth_token(auth_token, 'test_app_secret'))

if __name__ == '__main__':
  if __package__ is None:
    import sys
    from os import path
    sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
    from mentii import user_ctrl as usr
    from utils import MentiiAuth
  else:
    from ..mentii import user_ctrl as usr
    from ..utils import MentiiAuth
  unittest.main()
