import boto3
from boto3.dynamodb.conditions import Key, Attr
from utils.ResponseCreation import ControllerResponse
from utils import db_utils as dbUtils
import uuid
from flask import g
import utils.MentiiLogging as MentiiLogging

def getActiveClassList(dynamoDBInstance, email=None):
  response = ControllerResponse()
  classes = []
  classCodes = getClassCodesFromUser(dynamoDBInstance)
  #Use the class codes to get the class details for
  # each class.
  table = dbUtils.getTable('classes', dynamoDBInstance)
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

def getClassCodesFromUser(dynamoDBInstance, email=None):
  classCodes = []
  if email is None:
    email = g.authenticatedUser['email']
  usersTable = dbUtils.getTable('users', dynamoDBInstance)
  if usersTable is None:
    MentiiLogging.getLogger().error("Unable to get users table in getClassCodesFromUser")
    return None
  #An active class list is the list of class codes that
  # a user has in the user table.
  request = {"Key" : {"email": email}, "AttributesToGet": ["classCodes"]}
  res = dbUtils.getItem(request, usersTable)
  #Get the class codes for the user.
  if res is not None and 'Item' in res:
    classCodes = res['Item']['classCodes']
  return classCodes

def getPublicClassList(dynamodb, email=None):
  response = ControllerResponse()
  classCodes = getClassCodesFromUser(dynamodb)
  classes = []
  classesTable = dbUtils.getTable('classes', dynamodb)
  res = classesTable.scan()
  for pclass in res['Items']:
    if pclass['code'] not in classCodes and 'private' not in pclass and pclass.get('private') != True:
      classes.append(pclass)
  response.addToPayload('classes', classes)
  return response
