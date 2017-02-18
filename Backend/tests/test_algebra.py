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
    sol1 = [u'(5x) / 5 = 10/5', u'x = 10/5', u'x = 2']
    sol2 = [u'(3 + 2)x = 5 * 2', u'5x = 5 * 2',  u'5x = 5 * 2', u'5x = 10', u'(5x) / 5 = 10/5', u'x = 10/5', u'x = 2']
    steps = mathstepsWrapper.getStepsForProblem(problem1)
    self.assertEqual(sol1, steps)
    steps = mathstepsWrapper.getStepsForProblem(problem2)
    self.assertEqual(sol2, steps)

  def test_generateBadSteps(self):
    print('Running generateBadSteps test case')
    problem = '11+x=55/5'
    path = mathstepsWrapper.getStepsForProblem(problem)
    failurePoints = [u'11 + x = 11']
    badSteps = algebra.generateBadSteps(path,1, failurePoints)

    response = [
      {
        'correctStep' : u'11 + x = 11',
        'badStep' : u'11 - x = 11',
        'badStepPath' : [u'(11 - x) - 11 = 11 - 11', u'-x + 0 = 11 - 11', u'-x = 11 - 11', u'-x = 11 - 11', u'-x = 0', u'-x * -1 = 0 * -1', u'x = 0 * -1', u'x = 0']
      },
      { 'correctStep' : u'(11 + x) - 11 = 11 - 11'},
      { 'correctStep' : u'x + 0 = 11 - 11'},
      { 'correctStep' : u'x = 11 - 11'},
      { 'correctStep' : u'x = 11 - 11'},
      { 'correctStep' : u'x = 0'},
    ]
    self.assertEqual(response, badSteps)


if __name__ == '__main__':
  if __package__ is None:
    import sys
    from os import path
    sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
    from problems import mathstepsWrapper
  else:
    from ..problems import mathstepsWrapper
  unittest.main()
