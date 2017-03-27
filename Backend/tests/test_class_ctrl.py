import unittest
from mock import MagicMock

import boto3
from botocore.exceptions import ClientError
import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from mentii import class_ctrl
from utils import db_utils as db
import utils.ResponseCreation as ResponseCreation

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

  ########################## Remove Student Test Cases #################################

  def test_removeStudent(self):
    print('Running removeStudent test case')

    userRole = 'admin'
    email = 'remove@user.me'
    classCode = 'f24613dc-f09d-4fd6-81f1-026784d6cc9b'

    #Put user and class data into DB
    usersTable = db.getTable('users', dynamodb)
    classesTable = db.getTable('classes', dynamodb)

    userJsonData = {
      'email' : email,
      'classCodes' : [classCode]
    }

    classJsonData = {
      'code' : classCode,
      'students' : [email]
    }

    db.putItem(userJsonData, usersTable)
    db.putItem(classJsonData, classesTable)

    #Check test data was successfully placed into DB
    jsonData = {'Key':{'email':email}}
    response = db.getItem(jsonData, usersTable)
    self.assertIsNotNone(response.get('Item'))
    self.assertEqual(response.get('Item').get('email'), email)

    jsonData = {'Key':{'code':classCode}}
    response = db.getItem(jsonData, classesTable)
    self.assertIsNotNone(response.get('Item'))
    self.assertEqual(response.get('Item').get('code'), classCode)

    #Test removal
    jsonData = {
      'email': email,
      'classCode':classCode
    }
    res = class_ctrl.removeStudent(dynamodb, jsonData, userRole)
    self.assertFalse(res.hasErrors())
    self.assertTrue('Class removal success' in res.payload)
    self.assertTrue('Student removal success' in res.payload)

  def test_removeStudent_role_fail(self):
    print('Running removeStudent role fail test case')

    userRole = 'janitor'
    email = 'remove@user.me'
    classCode = 'f24613dc-f09d-4fd6-81f1-026784d6cc9b'

    #Test removal
    jsonData = {
      'email': email,
      'classCode':classCode
    }
    res = class_ctrl.removeStudent(dynamodb, jsonData, userRole)
    self.assertTrue(res.hasErrors())
    self.assertEqual(res.errors[0], {'message': 'Only those with teacher privileges can remove students from classes', 'title': 'Role error'})

  def test_removeStudent_data_fail(self):
    print('Running removeStudent data fail test case')

    userRole = 'admin'
    email = 'remove2@user.me'
    classCode = 'f15708db-fb9d-4fd6-81f1-026784d6cc9b'

    #Put user and class data into DB
    usersTable = db.getTable('users', dynamodb)
    classesTable = db.getTable('classes', dynamodb)

    userJsonData = {
      'email' : email,
      'classCodes' : [classCode]
    }

    classJsonData = {
      'code' : classCode,
      'students' : [email]
    }

    db.putItem(userJsonData, usersTable)
    db.putItem(classJsonData, classesTable)

    #Check test data was successfully placed into DB
    jsonData = {'Key':{'email':email}}
    response = db.getItem(jsonData, usersTable)
    self.assertIsNotNone(response.get('Item'))
    self.assertEqual(response.get('Item').get('email'), email)

    jsonData = {'Key':{'code':classCode}}
    response = db.getItem(jsonData, classesTable)
    self.assertIsNotNone(response.get('Item'))
    self.assertEqual(response.get('Item').get('code'), classCode)

    #Test bad class code
    jsonData = {
      'email': email,
      'classCode':'f24abcdc-f09d-4fd6-81f1-026784d6cc9b'
    }
    res = class_ctrl.removeStudent(dynamodb, jsonData, userRole)
    self.assertTrue(res.hasErrors())
    self.assertEqual(res.errors[0], {'message': 'Class not found', 'title': 'Failed to remove class from student'})

    #check student wasn't removed from class
    jsonData = {'Key':{'code':classCode}}
    response = db.getItem(jsonData, classesTable)
    self.assertIsNotNone(response.get('Item'))
    students = response.get('Item').get('students')
    self.assertTrue(email in students)


    #Test bad email
    jsonData = {
      'email': 'bad@user.me',
      'classCode':classCode
    }
    res = class_ctrl.removeStudent(dynamodb, jsonData, userRole)
    self.assertTrue(res.hasErrors())
    self.assertEqual(res.errors[0], {'message': 'Unable to find user', 'title': 'Failed to remove student from class'})

    #check class wasn't removed from student
    jsonData = {'Key':{'email':email}}
    response = db.getItem(jsonData, usersTable)
    self.assertIsNotNone(response.get('Item'))
    classCodes = response.get('Item').get('classCodes')
    self.assertTrue(classCode in classCodes)

  ##### REMOVE CLASS FROM STUDENT TEST CASES #####
  def test_removeClassFromStudent_len_zero(self):
    print('Running removeClassFromStudent students length is zero test case')

    userRole = 'admin'
    email = 'remove8@user.me'
    classCode = 'f84138db-fb9d-4fd6-81f1-026784d6cc9b'
    res = ResponseCreation.ControllerResponse()

    #Put user and class data into DB
    usersTable = db.getTable('users', dynamodb)

    userJsonData = {
      'email' : email,
      'classCodes' : [classCode]
    }

    db.putItem(userJsonData, usersTable)

    # Check test data was successfully placed into DB
    jsonData = {'Key':{'email':email}}
    response = db.getItem(jsonData, usersTable)
    self.assertIsNotNone(response.get('Item'))
    self.assertEqual(response.get('Item').get('email'), email)

    class_ctrl.removeClassFromStudent(dynamodb, res, email, classCode)

    # Check that the attribute was removed from the student
    jsonData = {'Key':{'email':email}}
    response = db.getItem(jsonData, usersTable)
    self.assertIsNotNone(response.get('Item'))
    self.assertIsNone(response.get('Item').get('classCodes'))

  def test_removeClassFromStudent(self):
    print('Running removeClassFromStudent test case')

    userRole = 'admin'
    email = 'remove23@user.me'
    classCode = 'f77668db-fb9d-4fd6-81f1-026784d6cc9b'
    classCode2 = 'e00045db-fb9d-4fd6-81f1-026784d6cc9b'
    res = ResponseCreation.ControllerResponse()

    # Put user and class data into DB
    usersTable = db.getTable('users', dynamodb)

    userJsonData = {
      'email' : email,
      'classCodes' : [classCode, classCode2]
    }

    db.putItem(userJsonData, usersTable)

    # Check test data was successfully placed into DB
    jsonData = {'Key':{'email':email}}
    response = db.getItem(jsonData, usersTable)
    self.assertIsNotNone(response.get('Item'))
    self.assertEqual(response.get('Item').get('email'), email)

    class_ctrl.removeClassFromStudent(dynamodb, res, email, classCode2)

    # Check that the classCode was removed from the student
    jsonData = {'Key':{'email':email}}
    response = db.getItem(jsonData, usersTable)
    self.assertIsNotNone(response.get('Item'))
    cc = response.get('Item').get('classCodes')
    self.assertFalse(classCode2 in cc)
    self.assertTrue(classCode in cc)

  ##### REMOVE STUDENT FROM CLASS TEST CASES #####
  def test_removeStudentFromClass_simulated_error(self):
    print('Running removeStudentFromClass simulated error test case')

    userRole = 'admin'
    email = 'remove3@user.me'
    classCode = 'f99998db-fb9d-4fd6-81f1-026784d6cc9b'
    classCode2 = 'f00000db-fb9d-4fd6-81f1-026784d6cc9b'
    res = ResponseCreation.ControllerResponse()
    res.hasError = True

    #Put user and class data into DB
    usersTable = db.getTable('users', dynamodb)
    classesTable = db.getTable('classes', dynamodb)

    ### to simulate class already removed from student ###
    userJsonData = {
      'email' : email
    }

    classJsonData = {
      'code' : classCode,
      'students' : [email]
    }

    db.putItem(userJsonData, usersTable)
    db.putItem(classJsonData, classesTable)

    #Check test data was successfully placed into DB
    jsonData = {'Key':{'email':email}}
    response = db.getItem(jsonData, usersTable)
    self.assertIsNotNone(response.get('Item'))
    self.assertEqual(response.get('Item').get('email'), email)

    jsonData = {'Key':{'code':classCode}}
    response = db.getItem(jsonData, classesTable)
    self.assertIsNotNone(response.get('Item'))
    self.assertEqual(response.get('Item').get('code'), classCode)

    #Test simulated error in removeStudentFromClass email
    class_ctrl.removeStudentFromClass(dynamodb, res, email, classCode)

    #check class was place back into student's classCodes
    jsonData = {'Key':{'email':email}}
    response = db.getItem(jsonData, usersTable)
    self.assertIsNotNone(response.get('Item'))
    classCodes = response.get('Item').get('classCodes')
    self.assertTrue(classCode in classCodes)

    #### add back to a list that when removed will still have elements ###
    userJsonData = {
      'email' : email,
      'classCodes' :[classCode, classCode2]
    }
    db.putItem(userJsonData, usersTable)
    #Check test data was successfully placed into DB
    jsonData = {'Key':{'email':email}}
    response = db.getItem(jsonData, usersTable)
    self.assertIsNotNone(response.get('Item'))
    self.assertEqual(response.get('Item').get('email'), email)

    #Test simulated error in removeStudentFromClass email
    class_ctrl.removeStudentFromClass(dynamodb, res, email, classCode2)

    #check class was place back into student's classCodes
    jsonData = {'Key':{'email':email}}
    response = db.getItem(jsonData, usersTable)
    self.assertIsNotNone(response.get('Item'))
    classCodes = response.get('Item').get('classCodes')
    self.assertTrue(classCode in classCodes)
    self.assertTrue(classCode2 in classCodes)

  def test_removeStudentFromClass_len_zero(self):
    print('Running removeStudentFromClass students length is zero test case')

    userRole = 'admin'
    email = 'remove4@user.me'
    classCode = 'f77998db-fb9d-4fd6-81f1-026784d6cc9b'
    res = ResponseCreation.ControllerResponse()

    #Put user and class data into DB
    classesTable = db.getTable('classes', dynamodb)

    classJsonData = {
      'code' : classCode,
      'students' : [email]
    }

    db.putItem(classJsonData, classesTable)

    #Check test data was successfully placed into DB
    jsonData = {'Key':{'code':classCode}}
    response = db.getItem(jsonData, classesTable)
    self.assertIsNotNone(response.get('Item'))
    self.assertEqual(response.get('Item').get('code'), classCode)

    class_ctrl.removeStudentFromClass(dynamodb, res, email, classCode)

    #check that the attribute was removed from the class
    jsonData = {'Key':{'code':classCode}}
    response = db.getItem(jsonData, classesTable)
    self.assertIsNotNone(response.get('Item'))
    self.assertIsNone(response.get('Item').get('students'))

  def test_removeStudentFromClasss(self):
    print('Running removeStudentFromClass test case')

    userRole = 'admin'
    email1 = 'remove@user.me1'
    email2 = 'remove@user.me2'
    classCode = 'f77668db-fb9d-4fd6-81f1-026784d6cc9b'
    res = ResponseCreation.ControllerResponse()

    #Put user and class data into DB
    classesTable = db.getTable('classes', dynamodb)

    classJsonData = {
      'code' : classCode,
      'students' : [email1, email2]
    }

    db.putItem(classJsonData, classesTable)

    #Check test data was successfully placed into DB
    jsonData = {'Key':{'code':classCode}}
    response = db.getItem(jsonData, classesTable)
    self.assertIsNotNone(response.get('Item'))
    self.assertEqual(response.get('Item').get('code'), classCode)

    class_ctrl.removeStudentFromClass(dynamodb, res, email1, classCode)

    #check that the student was removed from the class
    jsonData = {'Key':{'code':classCode}}
    response = db.getItem(jsonData, classesTable)
    self.assertIsNotNone(response.get('Item'))
    stu = response.get('Item').get('students')
    self.assertFalse(email1 in stu)
    self.assertTrue(email2 in stu)

if __name__ == '__main__':
  if __package__ is None:
    import sys
    from os import path
    sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
    from mentii import class_ctrl
  else:
    from ..mentii import class_ctrl
  unittest.main()
