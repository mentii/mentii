#!/usr/bin/env python
import subprocess
import os

JAVASCRIPT_FIRSTLINE="const mathsteps = require('mathsteps');\n"
JAVASCRIPT_PROBLEMLINE="const steps = mathsteps.solveEquation('{0}')\n";
JAVASCRIPT_PRINTLINE="steps.forEach(step => {console.log(step.newEquation.print()); });\n"

JAVASCRIPT_FILEPATH='/home/ryan/workspace/mathstepsStuff/mentii.js'
JAVASCRIPT_OUTPUTPATH='mentii_output.txt'

'''
NOTE: 

  It looks like the mathsteps needs to be installed where ever the 
  javascript file is executed. This means we can have a special 
  place on the server that has mathsteps and we just write and run the
  script there. 
'''

 
def _writeProblemFile(problem, filename=JAVASCRIPT_FILEPATH):
  with open(filename, 'w') as f:
    f.write(JAVASCRIPT_FIRSTLINE)
    f.write(JAVASCRIPT_PROBLEMLINE.format(problem))
    f.write(JAVASCRIPT_PRINTLINE)


def getStepsForProblem(problem):
  _writeProblemFile(problem)
  with open(JAVASCRIPT_OUTPUTPATH, 'w') as f:
    subprocess.call(['nodejs', JAVASCRIPT_FILEPATH], stdout=f)
  
  problemSteps = []
  with open(JAVASCRIPT_OUTPUTPATH, 'r') as f:
    for line in f:
      problemSteps.append(line)

  #Clean up the tmp files
  os.remove(JAVASCRIPT_FILEPATH)
  os.remove(JAVASCRIPT_OUTPUTPATH)

  return problemSteps

