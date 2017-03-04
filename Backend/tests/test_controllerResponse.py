import unittest
import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from utils.ResponseCreation import *

class ControllerResponseTests(unittest.TestCase):
  @classmethod
  def setUp(self):
    self.response = ControllerResponse()

  def test_addError(self):
    print('Running addError test case')
    response = self.response
    testMessage = 'testing error'
    testTitle = 'Test'
    #Check that there are no errors on a new object
    self.assertEqual(len(response.errors), 0)
    #Check that when you add an error the response has it.
    response.addError(testTitle, testMessage)
    self.assertEqual(len(response.errors), 1)
    self.assertEqual(response.errors[0]['title'], testTitle)
    self.assertEqual(response.errors[0]['message'], testMessage)

  def test_addToPayload(self):
    print('Running addToPayload test case')
    response = self.response
    testValue = 'testing data'
    testAttribute = 'Test'
    #Check that there are no errors on a new object
    self.assertEqual(len(response.payload), 0)
    #Check that when you add an error the response has it.
    response.addToPayload(testAttribute, testValue)
    self.assertEqual(len(response.payload), 1)
    self.assertEqual(response.payload[testAttribute], testValue)

  def test_hasErrors(self):
    print('Running hasErrors test case')
    response = self.response
    #test that has errors is not true until an error is added
    testValue = 'testing data'
    testAttribute = 'Test'
    self.assertEqual(response.hasErrors(), False)
    response.addToPayload(testAttribute, testValue)
    self.assertEqual(response.hasErrors(), False)
    response.addError('Error', 'Error message')
    self.assertEqual(response.hasErrors(), True)

  def test_prepForJsonDump(self):
    print('Running prepForJsonDump test case')
    testDict = {'one' : 1}
    cleaned = self.response.prepForJsonDump(testDict)
    self.assertEqual(cleaned, testDict)

    testTuple = ('test', 'test')
    cleaned = self.response.prepForJsonDump(testTuple)
    self.assertTrue(isinstance(cleaned, list))

    testSet = set(['test', 'test'])
    cleaned = self.response.prepForJsonDump(testSet)
    self.assertTrue(isinstance(cleaned, list))

    testList = ['one', 2]
    cleaned = self.response.prepForJsonDump(testList)
    self.assertEqual(cleaned, testList)

    testList.append(testTuple)
    testList.append(testSet)
    cleaned = self.response.prepForJsonDump(testList)
    self.assertTrue(isinstance(cleaned, list))
    self.assertEqual(len(cleaned), 4)
    self.assertTrue(isinstance(cleaned[2], list))
    self.assertTrue(isinstance(cleaned[3], list))

    testDict['list'] = testList
    cleaned = self.response.prepForJsonDump(testDict)
    self.assertTrue(isinstance(cleaned, dict))
    self.assertTrue(isinstance(cleaned['list'], list))
    self.assertEqual(len(cleaned['list']), 4)
    self.assertTrue(isinstance(cleaned['list'][2], list))
    self.assertTrue(isinstance(cleaned['list'][3], list))

  def test_updateUserRole(self):
    print('Running updateUserRole test case')
    #setup fake response object
    response = self.response
    response.user['userRole'] = 'student'
    self.assertEqual(response.user['userRole'], 'student')

    response.updateUserRole('admin')
    self.assertEqual(response.user['userRole'], 'admin')

  def test_getResponseString(self):
    response = self.response
    # setup test response object that would be seen in production
    classes = {'abcd', 'efg'}
    email = 'test@mentii.me'
    role = 'teacher'
    errorMessage = 'Error message'
    payloadMessage = 'World'

    response.addToPayload('hello', payloadMessage)
    response.addToPayload('classes', classes)
    response.addError('error1', errorMessage)
    response.user['userRole'] = role
    response.user['email'] = email

    responseString = response.getResponseString()
    solutionString = ('{"errors": [{"message": "Error message", "title": "error1"}], '
                      '"user": {"userRole": "teacher", "email": "test@mentii.me"}, '
                      '"payload": {"classes": ["abcd", "efg"], "hello": "World"}}')

    self.assertEqual(responseString,solutionString)

if __name__ == '__main__':
  unittest.main()
