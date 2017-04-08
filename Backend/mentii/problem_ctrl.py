from utils import db_utils as dbUtils
import utils.MentiiLogging as MentiiLogging
import random
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


def getProblemFromBook(bookId, chapterTitle, sectionTitle, dynamoDBInstance):
  #Get the book
  book = book_ctrl.getBook(bookId, dynamoDBInstance)
  problem = 'Bad Problem'
  if book is not None:
    for chapter in book.get('chapters', []):
      if chapter.get('title', '') == chapterTitle:
        sections = chapter.get('sections', [])
        for section in sections:
          if section.get('title', '') == sectionTitle:
            problem = random.choice(section['problems']).get('problemString')
            break #Break out of section loop
        break #Break out of chapter loop

  return problem
