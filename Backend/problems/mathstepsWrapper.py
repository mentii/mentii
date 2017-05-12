#!/usr/bin/env python
import subprocess
import os
import json

def getStepsForProblem(problem):
  allowSubSteps = False; # Changing this to false will prevent all substeps from showing

  # Uncomment lines for types of changes you do not want to occur within mathsteps as a
  # normal step or substep
  disallowedChangeTypes = [
    # 'NO_CHANGE',
    # 'ABSOLUTE_VALUE',
    # 'ADD_COEFFICIENT_OF_ONE',
    # 'ADD_EXPONENT_OF_ONE',
    # 'ADD_FRACTIONS',
    # 'ADD_NUMERATORS',
    # 'ADD_POLYNOMIAL_TERMS',
    # 'BREAK_UP_FRACTION',
    # 'CANCEL_EXPONENT',
    # 'CANCEL_EXPONENT_AND_ROOT',
    # 'CANCEL_MINUSES',
    # 'CANCEL_TERMS',
    # 'CANCEL_ROOT',
    # 'COLLECT_AND_COMBINE_LIKE_TERMS',
    # 'COLLECT_EXPONENTS',
    # 'COLLECT_LIKE_TERMS',
    # 'COMMON_DENOMINATOR',
    # 'COMBINE_NUMERATORS',
    # 'COMBINE_UNDER_ROOT',
    # 'CONVERT_INTEGER_TO_FRACTION',
    # 'CONVERT_MULTIPLICATION_TO_EXPONENT',
    # 'DISTRIBUTE',
    # 'DISTRIBUTE_NEGATIVE_ONE',
    # 'DISTRIBUTE_NTH_ROOT',
    # 'DIVIDE_FRACTION_FOR_ADDITION',
    # 'DIVISION_BY_NEGATIVE_ONE',
    # 'DIVISION_BY_ONE',
    # 'EVALUATE_DISTRIBUTED_NTH_ROOT',
    # 'FACTOR_INTO_PRIMES',
    # 'GROUP_COEFFICIENTS',
    # 'GROUP_TERMS_BY_ROOT',
    # 'MULTIPLY_BY_INVERSE',
    # 'MULTIPLY_BY_ZERO',
    # 'MULTIPLY_COEFFICIENTS',
    # 'MULTIPLY_FRACTIONS',
    # 'MULTIPLY_DENOMINATORS',
    # 'MULTIPLY_NUMERATORS',
    # 'MULTIPLY_POLYNOMIAL_TERMS',
    # 'NTH_ROOT_VALUE',
    # 'REARRANGE_COEFF',
    # 'REMOVE_ADDING_ZERO',
    # 'REMOVE_EXPONENT_BY_ONE',
    # 'REMOVE_EXPONENT_BASE_ONE',
    # 'REMOVE_MULTIPLYING_BY_NEGATIVE_ONE',
    # 'REMOVE_MULTIPLYING_BY_ONE',
    # 'REDUCE_EXPONENT_BY_ZERO',
    # 'REDUCE_ZERO_NUMERATOR',
    # 'RESOLVE_DOUBLE_MINUS',
    # 'SIMPLIFY_ARITHMETIC',
    # 'SIMPLIFY_DIVISION',
    # 'SIMPLIFY_FRACTION',
    # 'SIMPLIFY_SIGNS',
    # 'SIMPLIFY_TERMS',
    # 'UNARY_MINUS_TO_NEGATIVE_ONE',
    #'ADD_TO_BOTH_SIDES',
    #'DIVIDE_FROM_BOTH_SIDES',
    #'MULTIPLY_BOTH_SIDES_BY_INVERSE_FRACTION',
    #'MULTIPLY_BOTH_SIDES_BY_NEGATIVE_ONE',
    #'MULTIPLY_TO_BOTH_SIDES',
    # 'SIMPLIFY_LEFT_SIDE',
    # 'SIMPLIFY_RIGHT_SIDE',
    #'SUBTRACT_FROM_BOTH_SIDES',
    # 'SWAP_SIDES',
    # 'STATEMENT_IS_TRUE',
    # 'STATEMENT_IS_FALSE'
    ''
  ]

  stringStepList = json.dumps(disallowedChangeTypes)
  stringAllowBadSteps = json.dumps(allowSubSteps)


  mathstepsFile = os.path.dirname(os.path.abspath(__file__)) + "/index.js"
  problemStepsJson = subprocess.check_output(['node', mathstepsFile, problem, stringStepList, stringAllowBadSteps])
  problemSteps = json.loads(problemStepsJson)
  return problemSteps
