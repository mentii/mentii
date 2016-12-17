#!env/bin/python

from flask import Flask, request, jsonify, Response
from flask_cors import CORS, cross_origin
from flask_mail import Mail
from flask.ext.httpauth import HTTPBasicAuth
from flask import g
from mentii import user_ctrl
from utils.MentiiAuth import MentiiAuthentication
import utils.ResponseCreation as cr
from utils.ResponseCreation import ControllerResponse
import ConfigParser as cp
import boto3
import sys

from boto3.dynamodb.conditions import Key, Attr
import hashlib


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

#Email setup
address = parser.get('EmailData', 'address')
password = parser.get('EmailData', 'password')

#Database configuration
prod = parser.get('DatabaseData', 'isProd')
print("prod: " + str(prod))

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
    return boto3.resource('dynamodb')
  else:
    print("Returning the Dev resource")
    return boto3.resource('dynamodb', endpoint_url='http://localhost:8000')

@auth.verify_password
def verify_password(email_or_token, password):
  ma = MentiiAuthentication()
  user = ma.verify_auth_token(email_or_token)
  if not user:
    if email_or_token == '' or password == '':
      return False
    dynamodb = getDatabaseClient()
    table = dynamodb.Table('users')
    result = table.get_item(Key={'email': email_or_token}, AttributesToGet=['active', 'password'])
    if 'Item' not in result:
      return False
    if result['Item']['active'] != 'T':
      return False
    hashedPassword = result['Item']['password']
    testPassword = hashlib.md5(password).hexdigest()
    if hashedPassword != testPassword:
      return False
    else:
      g.authenticated_user = result['Item']
  else:
    g.authenticated_user = user
  return True

@app.route('/', methods=['GET', 'POST'])
def index():
  return cr.createEmptyResponse(200)

@app.route('/register/', methods=['POST', 'OPTIONS'])
def register():
  if request.method =='POST':
    dynamoDBInstance = getDatabaseClient()
    res = user_ctrl.register(request.json, mail, dynamoDBInstance)
    if not res.hasErrors():
      return cr.createResponse(res, 201)
    else:
      return cr.createResponse(res, 400)
  else:
    return cr.createEmptyResponse(200)

@app.route('/activate/<activationid>', methods=['GET'])
def activate(activationid):
  dynamoDBInstance = getDatabaseClient()
  res = user_ctrl.activate(activationid, dynamoDBInstance)
  if not res.hasErrors():
    return cr.createResponse(res, 200)
  else:
    return cr.createResponse(res, 400)

@app.route('/signin/', methods=['POST', 'OPTIONS'])
@auth.login_required
def signin():
  if request.method =='POST':
    user_credentials = {'email': request.authorization.username, 'password': request.authorization.password}
    response = ControllerResponse()
    ma = MentiiAuthentication()
    token = ma.generate_auth_token(user_credentials)
    response.addToPayload('token', token)
    return cr.createResponse(response, 200)
  else:
    return cr.createEmptyResponse(200)

@app.route('/secure/', methods=['POST', 'OPTIONS'])
@auth.login_required
def secure():
  '''
  This is an endpoint for testing authentication
  '''
  if request.method =='POST':
    # Do ya thang for the endpoint here. call another class/function etc
    # testing function just returns data on the authenticated user
    response = ControllerResponse()
    response.addToPayload('data', g.authenticated_user)
    return cr.createResponse(response, 200)
  else:
    return cr.createEmptyResponse(200)

if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=False)
