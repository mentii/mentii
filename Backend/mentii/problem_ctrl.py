from utils import db_utils as dbUtils
import utils.MentiiLogging as MentiiLogging
import random
from numpy.random import choice
import book_ctrl


def getProblemTemplate(classId, activity, dynamoDBInstance):
  bookId, chapterTitle, sectionTitle = getBookInfoFromActivity(classId, activity, dynamoDBInstance)
  problemTemplate = getProblemFromBook(bookId, chapterTitle, sectionTitle, dynamoDBInstance)
  return problemTemplate


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
  problemTemplate = 'Bad Problem'
  if len(templateList) == 0:
    print("error, empty template list passed")
  else:
    history = [-1*x for x in userHistoryList]
    if len(history) != len(templateList):
      history = [ 0 for _ in xrange(len(templateList))]

    #Normalize the history to be all positive numbers
    minVal = min(history)
    history = [x + abs(minVal) + 1 for x in history]
    #Create a probablility distrobution
    total = sum(history)
    probDist = [float(x)/total for x in history]
    print(history)
    print(probDist)

    problemTemplate = choice(templateList, p=probDist)

  return problemTemplate


def getProblemFromBook(bookId, chapterTitle, sectionTitle, userId, dynamoDBInstance):
  #Get the book
  book = book_ctrl.getBook(bookId, dynamoDBInstance)
  problem = 'Bad Problem'
  if book is not None:
    for chapter in book.get('chapters', []):
      if chapter.get('title', '') == chapterTitle:
        sections = chapter.get('sections', [])
        for section in sections:
          if section.get('title', '') == sectionTitle:
            #Get the user list 
            problem = random.choice(section['problems']).get('problemString')
            break #Break out of section loop
        break #Break out of chapter loop

  return problem
