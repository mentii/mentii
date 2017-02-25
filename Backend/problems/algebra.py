import mathstepsWrapper as mathsteps
from utils.ResponseCreation import ControllerResponse
import random

problemBank = {'a1': '5x=10', 'a2':'2x + 3x - 5 = 5', 'a3': '2x = -3x + 15'}

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

def getProblem(activity):
  #For now just get a problem out of the hardcoded 'problem bank'
  problem = 'Bad Problem'
  if activity in problemBank.keys():
    problem = problemBank[activity]
  return problem


def getProblemTree(problem):
  #When problem templates work problem could 
  # be a problem template instead. If that's the case 
  # we could get the problem from the template here
  response = ControllerResponse()
  numberOfFailurePoints = 2 #TODO: Replace this with the recommender system output

  problemPath = mathsteps.getStepsForProblem(problem)
  if len(problemPath) <= 1:
    #We couldn't get a path for the problem
    response.addError("Problem Solve Error", "Could not generate path for problem {0}".format(problem))
  else:
    problemTree = generateBadSteps(problemPath, numberOfFailurePoints)
    response.addToPayload("problemTree", problemTree)

  return response



def generateBadSteps(problemSolutionPath, numOfFailurePoints, failurePoints=None):
  # if testing failure points can be passed in
  # randomly pick failure points from problem solution path
  if not failurePoints and numOfFailurePoints < (len(problemSolutionPath) - 1):
    #Use a slice so we don't pick the first step as a failure point
    failurePoints = random.sample(problemSolutionPath[1:-1], numOfFailurePoints)
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
