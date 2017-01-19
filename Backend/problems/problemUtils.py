import sympy

def simplify(expression):
  '''
  Given a list of operands and 
  operators, attempt to simplify

  NO VARIABLES MAY BE PASSED
  ONLY INTS
  NO PARENS
  example: 
  simplify(["3", "+", "2"])

  '''

  digit = None
  add = False
  subtract = False

  for val in expression:
    if val.isdigit():
      if add:
        #Add the last element in the digits list 
        digit = digit + int(val)
        add = False
      elif subtract:
        digit = digit - int(val)
        subtract = False
      else:
        digit = int(val) #Should only happen with the first digit
    elif val == '+':
      add = True
    elif val == '-':
      subtract = True
    else:
      #Error! Bad symbol
      return 0

  return digit



