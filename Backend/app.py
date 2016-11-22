#!env/bin/python
from flask import Flask, request, jsonify
from mentii import user_ctrl

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return "hello from flask"

@app.route('/register/', methods=['POST'])
def register():
    response = user_ctrl.register(request.json)
    return jsonify(response)

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
