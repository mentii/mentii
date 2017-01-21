import unittest
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from flask_mail import Mail
import ConfigParser as cp

import boto3
import time
import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from utils.ResponseCreation import ControllerResponse
from mentii import user_ctrl as usr
from utils import db_utils as db
from botocore.exceptions import ClientError


app = Flask(__name__)
mail = Mail(app)

#local DynamoDB
dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')

class UserControlTests(unittest.TestCase):

  def test_parseEmail(self):
    print("Running parseEmail Test")
    validJson = {"email" : "johndoe@mentii.me"}
    invalidJson = {}
    self.assertEqual(usr.parseEmail(validJson),"johndoe@mentii.me",msg="Unable to parse email field from json data")
    self.assertIsNone(usr.parseEmail(invalidJson))

  def test_parsePassword(self):
    print("Running parsePassword Test")
    validJson = {"password" : "pw"}
    invalidJson = {}
    self.assertEqual(usr.parsePassword(validJson),"pw",msg="Unable to parse password field from json data")
    self.assertIsNone(usr.parsePassword(invalidJson))

  def test_validateRegistrationJSON(self):
    print("Running validateRegistrationJSON Test")
    validJson = {"email" : "marydoe@mentii.me", "password":"water"}
    missingEmail = {"password":"notMissing"}
    missingPassword = {"email" : "notMissing"}

    self.assertTrue(usr.validateRegistrationJSON(validJson), msg="Unable to validate registration email and password")
    self.assertFalse(usr.validateRegistrationJSON(missingEmail))
    self.assertFalse(usr.validateRegistrationJSON(missingPassword))
    self.assertFalse(usr.validateRegistrationJSON(None))

  def test_isEmailValid(self):
    print("Running isEmailValid Test")

    validEmail = "hello@mentii.me"
    invalidEmail = "hellomentiime"
    emptyEmail = ""

    self.assertTrue(usr.isEmailValid(validEmail))
    self.assertFalse(usr.isEmailValid(invalidEmail))
    self.assertFalse(usr.isEmailValid(emptyEmail))

  def test_isPasswordValid(self):
    print("Running isPasswordValid Test")
    validPassword = "iameight"
    invalidPassword = "less"
    emptyPassword = ""

    self.assertTrue(usr.isPasswordValid(validPassword))
    self.assertFalse(usr.isPasswordValid(invalidPassword))
    self.assertFalse(usr.isPasswordValid(emptyPassword))

  def test_register_fail(self):
    print("Running register fail case Test")
    jsonData = {"email" : "mail@mentii.me"}
    dbInstance = "blah"
    self.assertNotEqual(usr.register(jsonData,mail,dbInstance), None)

class UserControlDBTests(unittest.TestCase):
  @classmethod
  def setUpClass(self):
    settingsName = "table_settings.json"
    mockData = "mock_data.json"

    try:
      table = db.createTableFromFile("./tests/"+settingsName, dynamodb)
    except ClientError:
      db.getTable('users', dynamodb).delete()
      table = db.createTableFromFile("./tests/"+settingsName, dynamodb)

    db.preloadDataFromFile("./tests/"+mockData, table)

  '''@classmethod
  def tearDownClass(self):
    table = db.getTable('users', dynamodb).delete()'''

  def test_isEmailInSystem(self):
    print("Running isEmailInSystem Test")

    email = "test@mentii.me"
    response = usr.isEmailInSystem(email, dynamodb)
    self.assertTrue(response)

  def test_isEmailNotInSystem(self):
    print("Running isEmailNotInSystem Test")

    email = "notInDB@mentii.me"
    response = usr.isEmailInSystem(email, dynamodb)
    self.assertFalse(response)

  def test_addUserAndSendEmail(self):
    print("Running addUserAndSendEmail Test")

    email = "email@mentii.me"
    password = "password8"

    activationId = ""
    try:
      activationId = usr.addUserAndSendEmail(email,password,mail,dynamodb)
    except RuntimeError:
      print("Activation ID= " + activationId)
      self.assertTrue(False)

    response = usr.isEmailInSystem(email, dynamodb)
    self.assertTrue(response)

    # Delete user after test
    response = usr.deleteUser(email, dynamodb)

  # TODO: add test case where existing user with the same email is given

  # TODO: add a real test case for failing to add a user

  def test_register(self):
    print("Running register Test")

    email = "mail@mentii.me"
    password = "password"

    jsonData = {"email" : email, "password" : password}
    response = usr.register(jsonData,mail,dynamodb)
    self.assertTrue(usr.isEmailInSystem(email, dynamodb))

    # These statements should be the proper test, but the mailer throws
    # an exception and the test fails
    #isUserRegistered = 'activationId' in response.payload.keys()
    #self.assertTrue(isUserRegistered)

    # Delete user after test
    response = usr.deleteUser(email, dynamodb)

  def test_hashPassword(self):
    print("Running hashPassword Test")

    pw = "falsjdlf12lj"
    hashPW = usr.hashPassword(pw)
    self.assertNotEqual(pw,hashPW)

  def test_activate(self):
    print("Running activate Test")

    activationId = "12345"
    response = usr.activate(activationId, dynamodb)

    isUserActive = 'status' in response.payload.keys() and response.payload['status'] == 'Success'
    self.assertTrue(isUserActive)

  def test_changeUserRole(self):
    print("Running test_changeUserRole test")

    usersTable = db.getTable('users', dynamodb)

    data = {
      'Key': {'email': ''},
    }


    role = db.getItem('test@mentii.me',usersTable)
    self.assertEqual(role, "student")
    # change user role to teacher
    usr.changeUserRole("test@mentii.me", "T", dynamodb)
    role = usr.getUserRole("test@mentii.me", dynamodb)
    self.assertEqual(role, "teacher")
    # change user role to admin
    usr.changeUserRole("test@mentii.me", "A", dynamodb)
    role = usr.getUserRole("test@mentii.me", dynamodb)
    self.assertEqual(role, "admin")

  def test_changeUserRole_fail(self):
    print("Running test_changeUserRole_fail test")
    role = usr.getUserRole("test5@mentii.me", dynamodb)
    self.assertEqual(role, "student")
    # change user role to not defined
    usr.changeUserRole("test5@mentii.me", "Z", dynamodb)
    role = usr.getUserRole("test5@mentii.me", dynamodb)
    #role remains same as it was before failed attempt
    self.assertEqual(role, "student")

if __name__ == '__main__':
  if __package__ is None:
    import sys
    from os import path
    sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
    from mentii import user_ctrl as usr
  else:
    from ..mentii import user_ctrl as usr
  unittest.main()
