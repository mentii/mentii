import unittest
import sys
import boto3
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from mentii import problem_ctrl
from mentii import book_ctrl

#local DynamoDB
dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')

class ProblemCtrlTests(unittest.TestCase):

  def test_getProblemFromBook(self):
    bookId = 'd6742cc-f02d-4fd6-80f0-026784g1ab9b'
    chapterTitle = 'Chapter 1'
    sectionTitle = 'Section 2'
    problem = problem_ctrl.getProblemFromBook(bookId, chapterTitle, sectionTitle, dynamodb)
    print(problem)






if __name__ == '__main__':
  if __package__ is None:
    import sys
    from os import path
    sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
    from problems import mathstepsWrapper
  else:
    from ..problems import mathstepsWrapper
  unittest.main()
