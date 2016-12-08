import boto3
import re
from flask_mail import Message
from boto3.dynamodb.conditions import Key, Attr
import uuid

def register(jsonData, mailer):
	if not validateRegistration(jsonData):
		return 'Failing Registration Validation'
	return addUser(getEmail(jsonData), getPassword(jsonData), mailer)

def validateRegistration(jsonData):
    '''
    Validate the email address and password
    for a user.  
    '''
    try:
        email = getEmail(jsonData)
        #Emails must have only one @ and at least one . after the @
        emailRegex = re.compile(r"[^@]+@[^@]+\.[^@]+")
        if not emailRegex.match(email):
            return False 

        if isEmailInSystem(email):
            return False
        
        password = getPassword(jsonData)
        #Passwords must be at least 8 characters
        if len(password) < 8: 
            return False

        return True
    except Exception as e:
        print e
        return False

def getEmail(jsonData):
    return jsonData['email']

def getPassword(jsonData):
    return jsonData['password']

def addUser(email, password, mailer):
	activationId = str(uuid.uuid4())
	dynamodb = boto3.resource('dynamodb')
	table = dynamodb.Table('users')
	#this will change an existing user withthe same email.
	#TODO:we need enforce uniqueness on email
	response = table.put_item(
		Item={
			'email': email,
			'password': password,
			'activationId': activationId
		}
	)
	#TODO:send email with activation link here
	#currently this is returning the activationId for testing but once the email
	#is working it should just return a success message
        sendEmail(email, activationId, mailer)
	return activationId

def sendEmail(email, activationId, mailer):
    '''
    Create a message and send it from our email to 
    the passed in email. The message should contain 
    a link built with the activationId
    '''
    #Build Message
    msg = Message('Mentii: Thank You for Creating an Account!', sender = 'mentiiapp@gmail.com', recipients=[email])
    msg.body = "Here is your activationId link: api.mentii.me/activate/{}".format(activationId)
    #Send Email
    mailer.send(msg)

def isEmailInSystem(email):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('users')
    result = table.get_item(Key={'email': email})
    #Result is a dictionary that will have the key Item if 
    # it was able to find an item.
    return "Item" in result.keys()


def activate(activationId):
	dynamodb = boto3.resource('dynamodb')
	table = dynamodb.Table('users')
        email = ''
        #Scan for the email associated with this activationId
        scanResponse = table.scan(FilterExpression=Attr('activationId').eq(activationId))
        if scanResponse is not None:
            #scanResponse is a dictionary that has a list of 'Items'
            items = scanResponse['Items']
            if len(items) != 1:
                return "Error!!"
            email = items[0]['email']
        #Update using the email we have
	response = table.update_item(
	    Key={
	        'email': email,
	    },
	    UpdateExpression="SET active = :a, activationId = :aid",
	    ExpressionAttributeValues={
	        ':a': 'T',
	        ':aid': 'none'
	    },
	    ReturnValues='UPDATED_NEW'
	)
	return "Success"
