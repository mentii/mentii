from utils import db_utils as dbUtils
import utils.MentiiLogging as MentiiLogging
from utils.ResponseCreation import ControllerResponse
import random
import decimal
from numpy.random import choice
import book_ctrl


def getProblemTemplate(classId, activity, userId, dynamoDBInstance):
  bookId, chapterTitle, sectionTitle = getBookInfoFromActivity(classId, activity, dynamoDBInstance)
  (index, problemTemplate) = getProblemFromBook(bookId, chapterTitle, sectionTitle, userId, dynamoDBInstance)
  return (index, problemTemplate)


def getBookInfoFromActivity(classId, activityTitle, dynamoDBInstance):
  classItem = {}
  bookId = ''
  chapterTitle = ''
  sectionTitle = ''
  classTable = dbUtils.getTable('classes', dynamoDBInstance)
  if classTable is None:
    MentiiLogging.getLogger().warning('Could not get the class table') 
  else:
    classQuery = {'Key': {'code': classId}}
    res = dbUtils.getItem(classQuery, classTable)
    if res is not None and 'Item' in res.keys():
      classItem = res['Item']

  for activity in classItem.get('activities', []):
    if activity.get('title', '') == activityTitle:
      bookId = activity.get('bookId', '')
      chapterTitle = activity.get('chapterTitle', '')
      sectionTitle = activity.get('sectionTitle', '')
      break #Only get the first activity with this title

  return (bookId, chapterTitle, sectionTitle)

def chooseProblemTemplate(templateList, userHistoryList):
  '''
  The userHistoryList should be a list of integers
  '''
  index = -1
  problemTemplate = 'Bad Problem'
  if len(templateList) == 0:
    MentiiLogging.getLogger().error("error, empty template list passed")
  else:
    history = [-1*x for x in userHistoryList]
    if len(history) != len(templateList):
      history = [ 0 for _ in xrange(len(templateList))]

    #Normalize the history to be all positive numbers
    minVal = min(history)
    history = [x + abs(minVal) + 1 for x in history]
    #Create a probablility distribution
    total = sum(history)
    probDist = [decimal.Decimal(x)/total for x in history]

    index = choice(range(0, len(templateList)), p=probDist)
    problemTemplate = templateList[index].get('problemString', '')

  return (index, problemTemplate)


def updateUserTemplateHistory(classId, activity, userId, index, didSucceed, dynamoDBInstance):
  #Get the section so we can update the weights
  response = ControllerResponse()
  bookId, chapterTitle, sectionTitle = getBookInfoFromActivity(classId, activity, dynamoDBInstance)
  section = book_ctrl.getSectionFromBook(bookId, chapterTitle, sectionTitle, dynamoDBInstance)
  #Update the weights or create new ones if this is the first time
  currentWeights = section.get('users', {}).get(userId, [])
  newWeights = [0 for _ in xrange(len(section.get('problems', [])))] #Initial value
  if len(currentWeights) != 0: #Update if we can
    newWeights = currentWeights
  #Actually update the weights 
  if index < len(newWeights):
    if didSucceed:
      newWeights[index] += 1
    else:
      newWeights[index] -= 1
  #Send it elsewhere to update the database
  updateSuccessful = book_ctrl.updateBookWithUserData(bookId, chapterTitle, sectionTitle, userId, newWeights, dynamoDBInstance)
  if not updateSuccessful:
    response.addError('History Update Error', 'Unable to update the users history')

  return response



def getProblemFromBook(bookId, chapterTitle, sectionTitle, userId, dynamoDBInstance):
  section = book_ctrl.getSectionFromBook(bookId, chapterTitle, sectionTitle, dynamoDBInstance)
  problem = 'Bad Problem'
  index = -1
  #From the section we got get the weights and chose a random problem using them
  weights = section.get('users', {}).get(userId, [])
  problemTemplates = section.get('problems', [])
  index, problem = chooseProblemTemplate(problemTemplates, weights)

  return (index, problem)

