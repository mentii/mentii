from utils import db_utils as dbUtils
import utils.MentiiLogging as MentiiLogging
import random
import book_ctrl

problemBank = {'a1': '5x=10', 'a2':'2x + 3x - 5 = 5', 'a3': '2x = -3x + 15'}

def getProblemTemplate(classId, activity):
  global problemBank
  #Get massive data object from class table
  #Parse through it and grab a problem template
  #For now just return a problem and pretend its a template
  problemTemplate = 'Bad Problem'
  if activity in problemBank.keys():
    problemTemplate = problemBank[activity]
  return problemTemplate


def getProblemFromBook(bookId, chapterTitle, sectionTitle, dynamoDBInstance):
  #Get the book
  book = book_ctrl.getBook(bookId, dynamoDBInstance)
  problem = 'Bad Problem'
  
  if book is not None:
    for chapter in book['chapters']:
      if chapter.get('title', '') == chapterTitle:
        sections = chapter.get('sections', [])
        for section in sections:
          if section.get('title', '') == sectionTitle:
            problem = random.choice(section['problems'])
            break #Break out of section loop
        break #Break out of chapter loop

  return problem
