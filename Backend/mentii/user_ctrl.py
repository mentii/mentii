import boto3
import json
from boto3.dynamodb.conditions import Key, Attr
import uuid

def register(json):
	if not validateReg(json):
		return 'Bad Request'
	return addUser(getEmail(json), getPassword(json))

def validateReg(json):
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
	activationid = str(uuid.uuid4())
	dynamodb = boto3.resource('dynamodb')
	table = dynamodb.Table('users')
	#this will change an existing user withthe same email.
	#TODO:we need enforce uniqueness on email
	response = table.put_item(
		Item={
			'email': email,
			'password': password,
			'activationid': activationid
		}
	)
	#TODO:send email with activation link here
	#currently this is returning the activationid for testing but once the email
	#is working it should just return a success message
	return activationid

def activate(activationid):
	dynamodb = boto3.resource('dynamodb')
	table = dynamodb.Table('users')
	response = table.update_item(
	    Key={
	        'activationid': activationid,
	    },
		UpdateExpression="set userItem.active = :a, userItem.activationid = :aid",
	    ExpressionAttributeValues={
	        ':a': 'T',
			':aid': None
	    },
		ReturnValues='UPDATED_NEW'
	)
	return response
