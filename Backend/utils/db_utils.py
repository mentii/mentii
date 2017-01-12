import json
import boto3
import MentiiLogging as MentiiLogging
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

logger = MentiiLogging.getLogger()

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
  except IOError as e:
    message = "Unable to create table from file"
    logger.exception(message + ': ' + settings_file + '\n' + str(e))
    return None

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
  message = "Unable to create table from json"
  logger.error(message)
  return None

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
          codes = item['codes']

          table.put_item(
            Item={
               'email': email,
               'password': password,
               'activationId': activationId,
               'active': active,
               'codes': codes
            }
          )
        else:
          message = "Unable to add item to table " + table.describe_table + ". Missing email, password, activationId, or active status"
          logger.error(message)
      json_file.close()
  except IOError as e:
    message = "Unable to open file"
    logger.exception(message + ': ' + settings_file + '\n' + str(e))
    return None

def preloadClassData(jsonData, table):
  try:
    with open(jsonData) as json_file:
      data = json_file.read()
      items = json.loads(data)
      for item in items:
        code = item['code']
        title = item['title']
        subtitle = item['subtitle']
        description = item['description']

        table.put_item(
          Item={
            'code': code,
            'title': title,
            'subtitle' : subtitle,
            'description' : description
          }
        )
  except IOError as e:
    message = "Unable to load data into table"
    MentiiLogging.getLogger().exception(message + '\nJSON:\n' + jsonData + '\n' + str(e))
    return message

def preloadDataFromJson(jsonData, table):
  if (type(jsonData) == str):
    items = json.loads(jsonData)
  else:
    items = jsonData

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
      message = "Unable to add item to table " + table.describe_table + ". Missing email, password, activationId, or active status"
      logger.error(message)

def getTable(tableName, dbInstance):
  try:
    table = dbInstance.Table(tableName)
    status = table.table_status
    return table
  except ClientError as e:
    message = "Unable to get table " + tableName + ". Table does not exist"
    logger.exception(message + '\n' + str(e))
    return None

#Note putItem can overwrite data with the same key
def putItem(jsonData, table):
  if (type(jsonData) == str):
    item = json.loads(jsonData)
  else:
    item = jsonData

  if item is None:
    message = "Unable to put item. Missing Key"
    logger.error(message)
    return None

  response = table.put_item(Item=item)
  return response

def getItem(jsonData, table):
  if (type(jsonData) == str):
    data = json.loads(jsonData)
  else:
    data = jsonData

  attributes_to_get = data.get("AttributesToGet")
  key = data.get("Key")

  if key is None:
    message = "Unable to get item. Missing Key"
    logger.error(message)
    return None

  if attributes_to_get is not None:
    response = table.get_item(Key=key,AttributesToGet=attributes_to_get)
  else:
    response = table.get_item(Key=key)
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

  if key is None:
    message = "Unable to update item. Missing Key"
    logger.error(message)
    return None

  if update_expression is not None and expression_attribute_values is not None and return_values is not None:
    response = table.update_item(
      Key=key,
      UpdateExpression=update_expression,
      ExpressionAttributeValues=expression_attribute_values,
      ReturnValues=return_values
    )
    return response
  else:
    response = table.update_item(Key=key)
    return response

def deleteItem(keys, table):
  if (type(keys) == str):
    key = json.loads(keys)
  else:
    key = keys

  if key is None:
    message = "Unable to delete item. Missing Key"
    logger.error(message)
    return None

  response = table.delete_item(Key=key)
  return response

def query(key, query, table):
  response = table.query(KeyConditionExpression=Key(key).eq(query))
  return response

def scan(table):
  return table.scan()

def scanFilter(attributeName, attribute, table):
  return table.scan(FilterExpression=Attr(attributeName).eq(attribute))

def deleteTable(tableName, dbInstance):
  try:
    table = dbInstance.Table(tableName)
    status = table.table_status
    table.delete()
  except ClientError as e:
    message = "Unable to delete table " + tableName + ". Table does not exist"
    logger.exception(message + '\n' + str(e))
