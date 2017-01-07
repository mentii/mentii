import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

def createTableFromFile(settings_file, dbInstance):
  try:
    with open(settings_file) as f:
      data = f.read()
      settings = json.loads(data)

      attribute_definitions = settings.get("AttributeDefinitions")
      key_schema = settings.get("KeySchema")
      provisioned_throughput = settings.get("ProvisionedThroughput")
      table_name = settings.get("TableName")

      # check for required parameters
      if table_name is not None and key_schema is not None and attribute_definitions is not None and provisioned_throughput is not None:
        if len(key_schema) > 0 and len(attribute_definitions) > 0:
          table = dbInstance.create_table(
              AttributeDefinitions=attribute_definitions,
              KeySchema=key_schema,
              ProvisionedThroughput=provisioned_throughput,
              TableName=table_name
            )
          f.close()
          return table
      f.close()
      raise(IOError)
  except IOError as e:
    print(e)
    return "Unable to create table"

def createTableFromJson(settings_json, dbInstance):
  if (type(settings_json) == str):
    settings = json.loads(settings_json)
  else:
    settings = settings_json

  attribute_definitions = settings.get("AttributeDefinitions")
  key_schema = settings.get("KeySchema")
  provisioned_throughput = settings.get("ProvisionedThroughput")
  table_name = settings.get("TableName")

  # check for required parameters
  if table_name is not None and key_schema is not None and attribute_definitions is not None and provisioned_throughput is not None:
    if len(key_schema) > 0 and len(attribute_definitions) > 0:
      table = dbInstance.create_table(
          AttributeDefinitions=attribute_definitions,
          KeySchema=key_schema,
          ProvisionedThroughput=provisioned_throughput,
          TableName=table_name
        )
      return table
  return "Unable to create table"

def preloadDataFromFile(fileName, table):
  try:
    with open(fileName) as json_file:
      data = json_file.read()
      items = json.loads(data)
      for item in items:
        if "email" in item.keys() and "password" in item.keys() and "activationId" in item.keys() and "active" in item.keys():
          email = item['email']
          password = item['password']
          activationId = item['activationId']
          active = item['active']

          table.put_item(
            Item={
               'email': email,
               'password': password,
               'activationId': activationId,
               'active': active
            }
          )
        else:
          print("Unable to add item to table " + table.describe_table + ". Missing email or password")
  except IOError as e:
    print("Unable to load data into table")
    print(e)

def preloadDataFromJson(jsonData, table):
  if (type(jsonData) == str):
    items = json.loads(jsonData)
  else:
    items = jsonData
  try:
    for item in items:
      if "email" in item.keys() and "password" in item.keys() and "activationId" in item.keys() and "active" in item.keys():
        email = item['email']
        password = item['password']
        activationId = item['activationId']
        active = item['active']

        table.put_item(
          Item={
            'email': email,
            'password': password,
            'activationId': activationId,
            'active': active
          }
        )
      else:
        print("Unable to add item to table " + table.describe_table + ". Missing email or password")
  except:
    print("Unable to load data into table")

def getTable(tableName, dbInstance):
  return dbInstance.Table(tableName)

def putItem(jsonData, table):
  if (type(jsonData) == str):
    item = json.loads(jsonData)
  else:
    item = jsonData
  response = table.put_item(Item=item)
  return response

def getItem(jsonData, table):
  if (type(jsonData) == str):
    data = json.loads(jsonData)
  else:
    data = jsonData

  attributes_to_get = data.get("AttributesToGet")
  key = data.get("Key")

  response = table.get_item(Key=key,AttributesToGet=attributes_to_get)
  return response

def updateItem(jsonData, table):
  if (type(jsonData) == str):
    data = json.loads(jsonData)
  else:
    data = jsonData

  key = data.get("Key")
  update_expression = data.get("UpdateExpression")
  expression_attribute_values = data.get("ExpressionAttributeValues")
  return_values = data.get("ReturnValues")

  response = table.update_item(
    Key=key,
    UpdateExpression=update_expression,
    ExpressionAttributeValues=expression_attribute_values,
    ReturnValues=return_values
  )
  return response

def deleteItem(keys, table):
  if (type(keys) == str):
    key = json.loads(keys)
  else:
    key = keys
  response = table.delete_item(Key=key)
  return response

def query(key, query, table):
  response = table.query(KeyConditionExpression=Key(key).eq(query))
  return response

def scan(attributeName, attribute, table):
  #check for primary key
  return table.scan(FilterExpression=Attr(attributeName).eq(attribute))

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

  d = '{ "email" : "fire@test.com", "password": "passwerd" }'
  k = '{ "email" : "test2@mentii.com"}'
  print(putItem(d, table))
  response = getItem(k,table)
  print(response['Item']['password'])