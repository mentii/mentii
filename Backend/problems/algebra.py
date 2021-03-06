import mathstepsWrapper as mathsteps
from utils.ResponseCreation import ControllerResponse
import random
from algebraTemplate import ProblemGenerator
import re
import operator
import utils.MentiiLogging as MentiiLogging

def getProblem(problemTemplate):
  '''
  Expects a problem template of the form: 
  <template>|<*min range>|<*max range>|<*operator list>

  The template can be any math expression with $a, $b, $c, $d for any numerical value, $var for the variable 'x', $op for a random operator from the operator list.

  The values for the min range, max range, and operator list are optional but if one is provided all values have to be provided. The default values are: -20, 20, and + - * 
  '''
  problem = 'Bad Problem'
  problemTokens = problemTemplate.split('|')
  if len(problemTokens) == 4:
    try:
      template = problemTokens[0]
      minVal = int(problemTokens[1])
      maxVal = int(problemTokens[2])
      opVals = problemTokens[3].split(' ')
      generator = ProblemGenerator(minVal=minVal, maxVal=maxVal, opVals=opVals)     
      problem = generator.buildProblemFromTemplate(template)
    except Exception as e:
      MentiiLogging.getLogger().exception(e)
  elif len(problemTokens) == 1:
    template = problemTokens[0]
    generator = ProblemGenerator() 
    problem = generator.buildProblemFromTemplate(template)
  else:
    MentiiLogging.getLogger().warning('Could not build problem from template: {0}'.format(problemTemplate)) 
  
  return problem

def dropTerm(step):
  '''
  Always drop the right most term 
  '''
  regex = '(\+|-|\*|/| )+\s*\d+' #Will match any number after an operator
  termList = [m.start() for m in re.finditer(regex, step)]
  res = step
  if len(termList) > 0 and 'x' in step:
    lastTerm = termList[-1]
    badStep = step[0:lastTerm] #Get everything upto but not inlcuding the last term. 
    #Check to make sure we didnt drop the coefficent of x
    if 'x' in badStep and 'x' in step:
      xIndex = step.index('x')
      newXIndex = badStep.index('x')
      if step[xIndex-1] != badStep[newXIndex - 1 ]: #The coeffiecent of X was dropped :( 
        badstep = step
      res = badStep

    if not '=' in res or res[-1] == '=':
      res = step

  return res


def swapSign(step):
  signs = [m.start() for m in re.finditer('-(x|\d+)', step)]
  res = step
  if len(signs) > 0:
    signToSwap = random.choice(signs)
    badStep = list(step)
    if step[signToSwap] == '-':
      badStep[signToSwap] = ''
    res = ''.join(badStep)

  return res

def swapOperator(step):
  operators = [m.start() for m in re.finditer('(\+|-|\*|/){1}', step)]
  res = step
  if len(operators) > 0:
    signToSwap = random.choice(operators)
    badStep = list(step)
    if step[signToSwap] == '+':
      badStep[signToSwap] = '*'
    elif step[signToSwap] == '-' and step[signToSwap+1] == ' ':
      badStep[signToSwap] = '/'
    elif step[signToSwap] == '/':
      badStep[signToSwap] = '*'
    elif step[signToSwap] == '*':
      badStep[signToSwap] = '/'
    res = ''.join(badStep)

    if step[signToSwap+1] == 'x':
      res = step
    
  
  return res
  

def swapNumbers(step):
  numbers = [(m.start(), m.end()) for m in re.finditer('-?\d+', step)]
  res = step
  if len(numbers) > 1:
    firstNum, secondNum = random.sample(numbers, 2)
    if firstNum[0] > secondNum[0]:
      firstNum, secondNum = secondNum, firstNum
    if '=' in step[firstNum[1]:secondNum[0]]:#This means the swap is across the equal sign. If it isn't we don't do it.
      badStep = []
      #Get everything upto the first number's start
      badStep.append(step[0:firstNum[0]])
      #Add the second number
      badStep.append(step[secondNum[0]:secondNum[1]])
      #Get everything from the first number's end to the second number start
      badStep.append(step[firstNum[1]:secondNum[0]])
      #Add the first number
      badStep.append(step[firstNum[0]:firstNum[1]])
      #Get everything from the second number's end to the end
      badStep.append(step[secondNum[1]:])
      res = ''.join(badStep)

  
  return res

def isLastStep(step):
  regex = r'^\s*x = -?\d+\s*$'
  return bool(re.search(regex, step))

def badNumber(step):
  op = random.choice([operator.add, operator.sub, operator.mul, operator.div])
  num = random.choice(xrange(2, 20))
  digits = map(int, re.findall(r'-?\d+', step))
  newDigit = 0
  if len(digits) > 0:
    newDigit = int(op(digits[0], num)) 
  return 'x = {0}'.format(newDigit)

def newTerm(step):
  op = random.choice(["+", "-"])
  num = random.choice(xrange(0, 10))
  term = " {0} {1}".format(op, num)
  res = step + term
  return res

def modifyStep(step):
  badStep = step
  success = False
  containsNegOne = r'-1(?:[^\d]|$)'
  if isLastStep(step):
    badStep = badNumber(step)
  elif not re.search(containsNegOne, step):
    modifications = [dropTerm, swapSign, swapOperator, swapNumbers]
    modfunc = random.choice(modifications)
    badStep = modfunc(badStep)
 
  success = badStep != step

  return (badStep, success)


def getProblemTree(problemTemplate):
  #When problem templates work problem could 
  # be a problem template instead. If that's the case 
  # we could get the problem from the template here
  response = ControllerResponse()
  numberOfFailurePoints = 2 #TODO: Replace this with the recommender system output
  problem = getProblem(problemTemplate)  
  problemPath = mathsteps.getStepsForProblem(problem)
  if len(problemPath) <= 1:
    #We couldn't get a path for the problem
    response.addError('Problem Solve Error', 'Could not generate path for problem {0}'.format(problem))
  else:
    problemTree = generateTreeWithBadSteps(problemPath, numberOfFailurePoints)
    response.addToPayload('problemTree', problemTree)

  return response



def generateTreeWithBadSteps(problemSolutionPath, numOfFailurePoints, failurePoints=None):
  # if testing failure points can be passed in
  # randomly pick failure points from problem solution path
  if not failurePoints and numOfFailurePoints < (len(problemSolutionPath) - 1):
    #Use a slice so we don't pick the first step as a failure point
    failurePoints = random.sample(problemSolutionPath[1:], numOfFailurePoints)
  elif failurePoints:
    pass #Keep the failure points as they were passed in
  else:
    failurePoints = []


  response = []
  for correctStep  in problemSolutionPath:
    step = {}
    step['correctStep'] = correctStep
    response.append(step)

  # for each failure point generate the bad step and path
  for step in failurePoints:
    failureIndex = problemSolutionPath.index(step)
    badStep, successful = modifyStep(step)
    if successful:
      badStepPath = mathsteps.getStepsForProblem(badStep)
      response[failureIndex]['badStep'] = badStep
      response[failureIndex]['badStepPath'] = badStepPath

  return response
