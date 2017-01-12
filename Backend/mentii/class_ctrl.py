import boto3
from boto3.dynamodb.conditions import Key, Attr
from utils.ResponseCreation import ControllerResponse
import uuid
from flask import g

def getActiveClassList(dynamoDBInstance, email=None):
  response = ControllerResponse()
  user = email
  if email is None:
    user = g.authenticatedUser
  dynamodb = dynamoDBInstance
  table = dynamodb.Table('users')
  classCodes = []
  classes = []
  #An active class list is the list of class codes that
  # a user has in the user table. 
  res = table.get_item( 
          Key={
            'email': email,
          },
          ProjectedExpression='class_codes'
          )
  #Get the class codes for the user. 
  if res is not None and 'Item' in res:
    classCodes = res['Item']['class_codes']




  #Use the class codes to get the class details for 
  # each class. 
  table = dynamodb.Table('classes')
  for code in classCodes:
    res = table.get_item( 
            Key={
              'code': code,
            },
            ProjectedExpression='title'
            )
    if res is not None and 'Item' in res:
      classes.append(res['Item']['title'])

  response.addToPayload('classes', classes)
  return response
