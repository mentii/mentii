#!/usr/bin/env python
import subprocess
import os

JAVASCRIPT_FIRSTLINE="const mathsteps = require('mathsteps');\n"
JAVASCRIPT_PROBLEMLINE="const steps = mathsteps.solveEquation('{0}')\n";
JAVASCRIPT_PRINTLINE="steps.forEach(step => { if(step.substeps.length > 1){ step.substeps.forEach(subStep => console.log(subStep.newEquation.print())) }\n console.log(step.newEquation.print()); });\n"

JAVASCRIPT_FILEPATH='mentii.js'
JAVASCRIPT_OUTPUTPATH='mentii_output.txt'

'''
NOTE: 

  It looks like the mathsteps needs to be installed where ever the 
  javascript file is executed. This means we can have a special 
  place on the server that has mathsteps and we just write and run the
  script there. 
'''

def setMathstepsLocation(path):
  global JAVASCRIPT_FILEPATH
  #Set a global variable for the javacript path... 
  JAVASCRIPT_FILEPATH = path + "/mentii.js"

 
def _writeProblemFile(problem, filename):
  with open(filename, 'w') as f:
    f.write(JAVASCRIPT_FIRSTLINE)
    f.write(JAVASCRIPT_PROBLEMLINE.format(problem))
    f.write(JAVASCRIPT_PRINTLINE)


def getStepsForProblem(problem):
  _writeProblemFile(problem, JAVASCRIPT_FILEPATH)
  with open(JAVASCRIPT_OUTPUTPATH, 'w') as f:
    subprocess.call(['nodejs', JAVASCRIPT_FILEPATH], stdout=f)
  
  problemSteps = [problem]
  with open(JAVASCRIPT_OUTPUTPATH, 'r') as f:
    for line in f:
      cleanLine = line.strip()
      if cleanLine != problemSteps[-1]:
        problemSteps.append(cleanLine)

  #Clean up the tmp files
  os.remove(JAVASCRIPT_FILEPATH)
  os.remove(JAVASCRIPT_OUTPUTPATH)

  return problemSteps

