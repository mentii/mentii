import unittest
import boto3
from botocore.exceptions import ClientError
import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from mentii import book_ctrl
from utils import db_utils as db

#local DynamoDB
dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')

class BookControlDBTests(unittest.TestCase):
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
    bookMockData = 'mock_book.json'

    self.booksTable = db.createTableFromFile('./tests/'+booksSetting, dynamodb)

    db.preloadBookData('./tests/'+bookMockData, self.booksTable)

  def test_createBook(self):
    print('Running createBook test case')
    bookData = {
      'title' : 'Foundations of Algebra 1',
      'description' : 'How to do algebra',
      'chapters': [
        {
          'title': 'Chapter One',
          'sections' : [
            {
              'title': 'Section One',
              'problems' : [
                {
                  'problemString' : '2x-3=9'
                },
                {
                  'problemString' : '21x*7=11'
                },
                {
                  'problemString' : '5x/12=69'
                }
              ]
            },
            {
              'title': 'Section Two',
              'problems' : [
                {
                  'problemString' : '6x-2=7'
                },
                {
                  'problemString' : '4x+9=20'
                }
              ]
            }
          ]
        },
        {
          'title': 'Chapter Two',
          'sections' : [
            {
              'title': 'Section One',
              'problems' : [
                {
                  'problemString' : '21x*11=19'
                }
              ]
            },
            {
              'title': 'Section Two',
              'problems' : [
                {
                  'problemString' : '2x-9x=7'
                }
              ]
            }
          ]
        }
      ]
    }

    # check number of books in table before creating
    scan = self.booksTable.scan()
    count = scan['Count']

    userRole = 'admin'
    response = book_ctrl.createBook(bookData, dynamodb, userRole)
    # check response message
    self.assertEqual(response.payload, {'Success': 'Book Created'})

    # check number of books in table after creating
    scan = self.booksTable.scan()
    self.assertEqual(scan['Count'] , count+1)

  def test_createBook_fail(self):
    print('Running createBook fail test case')
    userRole = 'student'
    bookData = {'title' : 'Title'}

    # check number of books in table before creating
    scan = self.booksTable.scan()
    count = scan['Count']

    response = book_ctrl.createBook(bookData, dynamodb, userRole)
    # check response message
    error = response.errors[0]
    self.assertEqual(error, {'message': 'Only admins can create books', 'title': 'Role error'})

    # check number of books in table stayed the same
    scan = self.booksTable.scan()
    self.assertEqual(scan['Count'] , count)
