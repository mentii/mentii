import unittest
import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from problems import mathstepsWrapper
from problems import algebra

class MentiiMathstepsTests(unittest.TestCase):

  def test_getStepsForProblem(self):
    print('Running getStepsForProblem test case')
    problem1 = '5x=10'
    problem2 = '3x+2x=5*2'
    sol1 = [u'5x=10',u'(5x) / 5 = 10/5', u'x = 10/5', u'x = 2']
    sol2 = [u'3x+2x=5*2',u'(3 + 2)x = 5 * 2', u'5x = 5 * 2', u'5x = 10', u'(5x) / 5 = 10/5', u'x = 10/5', u'x = 2']
    steps = mathstepsWrapper.getStepsForProblem(problem1)
    self.assertEqual(sol1, steps)
    steps = mathstepsWrapper.getStepsForProblem(problem2)
    self.assertEqual(sol2, steps)

  def test_generateTreeWithBadSteps(self):
    print('Running generateTreeWithBadSteps test case')
    problem = '11+x=55/5'
    path = mathstepsWrapper.getStepsForProblem(problem)

    failurePoints = [u'11 + x = 11']
    badSteps = algebra.generateTreeWithBadSteps(path,1, failurePoints)

    response = [
      {'correctStep' : u'11+x=55/5'},
      {
        'correctStep' : u'11 + x = 11',
        'badStep' : u'11 - x = 11',
        'badStepPath' : [u'11 - x = 11', u'(11 - x) - 11 = 11 - 11', u'-x + 0 = 11 - 11', u'-x = 11 - 11', u'-x = 0', u'-x * -1 = 0 * -1', u'x = 0 * -1', u'x = 0']
      },
      { 'correctStep' : u'(11 + x) - 11 = 11 - 11'},
      { 'correctStep' : u'x + 0 = 11 - 11'},
      { 'correctStep' : u'x = 11 - 11'},
      { 'correctStep' : u'x = 0'}
    ]

    
    self.assertEqual(response, badSteps)

  def test_getProblem(self):
    print('Running getProblem test case')
    activity1 = 'a1'
    activity1Result = '5x=10'
    activity2 = 'bad'
    activity2Result = 'Bad Problem'

    res1 = algebra.getProblem(activity1)
    res2 = algebra.getProblem(activity2)

    self.assertEqual(activity1Result, res1)
    self.assertEqual(activity2Result, res2)

  def test_getProblemTree(self):
    print('Running getProblemTree test case')
    activity1 = '5x=10'
    activity2 = 'bad'

    res1 = algebra.getProblemTree(activity1)
    self.assertFalse(res1.hasErrors())
    res2 = algebra.getProblemTree(activity2)
    self.assertTrue(res2.hasErrors())



if __name__ == '__main__':
  if __package__ is None:
    import sys
    from os import path
    sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
    from problems import mathstepsWrapper
  else:
    from ..problems import mathstepsWrapper
  unittest.main()
