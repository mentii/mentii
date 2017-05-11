import boto3
import uuid
from boto3.dynamodb.conditions import Key, Attr
from utils.ResponseCreation import ControllerResponse
from utils import db_utils as dbUtils
from flask import g
from flask import render_template
import utils.MentiiLogging as MentiiLogging
import user_ctrl as user_ctrl
from flask_mail import Message

def getActiveClassList(dynamoDBInstance, email=None):
  response = ControllerResponse()
  usersTable = dbUtils.getTable('users', dynamoDBInstance)
  classTable = dbUtils.getTable('classes', dynamoDBInstance)

  if usersTable is None or classTable is None:
    response.addError(  'Get Active Class List Failed',
                        'Unable to access users and/or classes')
  else :
    if email is None: # pragma: no cover
      email = g.authenticatedUser['email']
    classes = []
    classCodes = getClassCodesFromUser(dynamoDBInstance, email)

    for code in classCodes:
      request = {'Key': {'code': code}}
      res = dbUtils.getItem(request, classTable)
      if res is not None and 'Item' in res:
        classes.append(res['Item'])
    response.addToPayload('classes', classes)
  return response

def getClass(classCode, dynamoDBInstance, email=None, userRole=None):
  response = ControllerResponse()
  classData = getClassByCode(classCode, dynamoDBInstance)
  if not classData:
      response.addError('Get Class Failed', 'Unable to load class data')
  else:
    if g: # pragma: no cover
      email = g.authenticatedUser['email']
      userRole = g.authenticatedUser['userRole']
    #Checks that user is the teacher of the class w/ classCode
    if ((userRole == 'teacher' or userRole == 'admin')
        and classCode in getTaughtClassCodesFromUser(dynamoDBInstance, email)):
      classData['isTeacher'] = True
    #Else remove students[] from classData, if it exists, because:
    #Only the teacher of a class can get the class's students
    elif 'students' in classData:
      if email in classData.get('students', []):
        classData['isStudent'] = True
      del classData['students']
    response.addToPayload('class', classData)
  return response;

def getTaughtClassList(dynamoDBInstance, email=None):
  response = ControllerResponse()
  if email is None: # pragma: no cover
    email = g.authenticatedUser['email']
  usersTable = dbUtils.getTable('users', dynamoDBInstance)
  classTable = dbUtils.getTable('classes', dynamoDBInstance)
  if usersTable is None or classTable is None:
    response.addError(  'Get Taught Class List Failed','Unable to access users and/or classes')
  else:
    classes = []
    classCodes = getTaughtClassCodesFromUser(dynamoDBInstance, email)
    if classCodes is not None:
      for code in classCodes:
        request = {'Key': {'code': code}}
        res = dbUtils.getItem(request, classTable)
        if res is not None and 'Item' in res:
          classes.append(res['Item'])
    response.addToPayload('classes', classes)
  return response

def checkClassDataValid(classData):
  return 'title' in classData.keys() and 'description' in classData.keys()

def createClass(dynamoDBInstance, classData, email=None, userRole=None):
  response = ControllerResponse()

  #g will be not be available during testing
  #and email and userRole will need to be passed to the function
  if g: # pragma: no cover
    email = g.authenticatedUser['email']
    userRole = g.authenticatedUser['userRole']
  #role is confirmed here incase createClass is called from somewhere other
  #than app.py create_class()
  if userRole != 'teacher' and userRole != 'admin':
    response.addError('Role error', 'Only teachers can create classes')
  elif classData is None or not checkClassDataValid(classData):
    response.addError('createClass call Failed.', 'Invalid class data given.')
  else:
    classTable = dbUtils.getTable('classes', dynamoDBInstance)
    userTable = dbUtils.getTable('users', dynamoDBInstance)
    if classTable is None or userTable is None:
      response.addError('createClass call Failed.', 'Unable to locate necessary table(s).')
    else:
      classCode = str(uuid.uuid4())
      newClass = {
        'code': classCode,
        'title': classData['title'],
        'description': classData['description']
      }

      if 'department' in classData.keys() and classData['department']:
        newClass['department'] = classData['department']
      if 'section' in classData.keys() and classData['section']:
        newClass['classSection'] = classData['section']

      result = dbUtils.putItem(newClass, classTable)

      if result is None:
        response.addError('createClass call Failed.', 'Unable to create class in classes table.')
      else:
        # Note: if teaching attribute does not previously exist, a set of class codes will be created
        # otherwise, the class code will be added to the set of class codes
        codeSet = set([classCode])
        jsonData = {
          'Key': {'email': email},
          'UpdateExpression': 'ADD teaching :classCode',
          'ExpressionAttributeValues': { ':classCode': codeSet },
          'ReturnValues' : 'UPDATED_NEW'
        }
        res = dbUtils.updateItem(jsonData, userTable)
        if res is None:
          response.addError('createClass call failed', 'Unable to update user data')
        else:
          response.addToPayload('Success', 'Class Created')
  return response

def getClassByCode(classCode, dynamoDBInstance):
  classData = None
  classTable = dbUtils.getTable('classes', dynamoDBInstance)
  if not classTable:
    MentiiLogging.getLogger().error(
      'Unable to access class table in getClassByCode')
  else:
    request = {'Key': {'code': classCode}}
    res = dbUtils.getItem(request, classTable)
    if not res or 'Item' not in res:
      MentiiLogging.getLogger().error(
        'Unable to load class data in getClassByCode')
    else:
      classData = res['Item']
  return classData

def getClassCodesFromUser(dynamoDBInstance, email=None):
  classCodes = set()
  if email is None: # pragma: no cover
    email = g.authenticatedUser['email']
  usersTable = dbUtils.getTable('users', dynamoDBInstance)
  if usersTable is None:
    MentiiLogging.getLogger().error('Unable to get users table in getClassCodesFromUser')
  else:
    #An active class list is the list of class codes that
    # a user has in the user table.
    request = {"Key" : {"email": email}, "ProjectionExpression": "classCodes"}
    res = dbUtils.getItem(request, usersTable)
    #Get the class codes for the user.
    if res is None or 'Item' not in res or 'classCodes' not in res['Item']:
      MentiiLogging.getLogger().error('Unable to get user data in getClassCodesFromUser')
    else:
      classCodes = res['Item']['classCodes']
  return classCodes

def getTaughtClassCodesFromUser(dynamoDBInstance, email=None):
  classCodes = None
  if email is None: # pragma: no cover
    email = g.authenticatedUser['email']
  usersTable = dbUtils.getTable('users', dynamoDBInstance)
  if usersTable is None:
    MentiiLogging.getLogger().error('Unable to get users table in getTaughtClassCodesFromUser')
  else:
    #An active class list is the list of class codes that
    # a user has in the user table.
    request = {'Key' : {'email': email}, 'ProjectionExpression': 'teaching'}
    res = dbUtils.getItem(request, usersTable)
    #Get the class codes for the user.
    if res is not None and 'Item' in res:
      classCodes = res['Item'].get('teaching', [])
  return classCodes

def getPublicClassList(dynamodb, email=None):
  response = ControllerResponse()
  classCodes = getClassCodesFromUser(dynamodb, email)
  classes = []
  classesTable = dbUtils.getTable('classes', dynamodb)
  if classesTable is None:
    MentiiLogging.getLogger().error('Unable to get classes table in getPublicClassList')
    response.addError('Failed to get class list', 'A database error occured')
  else:
    res = classesTable.scan()
    for pclass in res.get('Items', []):
      if pclass['code'] not in classCodes and 'private' not in pclass and pclass.get('private') != True:
        classes.append(pclass)
    response.addToPayload('classes', classes)
  return response

def removeStudent(dynamoDBInstance, jsonData, response=None, userRole=None):
  currentUserEmail = None
  if response is None:
    response = ControllerResponse()
  email = jsonData.get('email')
  classCode = jsonData.get('classCode')
  if g:
    userRole = g.authenticatedUser['userRole']
    currentUserEmail = g.authenticatedUser['email']
  if not (userRole == 'teacher' or userRole == 'admin' or currentUserEmail == email):
    response.addError('Role error', 'Only those with teacher privileges can remove students from classes')
  elif email is None or classCode is None:
    response.addError('Failed to remove student from class', 'Invalid data given')
  else:
    removeClassFromStudent(dynamoDBInstance, response, email, classCode)
    if not response.hasErrors():
      removeStudentFromClass(dynamoDBInstance, response, email, classCode)
  return response

def buildUpdateJsonData(keyName, keyValue, attributeName, attributeValue):
  jsonData = {}
  if len(attributeValue) == 0:
    #remove attribute
    jsonData = {
      'Key': {keyName : keyValue},
      'UpdateExpression': 'REMOVE '+ attributeName,
      'ReturnValues' : 'UPDATED_NEW'
    }
  else:
    #update attribute
    jsonData = {
      'Key': {keyName : keyValue},
      'UpdateExpression': 'SET ' + attributeName + ' = :v',
      'ExpressionAttributeValues': { ':v': attributeValue },
      'ReturnValues' : 'UPDATED_NEW'
    }
  return jsonData

def removeClassFromStudent(dynamoDBInstance, response, email, classCode):
  usersTable = dbUtils.getTable('users', dynamoDBInstance)
  if usersTable is None:
    MentiiLogging.getLogger().error('Unable to get users table in removeStudentFromClass')
    response.addError('Remove Student From Class Failed.', 'Unable to locate necessary table(s).')
  else:
    # check that user exists and user has that class
    user = user_ctrl.getUserByEmail(email, dynamoDBInstance)
    if user is None:
      MentiiLogging.getLogger().error('Unable to get user by email in removeStudentFromClass')
      response.addError('Failed to remove student from class', 'Unable to find user')
    else:
      classCodes = user['classCodes'] #set
      if classCode not in classCodes:
        response.addError('Failed to remove class from student', 'Class not found')
      else:
        classCodes.remove(classCode)
        jsonData = buildUpdateJsonData('email', email, 'classCodes', classCodes)
        res = dbUtils.updateItem( jsonData, usersTable)
        if res is None:
          MentiiLogging.getLogger().error('Unable to update classes in removeStudentFromClass')
          response.addError('Failed to remove student from class', 'Unable to update user data')
        else:
          MentiiLogging.getLogger().info('Class removal success. Removed class from student')
  return response

def undoClassCodeRemoval(dynamoDBInstance, email, classCode):
  # add classCode back to student if there was an error removing student from class
  usersTable = dbUtils.getTable('users', dynamoDBInstance)
  user = user_ctrl.getUserByEmail(email, dynamoDBInstance)
  jsonData = {}
  # if the classCodes attribute was removed, add the attribute
  if user.get('classCodes') is None:
    user_ctrl.addClassCodeToStudent(email, classCode, dynamoDBInstance)
  # update classCodes attribute
  else:
    classes = user.get('classCodes') #set
    classes.add(classCode)
    #update item
    jsonData = {
      'Key': {'email': email},
      'UpdateExpression': 'SET classCodes = :cc',
      'ExpressionAttributeValues': { ':cc': classes },
      'ReturnValues' : 'UPDATED_NEW'
    }
  dbUtils.updateItem(jsonData, usersTable)

def removeStudentFromClass(dynamoDBInstance, response, email, classCode):
  classesTable = dbUtils.getTable('classes', dynamoDBInstance)
  if classesTable is None:
    MentiiLogging.getLogger().error('Unable to get classes table in removeStudentFromClass')
    response.addError('Remove Student From Class Failed.', 'Unable to locate necessary table(s).')
  else:
    # check that class exists and class has that user
    cl = getClassByCode(classCode, dynamoDBInstance)
    if cl is None:
      MentiiLogging.getLogger().error('Unable to get class by classCode in removeStudentFromClass')
      response.addError('Failed to remove student from class', 'Unable to get class')
    else:
      students = cl['students'] #set
      if email not in students:
        response.addError('Failed to remove student from class', 'Student not found')
      else:
        students.remove(email)
        jsonData = buildUpdateJsonData('code', classCode, 'students', students)
        res = dbUtils.updateItem(jsonData, classesTable)
        if res is None:
          MentiiLogging.getLogger().error('Unable to update classes in removeStudentFromClass')
          response.addError('Failed to remove student from class', 'Unable to update classes data')
        if response.hasErrors():
          undoClassCodeRemoval(dynamoDBInstance, email, classCode)
        else:
          MentiiLogging.getLogger().info('Student removal success. Removed student from class')
  return response

def sendClassRemovalEmail(dynamoDBInstance, mailer, jsonData):
  '''
  Create a message to send it from our email to
  the passed in email. The message should notify the user they were removed from a class
  '''
  email = jsonData.get('email')
  classCode = jsonData.get('classCode')
  cl = getClassByCode(classCode, dynamoDBInstance)
  classTitle = cl['title']
  message = render_template('removedEmail.html', classTitle=classTitle)

  #Build Message
  msg = Message('You have been removed from a class', recipients=[email],
        extra_headers={'Content-Transfer-Encoding': 'quoted-printable'}, html=message)

  mailer.send(msg)

def updateClassDetails(jsonData, dynamodb, email=None, userRole=None):
  response = ControllerResponse()
  classesTable = dbUtils.getTable('classes', dynamodb)

  if classesTable is None:
    MentiiLogging.getLogger().error('Unable to get classes table in getPublicClassList')
    response.addError('Failed to get class list', 'A database error occured');
  else:
    # get data from request body
    code = jsonData.get('code')
    title = jsonData.get('title')
    desc = jsonData.get('description')
    dept = jsonData.get('department') # optional
    sec = jsonData.get('section') # optional

    if g: # pragma: no cover
      email = g.authenticatedUser['email']
      userRole = g.authenticatedUser['userRole']
    #check if teacher is teacher of the class
    if ((userRole == 'teacher' or userRole == 'admin')
      and code in getTaughtClassCodesFromUser(dynamodb, email)):

      updateExprString = 'SET title =:t, description =:dn'
      expresionAttrDict = { ':t': title, ':dn' : desc }

      removeString = ''
      # if empty string is given, remove the attribute
      if dept == '' and sec == '':
        removeString = removeString + ' REMOVE department, classSection'
      else:
        if dept == '':
          removeString = removeString + ' REMOVE department'
        else:
          updateExprString = updateExprString + ', department = :dt'
          expresionAttrDict[':dt'] = dept
        if sec == '':
          removeString = removeString + ' REMOVE classSection'
        else:
          updateExprString = updateExprString + ', classSection = :s'
          expresionAttrDict[':s'] = sec

      updateExprString = updateExprString + removeString

      # update item
      updateData = {
            'Key': {'code': code},
            'UpdateExpression': updateExprString,
            'ExpressionAttributeValues': expresionAttrDict,
            'ReturnValues' : 'UPDATED_NEW'
      }

      res = dbUtils.updateItem(updateData, classesTable)
      if res is None:
        response.addError('updateClassDetails has error', 'Unable to update class details')
      else:
        response.addToPayload('Success', 'Class Details Updated')
    else:
      response.addError('Teacher permissions incorrect', 'Unable to update class details')
  return response
