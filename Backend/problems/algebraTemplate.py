from string import Template
import random



class ProblemGenerator:

  def __init__(self, seed=None, opVals=None):
    self.randomGen = random.Random(seed)
    self.intMax = 20
    self.intMin = -20
    if opVals:
      self.operationValues = opVals
    else:
      self.operationValues = ['+', '-', '*', '/']
    self._updateTemplateValueMap()
   
  def _updateTemplateValueMap(self):
    a = 0
    b = 0
    c = 0
    d = 0
    while a == 0 or b == 0 or c == 0 or d == 0:
      a = self.randomGen.randint(self.intMin, self.intMax)
      b = self.randomGen.randint(self.intMin, self.intMax)
      c = self.randomGen.randint(self.intMin, self.intMax)
      d = self.randomGen.randint(self.intMin, self.intMax)
    op = self.randomGen.choice(self.operationValues)
    print("{0}, {1}, {2}, {3}".format(a, b, c, d))
    self.templateMap = {
        'a': a,
        'b': b,
        'c': c,
        'd': d,
        'aplusb': a+b,
        'aplusc': a+c,
        'aplusd': a+d, 
        'bplusc': b+c,
        'bplusd': b+d,
        'cplusd': c+d,
        'amulb': a*b,
        'amulc': a*c,
        'amuld': a*d, 
        'bmulc': b*c,
        'bmuld': b*d,
        'cmuld': c*d,
        'asubb': a-b,
        'asubc': a-c,
        'asubd': a-d, 
        'bsubc': b-c,
        'bsubd': b-d,
        'csubd': c-d,
        'adivb': a/b,
        'adivc': a/c,
        'adivd': a/d, 
        'bdivc': b/c,
        'bdivd': b/d,
        'cdivd': c/d,
        'op' : op, 
        'var': 'x'}

  def buildProblemFromTemplate(self, templateString):
    template = Template(templateString)
    problem = template.substitute(self.templateMap)
    return problem
