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

def editBook(bookData, dynamoDBInstance):
  response = ControllerResponse()
  # check for required options
  if 'title' not in bookData.keys() or 'description' not in bookData.keys() or 'bookId' not in bookData.keys():
    response.addError('Book update failed.', 'Invalid book data given.')
  else:
    # Get books table
    booksTable = dbUtils.getTable('books', dynamoDBInstance)
    if booksTable is None:
      response.addError(  'Get Books Table Failed',
                          'Unable to get books table from database')
    else :
      # put item into table
      result = dbUtils.putItem(bookData, booksTable)
      if result is None:
        response.addError('Book update failed.', 'Unable to update Book in database.')
      else:
        response.addToPayload('Success', 'Book Updated')

  return response

def getBook(bookId, dynamoDBInstance):
  response = {}
  booksTable = dbUtils.getTable('books', dynamoDBInstance)
  if booksTable is None:
    MentiiLogging.getLogger().error('Could not get book table') 
  else:
    bookQuery = {'Key': {'bookId': bookId}}
    res = dbUtils.getItem(bookQuery, booksTable)
    if res is not None and 'Item' in res.keys():
      response = res['Item']
    else:
      MentiiLogging.getLogger().warning('Could not get an item from the books table') 

  return response

def updateBookWithUserData(bookId, chapterTitle, sectionTitle, userId, weights, dynamoDBInstance):
  book = getBook(bookId, dynamoDBInstance)
  if book is not None:
    for chapter in book.get('chapters', []):
      if chapter.get('title', '') == chapterTitle:
        sections = chapter.get('sections', [])
        for section in sections:
          if section.get('title', '') == sectionTitle:
            #Get the section of interest
            if 'users' not in section.keys():
              section['users'] = {}
            section['users'][userId] = weights
            break 
        break 
  return not editBook(book, dynamoDBInstance).hasErrors()


def getSectionFromBook(bookId, chapterTitle, sectionTitle, dynamoDBInstance):
  book = getBook(bookId, dynamoDBInstance)
  sectionToUse = {}
  if book is not None:
    for chapter in book.get('chapters', []):
      if chapter.get('title', '') == chapterTitle:
        sections = chapter.get('sections', [])
        for section in sections:
          if section.get('title', '') == sectionTitle:
            sectionToUse = section           
            break #Break out of section loop
        break #Break out of chapter loop

  return sectionToUse
