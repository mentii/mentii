import unittest
from mock import MagicMock

import boto3
from botocore.exceptions import ClientError
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
    self.assertIsNotNone(response)

  def test_getTaughtClassList(self):
    print('Running getTaughtClassList test case')
    user =  'test5@mentii.me'
    response = class_ctrl.getTaughtClassList(dynamodb, user)
    self.assertIsNotNone(response)

  def test_getPublicClassList(self):
    print('Running getPublicClassList test case')
    user =  'test@mentii.me'
    response = class_ctrl.getPublicClassList(dynamodb, user)
    self.assertIsNotNone(response)

  def test_getClassCodesFromUser(self):
    print('Running getClassCodesFromUser test case')
    user =  'test@mentii.me'
    response = class_ctrl.getClassCodesFromUser(dynamodb, user)
    self.assertIsNotNone(response, None)
    self.assertTrue(len(response) == 3)

  def test_getTaughtClassCodesFromUser(self):
    print('Running getTaughtClassCodesFromUser test case')
    user =  'test5@mentii.me'
    response = class_ctrl.getTaughtClassCodesFromUser(dynamodb, user)
    self.assertIsNone(response)

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
    self.assertTrue('Item' in teacher.keys())
    self.assertTrue('teaching' in teacher['Item'])

    teachingList = list(teacher['Item']['teaching'])

    # check that class was created in classes table
    classCode = str(teachingList[0])
    data = {'Key': {'code': classCode}}
    classItem = db.getItem(data, classesTable)
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

  def test_getClass(self):
    realGetClassByCode = class_ctrl.getClassByCode
    realGetTaughtClassCodesFromUser = class_ctrl.getTaughtClassCodesFromUser

    #test None returned by getClassByCode
    class_ctrl.getClassByCode = MagicMock(return_value = None)
    res = class_ctrl.getClass('code', None)
    self.assertTrue(res.hasErrors())

    #test get class by student (no students or isTeacher returned)
    data = { 'students': ['aaron'], 'title': 'fakeClass' }
    class_ctrl.getClassByCode = MagicMock(return_value = data)
    res = class_ctrl.getClass('code', None, 'email', 'student')
    self.assertFalse(res.hasErrors())
    self.assertFalse('students' in res.payload['class'])
    self.assertFalse('isTeacher' in res.payload['class'])
    self.assertTrue('title' in res.payload['class'])

    #test get class by teacher, who does not teach class (no students or isTeacher returned)
    data = { 'students': ['aaron'], 'title': 'fakeClass' }
    class_ctrl.getClassByCode = MagicMock(return_value = data)
    class_ctrl.getTaughtClassCodesFromUser = MagicMock(
        return_value = ['other_code'])
    res = class_ctrl.getClass('code', None, 'email', 'teacher')
    self.assertFalse(res.hasErrors())
    self.assertFalse('students' in res.payload['class'])
    self.assertFalse('isTeacher' in res.payload['class'])
    self.assertTrue('title' in res.payload['class'])

    #test get class by admin, who does not teach class (no students or isTeacher returned)
    data = { 'students': ['aaron'], 'title': 'fakeClass' }
    class_ctrl.getClassByCode = MagicMock(return_value = data)
    res = class_ctrl.getClass('code', None, 'email', 'admin')
    self.assertFalse(res.hasErrors())
    self.assertFalse('students' in res.payload['class'])
    self.assertFalse('isTeacher' in res.payload['class'])
    self.assertTrue('title' in res.payload['class'])

    #test get class by teacher who teaches class (students and isTeacher returned)
    data = { 'students': ['aaron'], 'title': 'fakeClass' }
    class_ctrl.getClassByCode = MagicMock(return_value = data)
    class_ctrl.getTaughtClassCodesFromUser = MagicMock(return_value = ['code'])
    res = class_ctrl.getClass('code', None, 'email', 'teacher')
    self.assertFalse(res.hasErrors())
    self.assertTrue('students' in res.payload['class'])
    self.assertTrue('isTeacher' in res.payload['class'])
    self.assertTrue('title' in res.payload['class'])

    #test get class by admin who teaches class (students and isTeacher returned)
    data = { 'students': ['aaron'], 'title': 'fakeClass' }
    class_ctrl.getClassByCode = MagicMock(return_value = data)
    class_ctrl.getTaughtClassCodesFromUser = MagicMock(return_value = ['code'])
    res = class_ctrl.getClass('code', None, 'email', 'admin')
    self.assertFalse(res.hasErrors())
    self.assertTrue('students' in res.payload['class'])
    self.assertTrue('isTeacher' in res.payload['class'])
    self.assertTrue('title' in res.payload['class'])

    #resetting mocked functions
    class_ctrl.getClassByCode = realGetClassByCode
    class_ctrl.getTaughtClassCodesFromUser = realGetTaughtClassCodesFromUser

  def test_getClassByCode(self):
    #ClientError getting table, None returned by getTable
    mockDBInstance = MagicMock()
    mockDBInstance.Table.side_effect = ClientError({'Error': {}}, 'error')
    res = class_ctrl.getClassByCode('code', mockDBInstance)
    mockDBInstance.Table.assert_called_once()
    self.assertIsNone(res)

    #getItem returns None
    mockTable = MagicMock()
    mockTable.get_item = MagicMock(return_value = None)
    mockDBInstance = MagicMock()
    mockDBInstance.Table = MagicMock(return_value = mockTable)
    res = class_ctrl.getClassByCode('code', mockDBInstance)
    mockTable.get_item.assert_called_once()
    mockDBInstance.Table.assert_called_once()
    self.assertIsNone(res)

    #getItem return is missing 'Item'
    mockTable = MagicMock()
    mockTable.get_item = MagicMock(return_value = {'notItem' : 'notHere'})
    mockDBInstance = MagicMock()
    mockDBInstance.Table = MagicMock(return_value = mockTable)
    res = class_ctrl.getClassByCode('code', mockDBInstance)
    mockTable.get_item.assert_called_once()
    mockDBInstance.Table.assert_called_once()
    self.assertIsNone(res)

    #Successful
    classData = 'classData'
    mockTable = MagicMock()
    mockTable.get_item = MagicMock(return_value = {'Item' : classData})
    mockDBInstance = MagicMock()
    mockDBInstance.Table = MagicMock(return_value = mockTable)
    res = class_ctrl.getClassByCode('code123', mockDBInstance)
    mockTable.get_item.assert_called_once()
    mockDBInstance.Table.assert_called_once()
    mockTable.get_item.assert_called_with(Key={'code': 'code123'})
    self.assertEqual(res, classData)

  def test_updateClassDetails(self):
    print('Running updateClassDetails test')

    classesTable = db.getTable('classes', dynamodb)

    # put data into db first
    beforeData = {
      'title': 'before update title',
      'department': 'before update department',
      'description': 'before update description',
      'section': 'before update section',
      'code': 'before update code'
    }

    db.putItem(beforeData, classesTable)

    # check item was placed successfully
    code = {'Key': {'code': 'before update code'}}
    c = db.getItem(code, classesTable)
    self.assertTrue('Item' in c.keys())

    # update class details
    afterData = {
      'title': 'after update title',
      'department': 'after update department',
      'description': 'after update description',
      'section': 'after update section',
      'code': 'before update code'
    }

    response = class_ctrl.updateClassDetails(afterData, dynamodb)
    self.assertEqual(response.payload, {'Success': 'Class Details Updated'})
    c = db.getItem(code, classesTable)
    self.assertTrue('Item' in c.keys())
    self.assertEqual(c['Item']['title'], 'after update title')
    self.assertEqual(c['Item']['department'], 'after update department')
    self.assertEqual(c['Item']['section'], 'after update section')
    self.assertEqual(c['Item']['description'], 'after update description')


if __name__ == '__main__':
  if __package__ is None:
    import sys
    from os import path
    sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
    from mentii import class_ctrl
  else:
    from ..mentii import class_ctrl
  unittest.main()
