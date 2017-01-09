import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
import utils.MentiiLogging as MentiiLogging

def createTableFromFile(settings_file, dbInstance):
  try:
    with open(settings_file) as f:
      data = f.read()
      settings = json.loads(data)
      if "table_name" in settings.keys() and "key_schema" in settings.keys() and "attribute_definitions" in settings.keys() and "provisioned_throughput" in settings.keys():
        if len(settings["key_schema"]) > 0 and len(settings["attribute_definitions"]) > 0:
          table = dbInstance.create_table(
            TableName=settings["table_name"],
            KeySchema=settings["key_schema"],
            AttributeDefinitions=settings["attribute_definitions"],
            ProvisionedThroughput=settings["provisioned_throughput"]
          )
          f.close()
          return table
      f.close()
      raise(IOError)
  except IOError as e:
    message = "Unable to create table from file"
    logger = MentiiLogging.getLogger()
    logger.exception(message + ': ' + settings_file + '\n' + str(e))
    return message

def createTableFromJson(settings_json, dbInstance):
  if (type(settings_json) == str):
    settings = json.loads(settings_json)
  else:
    settings = settings_json
  if "table_name" in settings.keys() and "key_schema" in settings.keys() and "attribute_definitions" in settings.keys() and "provisioned_throughput" in settings.keys():
    if len(settings["key_schema"]) > 0 and len(settings["attribute_definitions"]) > 0:
      table = dbInstance.create_table(
        TableName=settings["table_name"],
        KeySchema=settings["key_schema"],
        AttributeDefinitions=settings["attribute_definitions"],
        ProvisionedThroughput=settings["provisioned_throughput"]
      )
      return table
  message = "Unable to create table"
  logger.error(message)
  return message

def getTable(tableName, dbInstance):
  return dbInstance.Table(tableName)

def preloadData(jsonData, table):
  try:
    with open(jsonData) as json_file:
      data = json_file.read()
      items = json.loads(data)
      for item in items:
        email = item['email']
        password = item['password']
        active = item['active']
        activationId = item['activationId']

        table.put_item(
          Item={
            'email': email,
            'password': password,
            'active' : active,
            'activationId' : activationId
          }
        )
  except IOError as e:
    message = "Unable to load data into table"
    logger = MentiiLogging.getLogger()
    logger.exception(message + '\nJSON:\n' + jsonData + '\n' + str(e))
    return message

def addItem(jsonData, table):
  #check for primary key
  item = json.loads(jsonData)
  return table.put_item(Item=item)

def getItem(keys, table):
  #check for primary key
  key = json.loads(keys)
  return table.get_item(Key=key)

def updateItem(keys, table):
  #check for primary key
  key = json.loads(keys)
  return table.update_item(Key=key)

def deleteItem(keys, table):
  #check for primary key
  key = json.loads(keys)
  return table.delete_item(Key=key)

def query(key, query, table):
  #check for primary key
  return table.query(KeyConditionExpression=Key(key).eq(query))

def scan(filterExpression, table):
  fe = filterExpression
  #check for primary key
  return table.scan(FilterExpression=fe)

def deleteTable(table):
  return table.delete()

if __name__ == '__main__':
  dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')
  getTable('users', dynamodb).delete()

  jsonData = '{\
    "table_name" :"users",\
    "key_schema":[\
      {\
        "AttributeName": "email",\
        "KeyType": "HASH"\
      }\
    ],\
    "attribute_definitions":[\
      {\
        "AttributeName": "email",\
        "AttributeType": "S"\
      }\
    ],\
    "provisioned_throughput":{\
      "ReadCapacityUnits": 5,\
      "WriteCapacityUnits": 5\
    }\
  }'

  table = createTableFromJson(jsonData,dynamodb)
  #table = createTableFromFile("table_settings.json", dynamodb)
  print(table.table_status)
  preloadData("mock_data.json", table)

  d = '{ "email" : "fire@mentii.me", "password": "passwerd" }'
  k = '{ "email" : "test2@mentii.me"}'
  print(addItem(d, table))
  response = getItem(k,table)
  print(response['Item']['password'])
