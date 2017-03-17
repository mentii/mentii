import uuid
from utils.ResponseCreation import ControllerResponse
from utils import db_utils as dbUtils
from flask import g
import utils.MentiiLogging as MentiiLogging

def createBook(bookData, dynamoDBInstance, userRole=None):
  response = ControllerResponse()

  #g will be not be available during testing
  #userRole will need to be passed to the function
  if g:
    userRole = g.authenticatedUser['userRole']
  #role is confirmed here incase createBook is called from somewhere other
  #than app.py createBook()
  if userRole != 'admin':
    response.addError('Role error', 'Only admins can create books')
  elif bookData is None:
    response.addError('createBook call Failed.', 'Invalid book data given.')
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
        'chapters': bookData['chapters']
      }
      # put item into table
      result = dbUtils.putItem(book, booksTable)
      if result is None:
        response.addError('createBook call Failed.', 'Unable to create Book in database.')
      else:
        response.addToPayload('Success', 'Book Created')

  return response
