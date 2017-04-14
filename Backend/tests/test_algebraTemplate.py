import unittest
import sys
import boto3
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from mentii import problem_ctrl
from mentii import book_ctrl
from utils import db_utils as db
from problems.algebraTemplate import *

class ProblemGeneratorTest(unittest.TestCase):

  def test_ProblemGenerator(self):
    problemTemplate1 = '$a + $b = $var $op $d'
    problemTemplate2 = '2x + 5 = 15'
    
    pg1 = ProblemGenerator()
    pg2 = ProblemGenerator(minVal=0, maxVal=10, opVals=['+', '*'])

    prob1 = pg1.buildProblemFromTemplate(problemTemplate1)
    self.assertTrue('a' not in prob1)
    
    prob2 = pg2.buildProblemFromTemplate(problemTemplate1)
    self.assertTrue('-' not in prob2)
    
    prob3 = pg2.buildProblemFromTemplate(problemTemplate2)
    self.assertTrue(problemTemplate2 == prob3)
    
