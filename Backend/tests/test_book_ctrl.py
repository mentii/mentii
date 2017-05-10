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

    #check that if no chapters are given, an empty chapters array is given
    bookData = {'description' : 'so many books', 'title' : 'books galore'}

    response = book_ctrl.createBook(bookData, dynamodb, userRole)
    self.assertFalse(response.hasErrors())
    res = db.scanFilter('title','books galore', self.booksTable)
    self.assertEqual(res.get('Items')[0].get('chapters'), [])

  def test_createBook_role_fail(self):
    print('Running createBook role fail test case')
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

  def test_createBook_data_fail(self):
    print('Running createBook data fail test case')
    userRole = 'admin'
    bookData = {'title' : 'missing description', 'chapters' : []}

    # check number of books in table before creating
    scan = self.booksTable.scan()
    count = scan['Count']

    response = book_ctrl.createBook(bookData, dynamodb, userRole)
    # check response message
    error = response.errors[0]
    self.assertEqual(error, {'message': 'Invalid book data given.', 'title': 'Book creation failed.'})

    # check number of books in table stayed the same
    scan = self.booksTable.scan()
    self.assertEqual(scan['Count'] , count)

    bookData = {'description' : 'missing title', 'chapters' : []}

    response = book_ctrl.createBook(bookData, dynamodb, userRole)
    # check response message
    error = response.errors[0]
    self.assertEqual(error, {'message': 'Invalid book data given.', 'title': 'Book creation failed.'})

    # check number of books in table stayed the same
    scan = self.booksTable.scan()
    self.assertEqual(scan['Count'] , count)

  def test_getBook(self):
    bookId = 'd6742cc-f02d-4fd6-80f0-026784g1ab9b'
    badBook = 'foobar'
    book = book_ctrl.getBook(bookId, dynamodb)
    self.assertEqual(book.get('bookId'), bookId)
    book = book_ctrl.getBook(badBook, dynamodb)
    self.assertIsNone(book)

  def test_editBook(self):
    print('Running editBook test case')
    bookData = {
      'title' : 'Foundations of Algebra 1',
      'description' : 'How to do algebra',
      'bookId' :  'd6742cc-f02d-4fd6-80f0-026784g1ab9b',
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
            }
          ]
        }
      ]
    }

    #Edit the existing book
    book_ctrl.editBook(bookData, dynamodb)
    bookId = 'd6742cc-f02d-4fd6-80f0-026784g1ab9b'

    book = book_ctrl.getBook(bookId, dynamodb)
    self.assertEqual(book, bookData)

  def test_getSectionFromBook(self):
    print('Running getSectionFromBook test case')
    bookId = 'd6742cc-f02d-4fd6-80f0-026784g1ab9b'
    chapterTitle = 'Chapter One'
    sectionTitle = 'Section One'

    res = book_ctrl.getSectionFromBook(bookId, chapterTitle, sectionTitle, dynamodb)
    self.assertNotEqual(res, {})

    chapterTitle2 = 'Non Existant'

    res = book_ctrl.getSectionFromBook(bookId, chapterTitle2, sectionTitle, dynamodb)
    self.assertEqual(res, {})


  def test_updateBookWithUserData(self):
    print('Running updateBookWithUserData test case')
    bookId = 'd6742cc-f02d-4fd6-80f0-026784g1ab9b'
    chapterTitle = 'Chapter One'
    sectionTitle = 'Section One'
    userId = 'test@mentii.me'
    weights = [1, -1, 1]
    success = book_ctrl.updateBookWithUserData(bookId, chapterTitle, sectionTitle, userId, weights, dynamodb)
    self.assertTrue(success)
    res = book_ctrl.getSectionFromBook(bookId, chapterTitle, sectionTitle, dynamodb)
    self.assertTrue(res['users'][userId] == weights)
