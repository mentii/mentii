#!/usr/bin/env python

class problem:
  
  def __init__(self):
    '''
    Problem representation. 

    Problems consist of a right hand side 
    and a left hand side. Each side can have
    operands and operators. There must be 
    at least one operand on each side of 
    a problem.
    
    Operands will be represented by string numbers
    
    Operators will be represented by string characters.
      Currently supported: "+" "-"

    Variables are represented by string characters
    '''
    self.rhs = []
    self.lhs = []

  def setEquation(self, lhs, rhs):
    self.lhs = lhs
    self.rhs = rhs

  def findSteps(self):
    '''
    Find steps that we can take to solve this equation. 

    The idea is to return a list that we can then choose 
    a step from and then apply that operation to both sides. 

    This requires that the equation always has 'x' in 
    one of the sides and that 'x' appears as the first
    thing in that equation. 

    Test:
    >>> foo = problem()
    >>> foo.setEquation(['x', '+', '2', '-', '3'], ['4'])
    >>> foo.findSteps()
    ['-2', '+3']
    '''
    steps = []
    varSide = None
    otherSide = None
    if len(self.rhs) == 0 or len(self.lhs) == 0:
      #Error, an equation needs something on both sides
      return steps

    if 'x' in self.rhs:
      varSide = self.rhs
      otherSide = self.lhs
    else:
      varSide = self.lhs
      otherSide = self.rhs
      
    operator = None
    operand = None
    for val in varSide:
      if val == 'x':
        continue
      elif val == '+':
        operator = '+'
      elif val == '-':
        operator = '-'
      elif val.isdigit():
        operand = val 
        if operator is not None:
          if operator == '+':
            steps.append('-'+operand)
            operand = None
          elif operator == '-':
            steps.append('+'+operand)
            operand = None

    return steps








