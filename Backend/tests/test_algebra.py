import unittest
import sys
from os import path
import ConfigParser as cp
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from problems import mathstepsWrapper


#Configuration setup
configPath = "/config/prodConfig.ini"
parser = cp.ConfigParser()
parser.read(configPath)

mathstepsPath = parser.get("MathstepsLocation", 'path')

class MentiiMathstepsTests(unittest.TestCase):

  @classmethod
  def setUpClass(self):
    mathstepsWrapper.setMathstepsLocation(mathstepsPath)

  def test_getStepsForProblem(self):
    problem1 = "5x=10"
    problem2 = "3x+2x=5*2"
    sol1 = ['5x=10', '(5x) / 5 = 10/5', 'x = 10/5', 'x = 2']
    sol2 = ['3x+2x=5*2', '(3 + 2)x = 5 * 2', '5x = 5 * 2', '5x = 10', '(5x) / 5 = 10/5', 'x = 10/5', 'x = 2']
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
