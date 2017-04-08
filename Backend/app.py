#!env/bin/python

from flask import Flask, request, jsonify, Response
from flask_cors import CORS, cross_origin
from flask_mail import Mail
from flask_httpauth import HTTPBasicAuth
from flask import g
from mentii import user_ctrl
from mentii import class_ctrl
from mentii import problem_ctrl
from mentii import book_ctrl
from problems import mathstepsWrapper
from problems import algebra
from utils import MentiiAuth
from utils.Decorators import *
import utils.ResponseCreation as ResponseCreation
import utils.MentiiLogging as MentiiLogging
import boto3
import ConfigParser as cp
import sys

#Configuration setup
configPath = "/config/prodConfig.ini"
if len(sys.argv) == 2:
  configPath = sys.argv[1]

#Parse any external configuration options
parser = cp.ConfigParser()
parser.read(configPath)

#Setup logfile
logPath = parser.get('LogfileLocation', 'path') + '/logs'
MentiiLogging.setupLogger(logPath)
logger = MentiiLogging.getLogger()

#Start Flask App
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
mail = Mail(app)
auth = HTTPBasicAuth()

#Email setup
address = parser.get('EmailData', 'address')
password = parser.get('EmailData', 'password')
appSecret = parser.get('MentiiAuthentication', 'appSecret')

#Database configuration
prod = parser.get('DatabaseData', 'isProd')
logger.info("Databse Configuration: prod: " + str(prod))

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = address
app.config['MAIL_DEFAULT_SENDER'] = address
app.config['MAIL_PASSWORD'] = password
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

def getDatabaseClient():
  '''
  Return the correct database client object based
  on if we are in Dev or Prod
  '''
  if prod == 'True':
    logger.info("Using AWS Prod Database")
    return boto3.resource('dynamodb')
  else:
    logger.info("Using Local Dev Database")
    return boto3.resource('dynamodb', endpoint_url='http://localhost:8000')



@auth.verify_password
def verify_password(email_or_token, password):
  logger.info(str(request))
  dynamoDBInstance = getDatabaseClient()
  response = MentiiAuth.verifyPassword(email_or_token, password, dynamoDBInstance, appSecret)
  logger.info('Password Verified: ' + str(response))
  return response

@app.route('/', methods=['GET', 'POST'])
def index():
  logger.info(str(request))
  response = ResponseCreation.createEmptyResponse(200)
  logger.info(str(response))
  return response

@app.route('/register/', methods=['POST', 'OPTIONS'])
@handleOptionsRequest
def register():
  logger.info(str(request))
  status = 200
  dynamoDBInstance = getDatabaseClient()
  httpOrigin = request.environ.get('HTTP_ORIGIN')
  jsonData = request.json
  res = user_ctrl.register(httpOrigin, jsonData, mail, dynamoDBInstance)
  status = 201
  if res.hasErrors():
    status = 400
  flaskResponse =  ResponseCreation.createResponse(res, status)
  logger.info(str(flaskResponse))
  return flaskResponse

@app.route('/activate/<activationid>', methods=['GET'])
def activate(activationid):
  logger.info(str(request))
  dynamoDBInstance = getDatabaseClient()
  res = user_ctrl.activate(activationid, dynamoDBInstance)
  status = 200
  if res.hasErrors():
    status = 400
  flaskResponse = ResponseCreation.createResponse(res, status)
  logger.info(str(flaskResponse))
  return flaskResponse

@app.route('/signin/', methods=['POST', 'OPTIONS'])
@auth.login_required
@handleOptionsRequest
def signin():
  logger.info(str(request))
  status = 200

  email = request.authorization.username
  password = request.authorization.password
  dynamoDBInstance = getDatabaseClient()
  userRole = user_ctrl.getRole(email, dynamoDBInstance)
  if not userRole:
    userRole = 'student'
  userCredentials = {
    'email': email,
    'userRole': userRole,
    'password': password
  }

  response = ResponseCreation.ControllerResponse()
  token = MentiiAuth.generateAuthToken(userCredentials, appSecret)
  response.addToPayload('token', token)
  flaskResponse = ResponseCreation.createResponse(response, status)

  logger.info(str(flaskResponse))
  return flaskResponse

@app.route('/user/classes/', methods=['GET', 'OPTIONS'])
@auth.login_required
@handleOptionsRequest
def class_list():
  status = 200
  dynamoDBInstance = getDatabaseClient()
  res = class_ctrl.getActiveClassList(dynamoDBInstance)
  if res.hasErrors():
    status = 400
  return ResponseCreation.createResponse(res, status)

@app.route('/user/classes/', methods=['POST'])
@auth.login_required
def joinClass():
  status = 200
  dynamoDBInstance = getDatabaseClient()
  res = user_ctrl.joinClass(request.json, dynamoDBInstance)
  if res.hasErrors():
    status = 400
  return ResponseCreation.createResponse(res, status)

@app.route('/teacher/classes/', methods=['GET', 'OPTIONS'])
@auth.login_required
@handleOptionsRequest
def taughtClassList():
  status = 200
  res = ResponseCreation.ControllerResponse()
  role = g.authenticatedUser['userRole']
  if role != 'teacher' and role != 'admin' :
    res.addError('Role error', 'Only teachers can view a list of classes they are teaching')
    status = 403
  else:
    dynamoDBInstance = getDatabaseClient()
    res = class_ctrl.getTaughtClassList(dynamoDBInstance)
    if res.hasErrors():
      status = 400
  return ResponseCreation.createResponse(res, status)

@app.route('/class', methods=['POST', 'OPTIONS'])
@auth.login_required
@handleOptionsRequest
def create_class():
  status = 200

  role = g.authenticatedUser['userRole']
  if role != "teacher" and role != "admin" :
    res = ResponseCreation.ControllerResponse()
    res.addError('Role error', 'Only teachers can create classes')
    status = 403
  else:
    dynamoDBInstance = getDatabaseClient()
    res = class_ctrl.createClass(dynamoDBInstance, request.json)
    if res.hasErrors():
      status = 400
  return ResponseCreation.createResponse(res, status)

@app.route('/classes/', methods=['GET', 'OPTIONS'])
@auth.login_required
@handleOptionsRequest
def public_class_list():
  status = 200
  dynamoDBInstance = getDatabaseClient()
  res = class_ctrl.getPublicClassList(dynamoDBInstance)
  if res.hasErrors():
    status = 400
  return ResponseCreation.createResponse(res, status)

@app.route('/classes/<classCode>', methods=['GET', 'OPTIONS'])
@auth.login_required
@handleOptionsRequest
def getClass(classCode):
  status = 200
  dynamoDBInstance = getDatabaseClient()
  res = class_ctrl.getClass(classCode, dynamoDBInstance)
  if res.hasErrors():
    status = 400
  return ResponseCreation.createResponse(res, status)

@app.route('/admin/changerole/', methods=['POST', 'OPTIONS'])
@auth.login_required
@handleOptionsRequest
def changeUserRole():
  status = 200

  res = ResponseCreation.ControllerResponse()
  if g.authenticatedUser['userRole'] != "admin":
    res.addError('Role Error', 'Only admins can change user roles')
    status = 403
  else:
    dynamoDBInstance = getDatabaseClient()
    res = user_ctrl.changeUserRole(request.json, dynamoDBInstance)
    if res.hasErrors():
      status = 400
  return ResponseCreation.createResponse(res,status)

@app.route('/problem/<classId>/<activity>/', methods=['GET', 'OPTIONS'])
@auth.login_required
@handleOptionsRequest
def problemSteps(classId, activity):
  status = 200
  dynamoDBInstance = getDatabaseClient()
  problem = problem_ctrl.getProblemTemplate(classId, activity, dynamoDBInstance)
  res = algebra.getProblemTree(problem)
  if res.hasErrors():
    status = 400
  return ResponseCreation.createResponse(res,status)

@app.route('/classes/remove', methods=['POST', 'OPTIONS'])
@auth.login_required
@handleOptionsRequest
def removeStudentFromClass():
  status = 200
  role = g.authenticatedUser['userRole']
  if role != "teacher" and role != "admin" :
    res = ResponseCreation.ControllerResponse()
    res.addError('Role error', 'Only those with teacher privileges can remove students from classes')
    status = 403
  else:
    dynamoDBInstance = getDatabaseClient()
    res = class_ctrl.removeStudent(dynamoDBInstance, request.json)
    if res.hasErrors():
      status = 400
    else:
      #send email
      class_ctrl.sendClassRemovalEmail(dynamoDBInstance, mail, request.json)
  return ResponseCreation.createResponse(res, status)

@app.route('/book', methods=['POST', 'OPTIONS'])
@auth.login_required
@handleOptionsRequest
def createBook():
  status = 200
  res = ResponseCreation.ControllerResponse()
  if g.authenticatedUser['userRole'] != "admin":
    res.addError('Role Error', 'Only admins can create books')
    status = 403
  else:
    dynamoDBInstance = getDatabaseClient()
    res = book_ctrl.createBook(request.json, dynamoDBInstance)
    if res.hasErrors():
      status = 400
  return ResponseCreation.createResponse(res,status)

@app.route('/class/details/update', methods=['POST', 'OPTIONS'])
@auth.login_required
@handleOptionsRequest
def updateClassDetails():
  status = 200
  res = ResponseCreation.ControllerResponse()
  role = g.authenticatedUser['userRole']
  if role != 'admin' and role != 'teacher':
    res.addError('Role Error', 'Only teachers or admins can update class details')
    status = 403
  else:
    dynamoDBInstance = getDatabaseClient()
    res = class_ctrl.updateClassDetails(request.json, dynamoDBInstance)
    if res.hasErrors():
      status = 400
  return ResponseCreation.createResponse(res,status)

@app.route('/forgotPassword/', methods=['POST', 'OPTIONS'])
@handleOptionsRequest
def forgotPassword():
  status = 200
  res = ResponseCreation.ControllerResponse()
  dynamoDBInstance = getDatabaseClient()
  httpOrigin = request.environ.get('HTTP_ORIGIN')
  res = user_ctrl.sendForgotPasswordEmail(httpOrigin, request.json, mail, dynamoDBInstance)
  return ResponseCreation.createResponse(res,status)


if __name__ == '__main__':
  logger.info('mentii app starting')
  try:
    app.run(host='0.0.0.0', debug=False, threaded=True)
  except Exception as e:
    logger.exception(e)
  logger.warning('mentii app down')
