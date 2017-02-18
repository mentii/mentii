import unittest
import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from problems import mathstepsWrapper


class MentiiMathstepsTests(unittest.TestCase):

  def test_getStepsForProblem(self):
    print('Running getStepsForProblem test case')
    problem1 = "5x=10"
    problem2 = "3x+2x=5*2"
    sol1 = [u'5x=10', u'(5x) / 5 = 10/5', u'x = 10/5', u'x = 2']
    sol2 = [u'3x+2x=5*2',u'(3 + 2)x = 5 * 2', u'5x = 5 * 2', u'5x = 10', u'(5x) / 5 = 10/5', u'x = 10/5', u'x = 2']
    steps = mathstepsWrapper.getStepsForProblem(problem1)
    self.assertEqual(sol1, steps)
    steps = mathstepsWrapper.getStepsForProblem(problem2)
    self.assertEqual(sol2, steps)

if __name__ == '__main__':
  if __package__ is None:
    import sys
    from os import path
    sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
    from problems import mathstepsWrapper
  else:
    from ..problems import mathstepsWrapper
  unittest.main()
