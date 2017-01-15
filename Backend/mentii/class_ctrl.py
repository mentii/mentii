import boto3
from boto3.dynamodb.conditions import Key, Attr
from utils.ResponseCreation import ControllerResponse
from utils import db_utils as dbUtils
import uuid
from flask import g
import utils.MentiiLogging as MentiiLogging

def getActiveClassList(dynamoDBInstance, email=None):
  response = ControllerResponse()
  if email is None:
    email = g.authenticatedUser['email']
  dynamodb = dynamoDBInstance
  table = dbUtils.getTable('users', dynamodb)
  if table is None:
    MentiiLogging.getLogger().error("Unable to get users table in getActiveClassList")
    return None
  classCodes = []
  classes = []
  #An active class list is the list of class codes that
  # a user has in the user table.
  request = {"Key" : {"email": email}, "ProjectionExpression": "classCodes"}
  res = dbUtils.getItem(request, table)
  #Get the class codes for the user.
  if res is not None and 'Item' in res:
    classCodes = res['Item']['classCodes']

  #Use the class codes to get the class details for
  # each class.
  table = dbUtils.getTable('classes', dynamodb)
  if table is None:
    MentiiLogging.getLogger().error("Unable to get classes table in getActiveClassList")
    return None
  for code in classCodes:
    request = {"Key": {"code": code}}
    res = dbUtils.getItem(request, table)
    if res is not None and 'Item' in res:
      classes.append(res['Item'])

  response.addToPayload('classes', classes)
  return response