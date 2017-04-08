import mathstepsWrapper as mathsteps
from utils.ResponseCreation import ControllerResponse
import random
from algebraTemplate import ProblemGenerator
import utils.MentiiLogging as MentiiLogging

def getProblem(problemTemplate):
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

def modifyStep(step):
  badStep = step
  #modify step
  if(badStep.find('*') != -1):
    badStep = badStep.replace('*', "/")
  elif(badStep.find('/') != -1):
    badStep = badStep.replace('/', "*")
  elif(badStep.find('+') != -1):
    badStep = badStep.replace('+', "-")
  elif(badStep.find('-') != -1):
    badStep = badStep.replace('-', "+")

  return badStep


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
    failurePoints = random.sample(problemSolutionPath[1:-1], numOfFailurePoints)
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
    badStep = modifyStep(step)
    badStepPath = mathsteps.getStepsForProblem(badStep)
    response[failureIndex]['badStep'] = badStep
    response[failureIndex]['badStepPath'] = badStepPath

  return response
