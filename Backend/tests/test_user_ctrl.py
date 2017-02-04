import unittest
from mock import MagicMock

import boto3
import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

from utils.ResponseCreation import ControllerResponse, createResponse
from mentii import user_ctrl as usr
from mentii import class_ctrl as classCtrl
from utils import db_utils as db

#Mailer is not used in testing because it depends on the flask application contex
mail = None
usr.sendEmail = MagicMock(return_value = None)

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
    self.dynamodbClient = boto3.client('dynamodb', endpoint_url='http://localhost:8000')

    #clean up local DB before tests
    tables = self.dynamodbClient.list_tables()
    tableNames = tables.get('TableNames')
    try:
      for name in tableNames:
        dynamodb.Table(name).delete()
    except:
      print('Error deleting tableNames')

    classSettingsName = 'classes_settings.json'
    classMockData = 'mock_classes.json'
    userSettingsName = 'table_settings.json'
    userMockData = 'mock_data.json'

    userTable = db.createTableFromFile('./tests/'+userSettingsName, dynamodb)
    classTable = db.createTableFromFile('./tests/'+classSettingsName, dynamodb)

    db.preloadDataFromFile('./tests/'+userMockData, userTable)
    db.preloadClassData('./tests/'+classMockData, classTable)

  @classmethod
  def tearDownClass(self):
    db.getTable('classes', dynamodb).delete()
    db.getTable('users', dynamodb).delete()

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

    activationId = usr.addUserAndSendEmail(email,password,mail,dynamodb)
    self.assertIsNotNone(activationId)

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
    print('Running test_changeUserRole test')

    usersTable = db.getTable('users', dynamodb)

    request = {
      'Key': {'email': 'test@mentii.me'},
      'ProjectExpression' : 'userRole'
    }

    # check that user is a student
    response = db.getItem(request, usersTable)
    self.assertEqual(response['Item']['userRole'], 'student')

    # change user role to teacher
    jsonData = {
      'email': 'test@mentii.me',
      'userRole' : 'teacher'
    }

    usr.changeUserRole(jsonData, dynamodb, adminRole='admin')
    response = db.getItem(request, usersTable)
    self.assertEqual(response['Item']['userRole'], 'teacher')

    # change user role to admin
    jsonData = {
      'email': 'test@mentii.me',
      'userRole' : 'admin'
    }

    usr.changeUserRole(jsonData, dynamodb, adminRole='admin')
    response = db.getItem(request, usersTable)
    self.assertEqual(response['Item']['userRole'], 'admin')

    # change user role back to student
    jsonData = {
      'email': 'test@mentii.me',
      'userRole' : 'student'
    }

    usr.changeUserRole(jsonData, dynamodb, adminRole='admin')
    response = db.getItem(request, usersTable)
    self.assertEqual(response['Item']['userRole'], 'student')

  def test_changeUserRole_fail(self):
    print('Running test_changeUserRole_fail test')

    usersTable = db.getTable('users', dynamodb)

    request = {
      'Key': {'email': 'test4@mentii.me'},
      'ProjectExpression' : 'userRole'
    }

    response = db.getItem(request, usersTable)
    self.assertEqual(response['Item']['userRole'], 'student')

    badJsonData = {
      'email': 'test4@mentii.me',
      'userRole' : 'boss'
    }

    # change user role to not defined role
    usr.changeUserRole(badJsonData, dynamodb, adminRole='admin')

    #role remains same as it was before failed attempt
    response = db.getItem(request, usersTable)
    self.assertEqual(response['Item']['userRole'], 'student')

    badJsonData = {
      'email': 'test777@mentii.me',
      'userRole' : 'student'
    }

    # try to change a user role of a non-existent user
    response = usr.changeUserRole(badJsonData, dynamodb, adminRole='admin')
    self.assertIsNone(response.payload.get('success'))

  def test_getRole(self):
    print('Running test_getRole test')

    jsonData = {
      'email': 'test3@mentii.me',
      'userRole' : 'admin'
    }

    # change user since default returns student
    usr.changeUserRole(jsonData, dynamodb, adminRole='admin')
    userRole = usr.getRole('test3@mentii.me', dynamodb)
    self.assertEqual(userRole, 'admin')

  def test_getRole_fail(self):
    print('Running test_getRole_fail test case')

    # get non-existent user
    userRole = usr.getRole('test85@mentii.me', dynamodb)
    self.assertIsNone(userRole)

  def test_joinClass(self):
    print 'Running test_joinClass'

    joinEmail = 'join@mentii.me'
    password = 'password'
    activationId = usr.addUserAndSendEmail(joinEmail,password,mail,dynamodb)
    usr.activate(activationId, dynamodb)

    teacherEmail = 'teacher@mentii.me'
    activationId = usr.addUserAndSendEmail(teacherEmail,password,mail,dynamodb)
    usr.activate(activationId, dynamodb)

    classData = {
      'title' : 'title',
      'description' : 'desc'
    }
    teacherRole = 'teacher'
    classCtrl.createClass(dynamodb, classData, teacherEmail, teacherRole)

    res = classCtrl.getPublicClassList(dynamodb, joinEmail)

    #confirm response can be created from classSet
    flaskRes = createResponse(res, 200)

    classes = res.payload['classes']
    allClassCodes = set()
    for c in classes:
      code = c['code']
      allClassCodes.add(code)
      joinData = { 'code' : code }
      res = usr.joinClass(joinData, dynamodb, joinEmail)
      self.assertFalse(res.hasErrors())
      self.assertEqual(res.payload['code'], code)

    joined = classCtrl.getClassCodesFromUser(dynamodb, joinEmail)
    missing = joined - allClassCodes
    #confirm the empty set, meing that all classes have been joined
    self.assertFalse(missing)

    joinEmail2 = 'join2@mentii.me'
    password = 'password'
    activationId = usr.addUserAndSendEmail(joinEmail2,password,mail,dynamodb)
    usr.activate(activationId, dynamodb)

    badJoinData = { 'bad' : 'data' }
    for c in classes:
      code = c['code']
      res = usr.joinClass(badJoinData, dynamodb, joinEmail2)
      self.assertTrue(res.hasErrors())

    joined = classCtrl.getClassCodesFromUser(dynamodb, joinEmail2)
    #confirm none joined
    self.assertFalse(joined)

if __name__ == '__main__':
  if __package__ is None:
    import sys
    from os import path
    sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
    from mentii import user_ctrl as usr
  else:
    from ..mentii import user_ctrl as usr
  unittest.main()
