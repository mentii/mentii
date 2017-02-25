import boto3
from boto3.dynamodb.conditions import Key, Attr
from utils.ResponseCreation import ControllerResponse
from utils import db_utils as dbUtils
import utils.MentiiLogging as MentiiLogging
from flask import g
  
problemBank = {'a1': '5x=10', 'a2':'2x + 3x - 5 = 5', 'a3': '2x = -3x + 15'}

def getProblemTemplate(classId, activity):
  global problemBank
  #Get massive data object from class table
  #Parse through it and grab a problem template
  #For now just return a problem and pretend its a template
  problemTemplate = 'Bad Problem'
  if activity in problemBank.keys():
    problemTemplate = problemBank[activity]
  return problemTemplate
  
