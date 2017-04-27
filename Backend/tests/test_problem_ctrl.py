import unittest
import sys
import boto3
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from mentii import problem_ctrl
from mentii import book_ctrl
from utils import db_utils as db

#local DynamoDB
dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')

class ProblemCtrlTests(unittest.TestCase):
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

    booksSetting = 'book_settings.json'
    classSetting = 'classes_settings.json'
    bookMockData = 'mock_book.json'
    classesMockData = 'mock_classes.json'

    self.booksTable = db.createTableFromFile('./tests/'+booksSetting, dynamodb)
    self.classesTable = db.createTableFromFile('./tests/'+classSetting, dynamodb)

    db.preloadBookData('./tests/'+bookMockData, self.booksTable)
    db.preloadClassData('./tests/'+classesMockData, self.classesTable)

  def test_getProblemFromBook(self):
    bookId = 'd6742cc-f02d-4fd6-80f0-026784g1ab9b'
    chapterTitle = 'Chapter 1'
    sectionTitle = 'Section 2'
    user = 'new@User.com'
    index, problem = problem_ctrl.getProblemFromBook(bookId, chapterTitle, sectionTitle, user, dynamodb)
    self.assertNotEqual(problem, 'Bad Problem') #Problem is a random problem. can't hard code it. 

  def test_getBookInfoFromActivity(self):
    classId = 'd26713cc-f02d-4fd6-80f0-026784d1ab9b'
    activityTitle = 'Week 1' 
    bookId, chapterTitle, sectionTitle = problem_ctrl.getBookInfoFromActivity(classId, activityTitle, dynamodb)
    self.assertEqual(bookId, 'd6742cc-f02d-4fd6-80f0-026784g1ab9b')
    self.assertEqual(chapterTitle,'Chapter 1')
    self.assertEqual(sectionTitle, 'Section 2')

  def test_chooseProblemTemplate(self):
    templateList = [{'problemString':'a'}, {'problemString': 'b'}, {'problemString': 'c'}, {'problemString': 'd'}]
    userHistoryList = [0, -1, 3, 0]
    index, template = problem_ctrl.chooseProblemTemplate(templateList, userHistoryList)
    
    self.assertTrue(template != 'Bad Problem')
    self.assertTrue(index < len(templateList))
    
    templateList = []
    userHistoryList = [0, -1, 3, 0]
    index, template = problem_ctrl.chooseProblemTemplate(templateList, userHistoryList)
    
    self.assertTrue(template == 'Bad Problem')

  def test_updateUserTemplateHistory(self):
    classId = 'd26713cc-f02d-4fd6-80f0-026784d1ab9b'
    activityTitle = 'Week 1' 
    userId = 'test@mentii.me'
    index = 1
    didSucceed = True
    res = problem_ctrl.updateUserTemplateHistory(classId, activityTitle, userId, index, didSucceed, dynamodb)
    self.assertTrue(not res.hasErrors())

    didSucceed = False
    res = problem_ctrl.updateUserTemplateHistory(classId, activityTitle, userId, index, didSucceed, dynamodb)
    self.assertTrue(not res.hasErrors())

if __name__ == '__main__':
  if __package__ is None:
    import sys
    from os import path
    sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
    from problems import mathstepsWrapper
  else:
    from ..problems import mathstepsWrapper
  unittest.main()
