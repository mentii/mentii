import json
from flask import Response

def createResponse(data, errors, statusCode):
  '''
  Put our data in a json string. 

  "standard"
  '''
  responseString = json.dumps({'payload' : data, 'errors' : errors})  
  response = Response(response=responseString, status=statusCode, mimetype='application/json')
  return response
