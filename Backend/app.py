#!env/bin/python

from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from flask_mail import Mail
from mentii import user_ctrl
import ConfigParser as cp
import boto3

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
mail = Mail(app)

#Parse any external configuration options
parser = cp.ConfigParser()
parser.read("/config/prodConfig.ini")

#Email setup
address = parser.get('EmailData', 'address')
password = parser.get('EmailData', 'password')

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = address
app.config['MAIL_DEFAULT_SENDER'] = address
app.config['MAIL_PASSWORD'] = password
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

@app.route('/', methods=['GET', 'POST'])
def index():
  return "hello from flask"

@app.route('/register/', methods=['POST', 'OPTIONS'])
def register():
  if request.method =='POST':
    dynamoDBInstance = boto3.resource('dynamodb')
    response = user_ctrl.register(request.json, mail, dynamoDBInstance)
    return jsonify(response)
  else:
    return "Success"

@app.route('/activate/<activationid>', methods=['GET'])
def activate(activationid):
  dynamoDBInstance = boto3.resource('dynamodb')
  response = user_ctrl.activate(activationid, dynamoDBInstance)
  return response

if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=False)
