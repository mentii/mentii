import unittest


import boto3
import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from mentii import class_ctrl
from utils import db_utils as db


#local DynamoDB
dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')

class ClassCtrlDBTests(unittest.TestCase):
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
    settingsName = 'table_settings.json'
    mockData = 'mock_data.json'

    user_table = db.createTableFromFile('./tests/'+settingsName, dynamodb)
    class_table = db.createTableFromFile('./tests/'+classSettingsName, dynamodb)

    db.preloadClassData('./tests/'+classMockData, class_table)
    db.preloadDataFromFile('./tests/'+mockData, user_table)

  @classmethod
  def tearDownClass(self):
    db.getTable('classes', dynamodb).delete()
    db.getTable('users', dynamodb).delete()

  def test_getActiveClassList(self):
    print('Running getActiveClassList test case')
    user =  'test@mentii.me'
    response = class_ctrl.getActiveClassList(dynamodb, user)
    self.assertIsNotNone(response, None)

  def test_getPublicClassList(self):
    print('Running getPublicClassList test case')
    user =  'test@mentii.me'
    response = class_ctrl.getPublicClassList(dynamodb, user)
    self.assertIsNotNone(response, None)

  def test_getClassCodesFromUser(self):
    print('Running getClassCodesFromUser test case')
    user =  'test@mentii.me'
    response = class_ctrl.getClassCodesFromUser(dynamodb, user)
    self.assertIsNotNone(response, None)
    self.assertTrue(len(response) == 3)

  def test_checkClassDataValid(self):
    print('Running checkClassDataValid')

    classData = {
      'title' : 'hello',
      'description' : 'world'
    }

    self.assertTrue(class_ctrl.checkClassDataValid(classData))
    classData = { 'title' : 'hello' }
    self.assertFalse(class_ctrl.checkClassDataValid(classData))
    classData = { 'description' : 'world' }
    self.assertFalse(class_ctrl.checkClassDataValid(classData))

  def test_createClass(self):
    print('Running creatClass test case')
    classData = {
      'title' : 'PSY',
      'department' : 'science',
      'section' : '25',
      'description' : 'How our brain works'
    }

    email = 'test3@mentii.me'
    userRole = 'teacher'
    response = class_ctrl.createClass(dynamodb, classData, email, userRole)
    # check response message
    self.assertEqual(response.payload, {'Success': 'Class Created'})

    # check that teaching set was added to user
    classesTable = db.getTable('classes', dynamodb)
    usersTable = db.getTable('users', dynamodb)

    data = {'Key': {'email': email}}
    teacher = db.getItem(data, usersTable)
    print(teacher)
    self.assertTrue('Item' in teacher.keys())
    self.assertTrue('teaching' in teacher['Item'])

    teachingList = list(teacher['Item']['teaching'])

    # check that class was created in classes table
    classCode = str(teachingList[0])
    data = {'Key': {'code': classCode}}
    classItem = db.getItem(data, classesTable)
    print(classItem)
    self.assertTrue('Item' in classItem.keys())
    self.assertEqual(classItem['Item']['title'], 'PSY')
    self.assertEqual(classItem['Item']['department'], 'science')
    self.assertEqual(classItem['Item']['section'], '25')
    self.assertEqual(classItem['Item']['description'], 'How our brain works')

  def test_createMultipleClasses(self):
    print('Running createMultipleClasses test case')
    classData = {
      'title' : 'ENG',
      'department' : 'arts',
      'section' : '12',
      'description' : 'english'
    }

    classData2 = {
      'title' : 'PE',
      'department' : 'science',
      'section' : '1',
      'description' : 'physical education'
    }

    email = 'test4@mentii.me'
    userRole = 'teacher'
    class_ctrl.createClass(dynamodb, classData, email, userRole)
    class_ctrl.createClass(dynamodb, classData2, email, userRole)

    # check that teaching list was added to user
    classesTable = db.getTable('classes', dynamodb)
    usersTable = db.getTable('users', dynamodb)

    data = {'Key': {'email': email}}
    teacher = db.getItem(data, usersTable)
    self.assertTrue('Item' in teacher.keys())
    self.assertTrue('teaching' in teacher['Item'])

    teachingSet = teacher['Item']['teaching']
    self.assertEqual(len(teachingSet), 2)

    # check that classes were created in classes table
    class1Found = False
    class2Found = False
    for classCode in teachingSet:
      data = {'Key': {'code': classCode}}
      classItem = db.getItem(data, classesTable)
      self.assertTrue('Item' in classItem.keys())
      if (classItem['Item']['title'] == 'ENG' and
          classItem['Item']['department'] == 'arts' and
          classItem['Item']['section'] == '12' and
          classItem['Item']['description'] == 'english'):
        class1Found = True
      elif (classItem['Item']['title'] == 'PE' and
          classItem['Item']['department'] == 'science' and
          classItem['Item']['section'] == '1' and
          classItem['Item']['description'] == 'physical education'):
        class2Found = True

    self.assertTrue(class1Found)
    self.assertTrue(class2Found)

  def test_createClassWrongRole(self):
    print('Running creatClassWrongRole test case')
    classData = {
      'title' : 'LING',
      'department' : 'science',
      'section' : '44',
      'description' : 'Linguistics'
    }

    email = 'test2@mentii.me'
    userRole = 'student'
    response = class_ctrl.createClass(dynamodb, classData, email, userRole)
    # check response message
    self.assertTrue(response.hasErrors)

    #check that user does not have teaching list
    usersTable = db.getTable('users', dynamodb)

    data = {'Key': {'email': email}}
    teacher = db.getItem(data, usersTable)
    self.assertTrue('Item' in teacher.keys())
    self.assertFalse('teaching' in teacher['Item'])

if __name__ == '__main__':
  if __package__ is None:
    import sys
    from os import path
    sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
    from mentii import class_ctrl
  else:
    from ..mentii import class_ctrl
  unittest.main()
