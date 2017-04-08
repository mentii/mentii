import unittest
import sys
import boto3
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from mentii import problem_ctrl
from mentii import book_ctrl
from utils import db_utils as db
from problems import algebra


class ProblemCtrlTests(unittest.TestCase):

  def test_getProblem(self):
    problemTemplate1 = '$a + $b = $var $op $d'
    problemTemplate2 = '$a + $b = $var $op $d|0|10|+ *'
    problemTemplate3 = '2x + 5 = 15'
    badTemplate1 = '$ax+3=15|+ -'
    badTemplate2 = '$b = $a$var $op $d|a|b|- / *'

    prob1 = algebra.getProblem(problemTemplate1)
    self.assertTrue('a' not in prob1)
   
    prob2 = algebra.getProblem(problemTemplate2)
    self.assertTrue('a' not in prob2)
    
    prob3 = algebra.getProblem(problemTemplate3)
    self.assertTrue(problemTemplate3 == prob3)

    prob4 = algebra.getProblem(badTemplate1)
    self.assertTrue(prob4 == 'Bad Problem')
    
    prob5 = algebra.getProblem(badTemplate2)
    self.assertTrue(prob5 == 'Bad Problem')
