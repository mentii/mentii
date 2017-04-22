import uuid
from utils.ResponseCreation import ControllerResponse
from utils import db_utils as dbUtils
from flask import g
import utils.MentiiLogging as MentiiLogging

def createBook(bookData, dynamoDBInstance, userRole=None):
  response = ControllerResponse()

  #g will be not be available during testing
  #userRole will need to be passed to the function
  if g: # pragma: no cover
    userRole = g.authenticatedUser['userRole']
  #role is confirmed here incase createBook is called from somewhere other
  #than app.py createBook()
  if userRole != 'admin':
    response.addError('Role error', 'Only admins can create books')
  # check for required options
  elif 'title' not in bookData.keys() or 'description' not in bookData.keys():
    response.addError('Book creation failed.', 'Invalid book data given.')
  else:
    # Get books table
    booksTable = dbUtils.getTable('books', dynamoDBInstance)
    if booksTable is None:
      response.addError(  'Get Books Table Failed',
                          'Unable to get books table from database')
    else :
      bookId = str(uuid.uuid4())
      # prep json data
      book = {
        'bookId': bookId,
        'title': bookData['title'],
        'description': bookData['description'],
        'chapters': bookData.get('chapters', [])
      }
      # put item into table
      result = dbUtils.putItem(book, booksTable)
      if result is None:
        response.addError('Book creation failed.', 'Unable to create Book in database.')
      else:
        response.addToPayload('Success', 'Book Created')

  return response

def getBook(bookId, dynamoDBInstance):
  book = None
  booksTable = dbUtils.getTable('books', dynamoDBInstance)
  if booksTable is None:
    MentiiLogging.getLogger().error('Could not get book table')
  else:
    bookQuery = {'Key': {'bookId': bookId}}
    res = dbUtils.getItem(bookQuery, booksTable)
    if res is not None and 'Item' in res.keys():
      book = res['Item']
    else:
      MentiiLogging.getLogger().warning('Could not get an item from the books table')
  return book

def getBookList(dynamoDBInstance):
  response = ControllerResponse()
  booksTable = dbUtils.getTable('books', dynamoDBInstance)
  if booksTable is None:
    MentiiLogging.getLogger().error('Could not get book table')
    response.addError('Failed to get book list', 'A database error occured')
  else:
    books = dbUtils.scan(booksTable)
    bookList = []
    if books is not None and 'Items' in books:
      for book in books.get('Items'):
        bookList.append({
          'id' : book.get('bookId'),
          'title' : book.get('title')
        })
      response.addToPayload('books', bookList)
    else:
      MentiiLogging.getLogger().warning('Could not scan books table')
  return response
