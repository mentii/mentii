import boto3
import json
from boto3.dynamodb.conditions import Key, Attr

def register(json):
    if not validate(json):
        return "Bad Request"
    addUser(getEmail(json), getPassword(json))

def validate(json):
    try:
        email = json['email']
        password = json['password']
        return True
    except Exception as e:
        print e
        return False

def getEmail(json):
    return json['email']

def getPassword(json):
    return json['password']

def addUser(email, password):
        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table('users')
        response = table.put_item(
            Item={
                    'email': email,
                    'password': password,
                    'activated': 'N'
            }
        )
        return response
