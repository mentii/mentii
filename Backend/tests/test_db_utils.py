import unittest
import json
import boto3
import utils.MentiiLogging as MentiiLogging
from boto3.dynamodb.conditions import Key, Attr
from utils import db_utils as db

class DbUtilsTest(unittest.TestCase):

#################### Test Class Setup #################################

  @classmethod
  def setUpClass(self):
    self.settingsName = "./tests/table_settings_2.json"
    self.badSettingsName = "./tests/bad_table_settings.json"
    self.mockData = "./tests/mock_data_2.json"
    self.badMockData = "./tests/bad_mock_data.json"
    self.dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')
    self.dynamodbClient = boto3.client('dynamodb', endpoint_url='http://localhost:8000')

    #clean up local DB before tests
    tables = self.dynamodbClient.list_tables()
    tableNames = tables.get("TableNames")
    try:
      for name in tableNames:
        self.dynamodb.Table(name).delete()
    except:
      print("Error deleting tableNames")

  @classmethod
  def tearDownClass(self):
    #clean up local DB
    tables = self.dynamodbClient.list_tables()
    tableNames = tables.get("TableNames")
    try:
      for name in tableNames:
        self.dynamodb.Table(name).delete()
    except:
      print("Error deleting tableNames")

  def setUp(self):

    # create table
    setUpData = {
      "TableName" : "users",
      "KeySchema":[
        {
          "AttributeName": "email",
          "KeyType": "HASH"
        }
      ],
      "AttributeDefinitions":[
        {
          "AttributeName": "email",
          "AttributeType": "S"
        }
      ],
      "ProvisionedThroughput":{
        "ReadCapacityUnits": 5,
        "WriteCapacityUnits": 5
      }
    }

    attribute_definitions = setUpData.get("AttributeDefinitions")
    key_schema = setUpData.get("KeySchema")
    provisioned_throughput = setUpData.get("ProvisionedThroughput")
    table_name = setUpData.get("TableName")

    self.table = self.dynamodb.create_table(
      AttributeDefinitions=attribute_definitions,
      KeySchema=key_schema,
      ProvisionedThroughput=provisioned_throughput,
      TableName=table_name
    )

    self.table.wait_until_exists()

    # preload table with data
    items = [
      {
        "email" : "test@mentii.me",
        "password" : "iameight",
        "activationId" : "12345",
        "active": "T"
      },
      {
        "email" : "test2@mentii.me",
        "password" : "iameight2",
        "activationId" : "abcde",
        "active": "F"
      },
      {
        "email" : "test3@mentii.me",
        "password" : "6b7330782b2feb4924020cc4a57782a9",
        "activationId" : "abcde",
        "active": "T"
      },
      {
        "email" : "test4@mentii.me",
        "password" : "6b7330782b2feb4924020cc4a57782a9",
        "activationId" : "abcde",
        "active": "F"
      }
    ]

    for item in items:
      email = item['email']
      password = item['password']
      activationId = item['activationId']
      active = item['active']

      self.table.put_item(
        Item={
           'email': email,
           'password': password,
           'activationId': activationId,
           'active': active
        }
      )

  def tearDown(self):
    self.dynamodb.Table("users").delete()

#################### Table Creation Tests #################################

  def test_create_table_from_file(self):
    print("Running create_table_from_file test")
    table = db.createTableFromFile(self.settingsName, self.dynamodb)
    self.assertIsNotNone(table)
    self.assertEqual(table.table_status,"ACTIVE")
    self.assertEqual(table.table_name, "testusers")

  def test_create_table_from_file_fail(self):
    print("Running create_table_from_file test fail test case")
    table = db.createTableFromFile(self.badSettingsName, self.dynamodb)
    self.assertIsNone(table)

  def test_create_table_from_string(self):
    print("Running create_table_from_string test")
    jsonDataString = '{\
      "TableName" :"puppies",\
      "KeySchema":[\
        {\
          "AttributeName": "name",\
          "KeyType": "HASH"\
        }\
      ],\
      "AttributeDefinitions":[\
        {\
          "AttributeName": "name",\
          "AttributeType": "S"\
        }\
      ],\
      "ProvisionedThroughput":{\
        "ReadCapacityUnits": 3,\
        "WriteCapacityUnits": 3\
      }\
    }'

    tableFromString = db.createTableFromJson(jsonDataString, self.dynamodb)
    self.assertIsNotNone(tableFromString)
    self.assertEqual(tableFromString.table_status, "ACTIVE")
    self.assertEqual(tableFromString.table_name, "puppies")

  def test_create_table_from_string_fail(self):
    print("Running create_table_from_string fail test case")
    badJsonDataString = '{\
      "AttributeDefinitions":[\
        {\
          "AttributeName": "name",\
          "AttributeType": "S"\
        }\
      ],\
      "ProvisionedThroughput":{\
        "ReadCapacityUnits": 3,\
        "WriteCapacityUnits": 3\
      }\
    }'

    tableFromBadString = db.createTableFromJson(badJsonDataString, self.dynamodb)
    self.assertIsNone(tableFromBadString)

  def test_create_table_from_json(self):
    print("Running create_table_from_json test")
    jsonData = {
      "TableName" :"cats",
      "KeySchema":[
        {
          "AttributeName": "name",
          "KeyType": "HASH"
        }
      ],
      "AttributeDefinitions":[
        {
          "AttributeName": "name",
          "AttributeType": "S"
        }
      ],
      "ProvisionedThroughput":{
        "ReadCapacityUnits": 3,
        "WriteCapacityUnits": 3
      }
    }

    tableFromJson = db.createTableFromJson(jsonData, self.dynamodb)
    self.assertIsNotNone(tableFromJson)
    self.assertEqual(tableFromJson.table_status, "ACTIVE")
    self.assertEqual(tableFromJson.table_name, "cats")

  def test_create_table_from_json_fail(self):
    print("Running create_table_from_json fail test case")
    jsonBadData = {
      "KeySchema":[
        {
          "AttributeName": "name",
          "KeyType": "HASH"
        }
      ],
      "ProvisionedThroughput":{
        "ReadCapacityUnits": 3,
        "WriteCapacityUnits": 3
      }
    }

    tableFromJsonBad = db.createTableFromJson(jsonBadData, self.dynamodb)
    self.assertIsNone(tableFromJsonBad)

#################### Preload Data Tests #################################

  def test_preload_data_from_file(self):
    print("Running preload_data_from_file test")
    self.assertIsNotNone(self.table)
    self.assertEqual(self.table.table_status,"ACTIVE")

    db.preloadDataFromFile(self.mockData, self.table)
    self.assertIsNotNone(self.table.get_item(Key={"email":"test@mentii.me"}).get("Item"))
    self.assertIsNotNone(self.table.get_item(Key={"email":"test2@mentii.me"}).get("Item"))
    self.assertIsNotNone(self.table.get_item(Key={"email":"test3@mentii.me"}).get("Item"))
    self.assertIsNotNone(self.table.get_item(Key={"email":"test4@mentii.me"}).get("Item"))

  def test_preload_data_from_json(self):
    print("Running preload_data_from_json test")
    self.assertIsNotNone(self.table)
    self.assertEqual(self.table.table_status,"ACTIVE")

    jsonData = [
      {
        "email" : "sharks@mentii.me",
        "password" : "fisharefriends",
        "activationId" : "12222",
        "active": "F"
      },
      {
        "email" : "lizards@mentii.me",
        "password" : "lizzzard",
        "activationId" : "asd544",
        "active": "F"
      }
    ]

    db.preloadDataFromJson(jsonData, self.table)
    self.assertIsNotNone(self.table.get_item(Key={"email":"sharks@mentii.me"}).get("Item"))
    self.assertIsNotNone(self.table.get_item(Key={"email":"lizards@mentii.me"}).get("Item"))

#################### Get Table Tests #################################

  def test_getTable(self):
    print("Running getTable test")
    tableName = "users"
    returnedTable = db.getTable(tableName, self.dynamodb)
    self.assertIsNotNone(returnedTable)
    self.assertEqual(returnedTable.table_name, tableName)
    self.assertEqual(returnedTable.table_status, "ACTIVE")

  def test_getTable_fail(self):
    print("Running getTable fail test case")
    tableName = "bananas"
    returnedTable = db.getTable(tableName, self.dynamodb)
    self.assertIsNone(returnedTable)

#################### Item Tests #################################

  def test_putItem_json(self):
    print("Running putItem_json test")
    self.assertIsNotNone(self.table)
    self.assertEqual(self.table.table_status,"ACTIVE")

    jsonData = {
      "email": "tabby",
      "gender": "male"
    }

    db.putItem(jsonData, self.table)
    self.assertIsNotNone(self.table.get_item(Key={"email":"tabby"}).get("Item"))

  def test_putItem_string(self):
    print("Running putItem_string test")
    self.assertIsNotNone(self.table)
    self.assertEqual(self.table.table_status,"ACTIVE")

    jsonData = '{\
      "email": "doggy",\
      "gender": "female"\
    }'

    db.putItem(jsonData, self.table)
    self.assertIsNotNone(self.table.get_item(Key={"email":"doggy"}).get("Item"))

  def test_getItem_json(self):
    print("Running getItem_json test")
    self.assertIsNotNone(self.table)
    self.assertEqual(self.table.table_status,"ACTIVE")

    jsonData = {
      'Key':{'email':'test@mentii.me'},
    }

    response = db.getItem(jsonData, self.table)
    self.assertIsNotNone(response.get("Item"))
    self.assertEqual(response.get("Item").get("email"), "test@mentii.me")

  def test_getItem_string(self):
    print("Running getItem_string test")
    self.assertIsNotNone(self.table)
    self.assertEqual(self.table.table_status,"ACTIVE")

    jsonData = '{\
      "Key": {"email":"test2@mentii.me"},\
      "AttributesToGet": ["password"]\
    }'

    response = db.getItem(jsonData, self.table)
    self.assertIsNotNone(response.get("Item"))
    self.assertEqual(response.get("Item").get("password"), "iameight2")

  def test_getItem_fail(self):
    print("Running getItem_fail fail test case")
    self.assertIsNotNone(self.table)
    self.assertEqual(self.table.table_status,"ACTIVE")

    jsonData = '{\
      "Key": {"email":"potato@mentii.me"},\
      "AttributesToGet": ["password"]\
    }'

    response = db.getItem(jsonData, self.table)
    self.assertIsNone(response.get("Item"))

  def test_updateItem_json(self):
    print("Running updateItem_json test")
    self.assertIsNotNone(self.table)
    self.assertEqual(self.table.table_status,"ACTIVE")

    jsonData = {
      "Key": {"email": "test4@mentii.me"},
      "UpdateExpression": "SET active = :a",
      "ExpressionAttributeValues": { ":a": "T" },
      "ReturnValues" : "UPDATED_NEW"
    }

    db.updateItem(jsonData, self.table)
    item = self.table.get_item(Key={"email":"test4@mentii.me"}).get("Item")

    self.assertIsNotNone(item)
    self.assertEqual(item.get("active"), "T")

  def test_updateItem_string(self):
    print("Running updateItem_string test")
    self.assertIsNotNone(self.table)
    self.assertEqual(self.table.table_status,"ACTIVE")

    jsonData = '{\
      "Key": {"email": "test3@mentii.me"},\
      "UpdateExpression": "SET active = :a",\
      "ExpressionAttributeValues": { ":a": "F" },\
      "ReturnValues" : "UPDATED_NEW"\
    }'

    db.updateItem(jsonData, self.table)
    item = self.table.get_item(Key={"email":"test3@mentii.me"}).get("Item")

    self.assertIsNotNone(item)
    self.assertEqual(item.get("active"), "F")

  def test_updateItem_not_previously_existed(self):
    print("Running updateItem_not_previously_existed test")
    self.assertIsNotNone(self.table)
    self.assertEqual(self.table.table_status,"ACTIVE")

    jsonData = '{\
      "Key": {"email": "crab@mentii.me"},\
      "UpdateExpression": "SET active = :a",\
      "ExpressionAttributeValues": { ":a": "F" },\
      "ReturnValues" : "UPDATED_NEW"\
    }'

    db.updateItem(jsonData, self.table)
    item = self.table.get_item(Key={"email":"crab@mentii.me"}).get("Item")

    self.assertIsNotNone(item)
    self.assertEqual(item.get("active"), "F")

  def test_deleteItem_string(self):
    print("Running deleteItem_string test")
    self.assertIsNotNone(self.table)
    self.assertEqual(self.table.table_status,"ACTIVE")

    jsonData = '{\
      "email" : "test2@mentii.me"\
    }'

    db.deleteItem(jsonData, self.table)
    self.assertIsNone(self.table.get_item(Key={"email":"test2@mentii.me"}).get("Item"))

  def test_deleteItem_json(self):
    print("Running deleteItem_json test")
    self.assertIsNotNone(self.table)
    self.assertEqual(self.table.table_status,"ACTIVE")

    jsonData = {
      "email" : "test4@mentii.me"
    }

    db.deleteItem(jsonData, self.table)
    self.assertIsNone(self.table.get_item(Key={"email":"test4@mentii.me"}).get("Item"))

  def test_deleteItem_fail(self):
    print("Running deleteItem fail test case")
    self.assertIsNotNone(self.table)
    self.assertEqual(self.table.table_status,"ACTIVE")

    jsonData = {
      "email" : "lizards@mentii.me"
    }

    db.deleteItem(jsonData, self.table)
    self.assertIsNone(self.table.get_item(Key={"email":"lizards@mentii.me"}).get("Item"))

#################### Table Action Tests #################################

  def test_query(self):
    print("Running query test")
    self.assertIsNotNone(self.table)
    self.assertEqual(self.table.table_status,"ACTIVE")

    response = db.query("email", "test2@mentii.me", self.table)
    self.assertEqual(response.get("Count"), 1)
    self.assertEqual(response.get("Items")[0].get("email"), "test2@mentii.me")

  def test_scan(self):
    print("Running scan test")
    self.assertIsNotNone(self.table)
    self.assertEqual(self.table.table_status,"ACTIVE")

    response = db.scan(self.table)
    self.assertEqual(response.get("Count"), 4)
    self.assertIsNotNone(response.get("Items"))

  def test_scanFilter(self):
    print("Running scanFilter test")
    self.assertIsNotNone(self.table)
    self.assertEqual(self.table.table_status,"ACTIVE")

    attributeName = 'active'
    attribute = 'T'

    response = db.scanFilter(attributeName, attribute, self.table)
    for i in response['Items']:
      self.assertEqual(i.get("active"), "T")

  def test_deleteTable(self):
    print("Running deleteTable test")

    setUpData = {
      "TableName" :"monkeys",
      "KeySchema":[
        {
          "AttributeName": "email",
          "KeyType": "HASH"
        }
      ],
      "AttributeDefinitions":[
        {
          "AttributeName": "email",
          "AttributeType": "S"
        }
      ],
      "ProvisionedThroughput":{
        "ReadCapacityUnits": 5,
        "WriteCapacityUnits": 5
      }
    }

    attribute_definitions = setUpData.get("AttributeDefinitions")
    key_schema = setUpData.get("KeySchema")
    provisioned_throughput = setUpData.get("ProvisionedThroughput")
    table_name = setUpData.get("TableName")

    self.dynamodb.create_table(
      AttributeDefinitions=attribute_definitions,
      KeySchema=key_schema,
      ProvisionedThroughput=provisioned_throughput,
      TableName=table_name
    )

    db.deleteTable("monkeys", self.dynamodb)

    tables = self.dynamodbClient.list_tables()
    tableNames = tables.get("TableNames")
    for name in tableNames:
      self.assertNotEqual(name, "monkeys")

  def test_deleteTable_fail(self):
    print("Running deleteTable fail test case")
    tableName = "apples"
    returnedTable = db.deleteTable(tableName, self.dynamodb)
    self.assertIsNone(returnedTable)