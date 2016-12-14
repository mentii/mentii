import unittest
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from flask_mail import Mail
import ConfigParser as cp

app = Flask(__name__)
mail = Mail(app)

class UserControlTests(unittest.TestCase):

  def test_parseEmail(self):
    validJson = {"email" : "johndoe@email.com"}
    invalidJson = {}
    self.assertEqual(usr.parseEmail(validJson),"johndoe@email.com",msg="Unable to parse email field from json data")
    self.assertIsNone(usr.parseEmail(invalidJson))

  def test_parsePassword(self):
    validJson = {"password" : "pw"}
    invalidJson = {}
    self.assertEqual(usr.parsePassword(validJson),"pw",msg="Unable to parse password field from json data")
    self.assertIsNone(usr.parsePassword(invalidJson))

  def test_validateRegistrationJSON(self):
    validJson = {"email" : "marydoe@mentii.com", "password":"water"}
    missingEmail = {"password":"notMissing"}
    missingPassword = {"email" : "notMissing"}

    self.assertTrue(usr.validateRegistrationJSON(validJson), msg="Unable to validate registration email and password")
    self.assertFalse(usr.validateRegistrationJSON(missingEmail))
    self.assertFalse(usr.validateRegistrationJSON(missingPassword))
    self.assertFalse(usr.validateRegistrationJSON(None))

  def test_isEmailValid(self):
    validEmail = "hello@world.com"
    invalidEmail = "helloworldcom"

    self.assertTrue(usr.isEmailValid(validEmail))
    self.assertFalse(usr.isEmailValid(invalidEmail))

  def test_isPasswordValid(self):
    validPassword = "iameight"
    invalidPassword = "less"

    self.assertTrue(usr.isPasswordValid(validPassword))
    self.assertFalse(usr.isPasswordValid(invalidPassword))

  def test_register_fail(self):
    jsonData = {"email" : "mail@email.com"}
    dbInstance = "blah"
    self.assertEqual(usr.register(jsonData,mail,dbInstance),"Failing Registration Validation")

class UserControlDBTests(unittest.TestCase):
  '''@classmethod
  def setUpClass(self):
    from ddbmock import connect_boto_patch
    from ddbmock.database.db import dynamodb
    from ddbmock.database.table import Table
    from ddbmock.database.key import PrimaryKey

    # Do a full database wipe
    dynamodb.hard_reset()

    # Instanciate the keys
    hash_key = PrimaryKey(TABLE_HK_NAME, TABLE_HK_TYPE)
    range_key = PrimaryKey(TABLE_RK_NAME, TABLE_RK_TYPE)

    # Create a test table and register it in ``self`` so that you can use it directly
    self.t1 = Table(TABLE_NAME, TABLE_RT, TABLE_WT, hash_key, range_key)

    # Very important: register the table in the DB
    dynamodb.data[TABLE_NAME]  = self.t1

    # Unconditionally add some data, for example.
    self.t1.put(ITEM, {})

    # Create the database connection ie: patch boto
    self.db = connect_boto_patch()

  @classmethod
  def tearDownClass(self):
    from ddbmock.database.db import dynamodb
    from ddbmock import clean_boto_patch

    # Do a full database wipe
    dynamodb.hard_reset()

    # Remove the patch from Boto code (if any)
    clean_boto_patch()

  def test_isEmailInSystem(self):
    email = ""
    # dictionary
    var = usr.isEmailInSystem(email)
    self.assertEqual()

  # TODO register() success case

  # TODO need to create a test email in the system to query


  # TODO test email instead of what's below?
  # add test case where existing user with the same email is given
  def test_addUserAndSendEmail(self):
    email = "email@test.com"
    password = "password8"
    activationId = usr.addUserAndSendEmail(email,password,mail)
    self.assertEqual(activationId,)

  def test_addUserAndSendEmail_fail(self):
    email = "email"
    password = "password8"
    activationId = usr.addUserAndSendEmail(email,password,mail)

    self.assertEqual(activationId,"none")

  # TODO sendEmail

  # TODO add test activationId
  def test_activate(self):
    activationId = "?"
    response = usr.activate(activationId)
    self.assertEqual(response, "Success")

  def test_activate_fail(self):
    activationId = "none"
    response = usr.activate(activationId)
    self.assertEqual(response, "Error!! Could not find an item with that code.")'''

if __name__ == '__main__':
  if __package__ is None:
    import sys
    from os import path
    sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
    from mentii import user_ctrl as usr
  else:
    from ..mentii import user_ctrl as usr
  unittest.main()
