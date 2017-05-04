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


  def test_dropTerm(self):
    p1 = "5x = 3 - 2"
    p2 = "2x = 4"
    p3 = "3 = 1 - 2x"
    p4 = "Bad Problem"
    p5 = "x + 1 = 2"

    res = algebra.dropTerm(p1)
    self.assertTrue(p1 != res)
    res = algebra.dropTerm(p2)
    self.assertTrue(p2 == res)
    res = algebra.dropTerm(p3)
    self.assertTrue(p3 == res)
    res = algebra.dropTerm(p4)
    self.assertTrue(p4 == res)
    res = algebra.dropTerm(p5)
    self.assertTrue(p5 == res)



  def test_swapSign(self):
    p1 = "5x = 3 - 2"
    p2 = "2x = 4"
    p3 = "3 = 1 + 2x"
    p4 = "Bad Problem"
    p5 = "x + 1 = 2"

    res = algebra.swapSign(p1)
    self.assertTrue(p1 != res)
    res = algebra.swapSign(p2)
    self.assertTrue(p2 == res)
    res = algebra.swapSign(p3)
    self.assertTrue(p3 != res)
    res = algebra.swapSign(p4)
    self.assertTrue(p4 == res)
    res = algebra.swapSign(p5)
    self.assertTrue(p5 != res)

  def test_swapOperator(self):
    p1 = "5x = 3 * 2"
    p2 = "2x = 4 + 5"
    p3 = "3 = 1 + 2x"
    p4 = "Bad Problem"
    p5 = "x / 3 = 2"

    res = algebra.swapOperator(p1)
    self.assertTrue(p1 != res)
    res = algebra.swapOperator(p2)
    self.assertTrue(p2 != res)
    res = algebra.swapOperator(p3)
    self.assertTrue(p3 != res)
    res = algebra.swapOperator(p4)
    self.assertTrue(p4 == res)
    res = algebra.swapOperator(p5)
    self.assertTrue(p5 != res)

  def test_swapNumber(self):
    p1 = "5x = 3 * 2"
    p2 = "2x = 4 + 5"
    p3 = "3 = 1 + 2x"
    p4 = "Bad Problem"
    p5 = "x / 3 = 2"

    res = algebra.swapNumbers(p1)
    self.assertTrue(p1 is not None)
    res = algebra.swapNumbers(p2)
    self.assertTrue(p2 is not None)
    res = algebra.swapNumbers(p3)
    self.assertTrue(p3 is not None)
    res = algebra.swapNumbers(p4)
    self.assertTrue(p4 is not None)
    res = algebra.swapNumbers(p5)
    self.assertTrue(p5 is not None)

  def test_newTerm(self):
    p1 = "5x = 3 * 2"
    p2 = "2x = 4 + 5"
    p3 = "3 = 1 + 2x"
    p4 = "Bad Problem"
    p5 = "x / 3 = 2"

    res = algebra.newTerm(p1)
    self.assertTrue(p1 != res)
    res = algebra.newTerm(p2)
    self.assertTrue(p2 != res)
    res = algebra.newTerm(p3)
    self.assertTrue(p3 != res)
    res = algebra.newTerm(p4)
    self.assertTrue(p4 != res)
    res = algebra.newTerm(p5)
    self.assertTrue(p5 != res)

  def test_modifyStep(self):
    p1 = "5x = 3 * 2"
    p2 = "2x = 4 + 5"
    p3 = "3 = -1 + 2x"
    p4 = "Bad Problem"
    p5 = "x / 3 = 2"
    p6 = "x = 4"

    _, res = algebra.modifyStep(p1)
    self.assertTrue(res is not None)
    _, res = algebra.modifyStep(p2)
    self.assertTrue(res is not None)
    _, res = algebra.modifyStep(p3)
    self.assertTrue(res is not None)
    _, res = algebra.modifyStep(p4)
    self.assertTrue(res is not None)
    _, res = algebra.modifyStep(p5)
    self.assertTrue(res is not None)
    _, res = algebra.modifyStep(p6)
    self.assertTrue(res is not None)
    
  def test_isLastStep(self):
    p1 = "x = 3 * 2"
    p2 = "2x = 3"
    p3 = "x = -2"
    p4 = "Bad Problem"
    p5 = "x = 4"

    res = algebra.isLastStep(p1)
    self.assertFalse(res)
    res = algebra.isLastStep(p2)
    self.assertFalse(res)
    res = algebra.isLastStep(p3)
    self.assertTrue(res)
    res = algebra.isLastStep(p4)
    self.assertFalse(res)
    res = algebra.isLastStep(p5)
    self.assertTrue(res)

  def test_badNumber(self):
    p1 = "x = -2"
    p2 = "x = 4"

    res = algebra.badNumber(p1)
    self.assertFalse(res == p1)
    res = algebra.badNumber(p2)
    self.assertFalse(res == p2)
