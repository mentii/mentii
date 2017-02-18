import mathstepsWrapper as mathsteps
import random

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

def generateBadSteps(problemSolutionPath, numOfFailurePoints, failurePoints=None):
  # if testing failure points can be passed in
  # randomly pick failure points from problem solution path
  if not failurePoints:
    failurePoints = random.sample(problemSolutionPath, numOfFailurePoints)

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
