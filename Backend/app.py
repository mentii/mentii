#!env/bin/python

from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from flask_mail import Mail
from mentii import user_ctrl
import ConfigParser as cp

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
mail = Mail(app)

#Parse any external configuration options
parser = cp.ConfigParser()
parser.read("config/prodConfig.ini")

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
        response = user_ctrl.register(request.json, mail)
        return jsonify(response)
    else:
        return "Success"

@app.route('/activate/<activationid>', methods=['GET'])
def activate(activationid):
	response = user_ctrl.activate(activationid)
	return response

'''
#Testing reading from the database
@app.route('/users/', methods=['GET'])
def users():
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table('users')
    response = table.get_item(
        Key={
            'email': 'jtm333@drexel.edu'
        }
    )
    return jsonify(response)
'''

'''
#testing reading url parameters
@app.route('/activate/<uuid>', methods=['GET'])
def activate(uuid):
    return uuid
'''

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
