from problems.algebraTemplate import ProblemGenerator

problemBank = {'a1': ('$var = $a + $b', 1, 20, ['+', '-']), 'a2': ('$c + $var = $a $op $b', -20, 20, ['+', '-']), 'a3': ('$c$var + $bmulc = $amulc', -20, 20, ['+', '-']),}

def getProblem(classId, activity):
  global problemBank
  #Get massive data object from class table
  #Parse through it and grab a problem template
  #For now just return a problem and pretend its a template
  problem = 'Bad Problem'
  if activity in problemBank.keys():
    template, minVal, maxVal, ops = problemBank[activity]
    generator = ProblemGenerator(minVal=minVal, maxVal=maxVal, opVals=ops) #Get the operation values and min and max ints from the db
    problem = generator.buildProblemFromTemplate(template)

  
  return problem
  
