import unittest
import user_ctrl as usr #TODO need to some how import from /mentii
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from flask_mail import Mail
import ConfigParser as cp

app = Flask(__name__)
mail = Mail(app)

class UserControlTests(unittest.TestCase):

  def test_parseEmail(self):
    validJson = {"email" : "johndoe@email.com"}   
    self.assertTrue(usr.parseEmail(validJson), msg="Unable to parse email from json data")

  def test_parsePassword(self):
    validJson = {"password" : "pw"}
    self.assertTrue(usr.parsePassword(validJson), msg="Unable to parse password from json data")

  def test_validateRegistrationJSON(self):
    validJson = {"email" : "marydoe@mentii.com", "password":"water"}
    missingEmail = {"password":"notMissing"}
    missingPassword = {"email" : "notMissing"}

    self.assertTrue(usr.validateRegistrationJSON(validJson), msg="Unable to validate registration email and password")
    self.assertFalse(usr.validateRegistrationJSON(missingEmail))
    self.assertFalse(usr.validateRegistrationJSON(missingPassword))

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
    jsondata = {"email" : "mail@email.com"}
    self.assertEqual(usr.register(jsondata,mail),"Failing Registration Validation")

  # TODO register() success case

  # TODO need to create a test email in the system to query
  def test_isEmailInSystem(self):
    email = ""
    # dictionary
    var = usr.isEmailInSystem(email)
    self.assertEqual()

  # TODO test email instead of what's below?
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
    self.assertEqual(response, "Error!! Could not find an item with that code.")
    

if __name__ == '__main__':
    unittest.main()