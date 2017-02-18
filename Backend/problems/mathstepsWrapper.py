#!/usr/bin/env python
import subprocess
import os
import json

def getStepsForProblem(problem):
  mathstepsFile = os.path.dirname(os.path.abspath(__file__)) + "/index.js"
  problemStepsJson = subprocess.check_output(['node', mathstepsFile, problem])
  problemSteps = json.loads(problemStepsJson)
  return problemSteps
