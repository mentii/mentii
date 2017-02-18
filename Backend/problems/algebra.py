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

'''
  Called by API
  Gets the index of the selected steps from pickFailurePoints in the original solution path
'''
def generateBadSteps(problemSolutionPath, numOfFailurePoints):
  # randomly pick failure points from problem solution path
  failurePoints = random.sample(problemSolutionPath, numOfFailurePoints)

  response = []
  for correctStep  in problemSolutionPath:
    step = {}
    step['correctStep'] = correctStep
    response.append(step)

  # for each failure point generate the bad step and path
  for step in failurePoints:
    #print(step)
    failureIndex = problemSolutionPath.index(step)
    badStep = modifyStep(step)
    badStepPath = mathsteps.getStepsForProblem(badStep)
    response[failureIndex]['badStep'] = badStep
    response[failureIndex]['badStepPath'] = badStepPath

  return response