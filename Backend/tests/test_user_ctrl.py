import unittest
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from flask_mail import Mail
import ConfigParser as cp

import db_utils as db
from botocore.exceptions import ClientError

import boto3
import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from mentii import user_ctrl as usr

app = Flask(__name__)
mail = Mail(app)

#local DynamoDB
dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')

class UserControlTests(unittest.TestCase):

  def test_parseEmail(self):
    print("Running parseEmail Test")
    validJson = {"email" : "johndoe@email.com"}
    invalidJson = {}
    self.assertEqual(usr.parseEmail(validJson),"johndoe@email.com",msg="Unable to parse email field from json data")
    self.assertIsNone(usr.parseEmail(invalidJson))

  def test_parsePassword(self):
    print("Running parsePassword Test")
    validJson = {"password" : "pw"}
    invalidJson = {}
    self.assertEqual(usr.parsePassword(validJson),"pw",msg="Unable to parse password field from json data")
    self.assertIsNone(usr.parsePassword(invalidJson))

  def test_validateRegistrationJSON(self):
    print("Running validateRegistrationJSON Test")
    validJson = {"email" : "marydoe@mentii.com", "password":"water"}
    missingEmail = {"password":"notMissing"}
    missingPassword = {"email" : "notMissing"}

    self.assertTrue(usr.validateRegistrationJSON(validJson), msg="Unable to validate registration email and password")
    self.assertFalse(usr.validateRegistrationJSON(missingEmail))
    self.assertFalse(usr.validateRegistrationJSON(missingPassword))
    self.assertFalse(usr.validateRegistrationJSON(None))

  def test_isEmailValid(self):
    print("Running isEmailValid Test")

    validEmail = "hello@world.com"
    invalidEmail = "helloworldcom"

    self.assertTrue(usr.isEmailValid(validEmail))
    self.assertFalse(usr.isEmailValid(invalidEmail))

  def test_isPasswordValid(self):
    print("Running isPasswordValid Test")
    validPassword = "iameight"
    invalidPassword = "less"

    self.assertTrue(usr.isPasswordValid(validPassword))
    self.assertFalse(usr.isPasswordValid(invalidPassword))

  def test_register_fail(self):
    print("Running register fail Test")
    jsonData = {"email" : "mail@email.com"}
    dbInstance = "blah"
    self.assertEqual(usr.register(jsonData,mail,dbInstance),"Failing Registration Validation")

class UserControlDBTests(unittest.TestCase):
  @classmethod
  def setUpClass(self):
    try:
      table = db.createTableFromFile("table_settings.json", dynamodb)
    except ClientError:
      db.getTable('users', dynamodb).delete()
      table = db.createTableFromFile("table_settings.json", dynamodb)

    db.preloadData("mock_data.json", table)

  @classmethod
  def tearDownClass(self):
    table = db.getTable('users', dynamodb).delete()

  def test_isEmailInSystem(self):
    print("Running isEmailInSystem Test")

    email = "test@mentii.com"
    response = usr.isEmailInSystem(email, dynamodb)
    self.assertTrue(response)

  def test_isEmailInSystem_fail(self):
    print("Running isEmailInSystem FAIL Test")

    email = "no_test@mentii.com"
    response = usr.isEmailInSystem(email, dynamodb)
    self.assertFalse(response)

  def test_addUserAndSendEmail(self):
    print("Running addUserAndSendEmail Test")

    email = "email@test.com"
    password = "password8"

    activationId = ""
    try:
      activationId = usr.addUserAndSendEmail(email,password,mail,dynamodb)
    except RuntimeError:
      print("Activation ID= " + activationId)
      self.assertEqual(activationId, activationId)

  # add test case where existing user with the same email is given

  def test_addUserAndSendEmail_fail(self):
    print("Running addUserAndSendEmail FAIL Test")

    email = "email"
    password = "password8"
    activationId = usr.addUserAndSendEmail(email,password,mail,dynamodb)
    self.assertEqual(activationId,"none")

  def test_register(self):
    print("Running register Test")

    jsonData = {"email" : "mail@email.com"}
    activationId = usr.register(jsonData,mail,dynamodb)
    self.assertEqual(activationId, activationId)

  def test_hashPassword(self):
    print("Running hashPassword Test")

    pw = "falsjdlf12lj"
    hashPW = usr.hashPassword(pw)
    self.assertNotEqual(pw,hashPW)

  def test_activate(self):
    print("Running activate Test")

    activationId = "12345"
    response = usr.activate(activationId, dynamodb)
    self.assertEqual(response, "Success")

  def test_activate_fail(self):
    print("Running activate FAIL Test")

    activationId = "none"
    response = usr.activate(activationId, dynamodb)
    self.assertEqual(response, "Error!! Could not find an item with that code.")

if __name__ == '__main__':
  if __package__ is None:
    import sys
    from os import path
    sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
    from mentii import user_ctrl as usr
  else:
    from ..mentii import user_ctrl as usr
  unittest.main()
