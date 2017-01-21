#!env/bin/python

from flask import Flask, request, jsonify, Response
from flask_cors import CORS, cross_origin
from flask_mail import Mail
from flask_httpauth import HTTPBasicAuth
from flask import g
from mentii import user_ctrl
from mentii import class_ctrl
from utils import MentiiAuth
import utils.ResponseCreation as ResponseCreation
from utils.ResponseCreation import ControllerResponse
import utils.MentiiLogging as MentiiLogging
import ConfigParser as cp
import boto3
import sys


app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
mail = Mail(app)
auth = HTTPBasicAuth()

#Configuration setup
configPath = "/config/prodConfig.ini"
if len(sys.argv) == 2:
  configPath = sys.argv[1]

#Parse any external configuration options
parser = cp.ConfigParser()
parser.read(configPath)

logPath = parser.get('MentiiData', 'path') + '/logs'
MentiiLogging.setupLogger(logPath)
logger = MentiiLogging.getLogger()

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
def register():
  logger.info(str(request))
  status = 200
  if request.method =='OPTIONS':
    flaskResponse = ResponseCreation.createEmptyResponse(status)
    logger.info(str(flaskResponse))
    return flaskResponse
  dynamoDBInstance = getDatabaseClient()
  res = user_ctrl.register(request.json, mail, dynamoDBInstance)
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
  dynamoDBInstance = getDatabaseClient()
  role = user_ctrl.getRole(email, dynamoDBInstance)
  userCredentials = {
    'email': email,
    'password': request.authorization.password,
    'role': role
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

@app.route('/class', methods=['POST', 'OPTIONS'])
@auth.login_required
def create_class():
  status = 200
  if request.method =='OPTIONS':
    return ResponseCreation.createEmptyResponse(status)

  if g.authenticatedUser['role'] == "student":
    res = ResponseCreation.ControllerResponse()
    res.addError("Role error", "Students cannot create classes")
    status = 403
  else:
    dynamoDBInstance = getDatabaseClient()
    res = class_ctrl.createClass(dynamoDBInstance, request.json)
    if res.hasErrors():
      status = 400
  return ResponseCreation.createResponse(res, status)

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

@app.route('/admin/changerole/', methods=['POST', 'OPTIONS'])
@auth.login_required
def changeUserRole():
  status = 200
  if request.method =='OPTIONS':
    return ResponseCreation.createEmptyResponse(status)

  if g.authenticatedUser['role'] != "admin":
    res = ResponseCreation.ControllerResponse()
    res.addError('Role Error', 'Only admins can change user roles')
    status = 403
  else:
    dynamoDBInstance = getDatabaseClient()
    res = user_ctrl.changeUserRole(request.json, dynamoDBInstance)
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
