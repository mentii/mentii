#!env/bin/python

from flask import Flask, request, jsonify, Response
from flask_cors import CORS, cross_origin
from flask_mail import Mail
from mentii import user_ctrl
import utils.ResponseCreation as cr
import ConfigParser as cp
import boto3
import sys


app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
mail = Mail(app)

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
def signin():
  if request.method =='POST':
    return cr.createEmptyResponse(200)
  else:
    return cr.createEmptyResponse(200)

if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=False)
