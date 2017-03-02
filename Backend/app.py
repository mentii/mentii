#!env/bin/python

from flask import Flask, request, jsonify, Response
from flask_cors import CORS, cross_origin
from flask_mail import Mail
from flask_httpauth import HTTPBasicAuth
from flask import g
from mentii import user_ctrl
from mentii import class_ctrl
from mentii import problem_ctrl
from problems import mathstepsWrapper
from problems import algebra
from utils import MentiiAuth
from utils.ResponseCreation import ControllerResponse
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

def updateRoleDecorate(func):
  def updateResponseWithRole(response):
    userEmail = request.authorization.username
    role = user_ctrl.getRole(userEmail, getDatabaseClient())
    print(role)
    response.updateUserRole(role)
    return response
  return updateResponseWithRole

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
def register():
  logger.info(str(request))
  status = 200
  if request.method =='OPTIONS':
    flaskResponse = ResponseCreation.createEmptyResponse(status)
    logger.info(str(flaskResponse))
    return flaskResponse
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
def signin():
  logger.info(str(request))
  status = 200
  if request.method =='OPTIONS':
    flaskResponse = ResponseCreation.createEmptyResponse(status)
    logger.info(str(flaskResponse))
    return flaskResponse

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

  response = ControllerResponse()
  token = MentiiAuth.generateAuthToken(userCredentials, appSecret)
  response.addToPayload('token', token)
  flaskResponse = ResponseCreation.createResponse(response, status)

  logger.info(str(flaskResponse))
  return flaskResponse

@app.route('/secure/', methods=['POST', 'OPTIONS'])
@auth.login_required
def secure():
  '''
  This is an endpoint for testing authentication
  '''
  logger.info(str(request))
  status = 200
  if request.method =='OPTIONS':
    flaskResponse = ResponseCreation.createEmptyResponse(status)
    logger.info(str(flaskResponse))
    return flaskResponse
    # Do ya thang for the endpoint here. call another class/function etc
    # testing function just returns data on the authenticated user
  response = ControllerResponse()
  response.addToPayload('user', g.authenticatedUser)
  flaskResponse = ResponseCreation.createResponse(response, status)
  logger.info(str(flaskResponse))
  return flaskResponse

@updateRoleDecorate
@app.route('/user/classes/', methods=['GET', 'OPTIONS'])
@auth.login_required
def class_list():
  status = 200
  if request.method =='OPTIONS':
    return ResponseCreation.createEmptyResponse(status)
  dynamoDBInstance = getDatabaseClient()
  res = class_ctrl.getActiveClassList(dynamoDBInstance)
  if res.hasErrors():
    status = 400
  return ResponseCreation.createResponse(res, status)

@updateRoleDecorate
@app.route('/user/classes/', methods=['POST'])
@auth.login_required
def joinClass():
  status = 200
  dynamoDBInstance = getDatabaseClient()
  res = user_ctrl.joinClass(request.json, dynamoDBInstance)
  if res.hasErrors():
    status = 400
  return ResponseCreation.createResponse(res, status)

@updateRoleDecorate
@app.route('/teacher/classes/', methods=['GET', 'OPTIONS'])
@auth.login_required
def taughtClassList():
  status = 200
  if request.method =='OPTIONS':
    return ResponseCreation.createEmptyResponse(status)
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

@updateRoleDecorate
@app.route('/class', methods=['POST', 'OPTIONS'])
@auth.login_required
def create_class():
  status = 200
  if request.method =='OPTIONS':
    return ResponseCreation.createEmptyResponse(status)

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

@updateRoleDecorate
@app.route('/classes/', methods=['GET', 'OPTIONS'])
@auth.login_required
def public_class_list():
  status = 200
  if request.method =='OPTIONS':
    return ResponseCreation.createEmptyResponse(status)
  dynamoDBInstance = getDatabaseClient()
  res = class_ctrl.getPublicClassList(dynamoDBInstance)
  if res.hasErrors():
    status = 400
  return ResponseCreation.createResponse(res, status)

@updateRoleDecorate
@app.route('/classes/<classCode>', methods=['GET', 'OPTIONS'])
@auth.login_required
def getClass(classCode):
  status = 200
  if request.method =='OPTIONS':
    return ResponseCreation.createEmptyResponse(status)
  dynamoDBInstance = getDatabaseClient()
  res = class_ctrl.getClass(classCode, dynamoDBInstance)
  if res.hasErrors():
    status = 400
  return ResponseCreation.createResponse(res, status)

@app.route('/admin/changerole/', methods=['POST', 'OPTIONS'])
@auth.login_required
def changeUserRole():
  status = 200
  if request.method =='OPTIONS':
    return ResponseCreation.createEmptyResponse(status)

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

@app.route('/ms-test/', methods=['POST', 'OPTIONS'])
def mathsteps():
  status = 200
  if request.method =='OPTIONS':
    return ResponseCreation.createEmptyResponse(status)
  res = ResponseCreation.ControllerResponse()
  problem = request.json['problem']
  steps = mathstepsWrapper.getStepsForProblem(problem)
  res.addToPayload('steps', steps)
  if res.hasErrors():
    status = 400
  return ResponseCreation.createResponse(res,status)

@app.route('/ms-bad-test/', methods=['POST', 'OPTIONS'])
def badsteps():
  status = 200
  if request.method =='OPTIONS':
    return ResponseCreation.createEmptyResponse(status)
  res = ResponseCreation.ControllerResponse()
  problem = request.json['problem']
  steps = mathstepsWrapper.getStepsForProblem(problem)
  respon = algebra.generateTreeWithBadSteps(steps,3)
  res.addToPayload('steps', respon)
  if res.hasErrors():
    status = 400
  return ResponseCreation.createResponse(res,status)

@app.route('/problem/<classId>/<activity>/', methods=['GET', 'OPTIONS'])
@auth.login_required
def problemSteps(classId, activity):
  status = 200
  problem = problem_ctrl.getProblemTemplate(classId, activity)
  res = algebra.getProblemTree(problem)
  if res.hasErrors():
    status = 400
  return ResponseCreation.createResponse(res,status)

if __name__ == '__main__':
  logger.info('mentii app starting')
  try:
    app.run(host='0.0.0.0', debug=False, threaded=True)
  except Exception as e:
    logger.exception(e)
  logger.warning('mentii app down')
