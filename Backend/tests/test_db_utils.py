import unittest
import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
from utils import db_utils as db

import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )


class DbUtilsTest(unittest.TestCase):

#################### Test Class Setup #################################

  @classmethod
  def setUpClass(self):
    self.settingsName = "./tests/table_settings.json"
    self.badSettingsName = "./tests/bad_table_settings.json"
    self.mockData = "./tests/mock_data.json"
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

#################### Table Creation Tests #################################

  def test_create_table_from_file(self):
    print("Running create_table_from_file test")
    table = db.createTableFromFile(self.settingsName, self.dynamodb)
    self.assertNotEqual(table,"Unable to create table")
    self.assertEqual(table.table_status,"ACTIVE")
    self.assertEqual(table.table_name, "users")

  def test_create_table_from_file_fail(self):
    print("Running create_table_from_file test fail test case")
    table = db.createTableFromFile(self.badSettingsName, self.dynamodb)
    self.assertEqual(table,"Unable to create table")

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
    self.assertNotEqual(tableFromString, "Unable to create table")
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
    self.assertEqual(tableFromBadString, "Unable to create table")

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
    self.assertNotEqual(tableFromJson, "Unable to create table")
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
    self.assertEqual(tableFromJsonBad, "Unable to create table")

#################### Preload Data Tests #################################

  def test_preload_data_from_file(self):
    print("Running preload_data_from_file test")
    #get users table from dynamodb instance
    table = self.dynamodb.Table('users')
    self.assertNotEqual(table,"Unable to create table")
    self.assertEqual(table.table_status,"ACTIVE")

    db.preloadDataFromFile(self.mockData, table)
    self.assertIsNotNone(table.get_item(Key={"email":"test@mentii.me"}).get("Item"))
    self.assertIsNotNone(table.get_item(Key={"email":"test2@mentii.me"}).get("Item"))
    self.assertIsNotNone(table.get_item(Key={"email":"test3@mentii.me"}).get("Item"))
    self.assertIsNotNone(table.get_item(Key={"email":"test4@mentii.me"}).get("Item"))

  def test_preload_data_from_json(self):
    print("Running preload_data_from_json test")
    #get users table from dynamodb instance
    table = self.dynamodb.Table('users')
    self.assertNotEqual(table,"Unable to create table")
    self.assertEqual(table.table_status,"ACTIVE")

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

    db.preloadDataFromJson(jsonData, table)
    self.assertIsNotNone(table.get_item(Key={"email":"sharks@mentii.me"}).get("Item"))
    self.assertIsNotNone(table.get_item(Key={"email":"lizards@mentii.me"}).get("Item"))

    print (table.scan())

#################### Get Table Tests #################################

  def test_getTable(self):
    print("Running getTable test")
    tableName = "users"
    table = db.getTable(tableName, self.dynamodb)
    self.assertEqual(table.table_name, tableName)
    self.assertEqual(table.table_status, "ACTIVE")

  def test_getTable_fail(self):
    print("Running getTable fail test case")
    tableName = "bananas"
    table = db.getTable(tableName, self.dynamodb)
    self.assertEqual(table, "Unable to get table bananas. Table does not exist")

#################### Item Tests #################################

  def test_putItem_json(self):
    print("Running putItem_json test")
    #check table instance
    #get users table from dynamodb instance
    table = self.dynamodb.Table('cats')
    self.assertNotEqual(table,"Unable to create table")
    self.assertEqual(table.table_status,"ACTIVE")

    jsonData = {
      "name": "tabby",
      "gender": "male"
    }

    db.putItem(jsonData, table)
    self.assertIsNotNone(table.get_item(Key={"name":"tabby"}).get("Item"))

  def test_putItem_string(self):
    print("Running putItem_string test")
    #check table instance
    #get users table from dynamodb instance
    table = self.dynamodb.Table('puppies')
    self.assertNotEqual(table,"Unable to create table")
    self.assertEqual(table.table_status,"ACTIVE")

    jsonData = '{\
      "name": "doggy",\
      "gender": "female"\
    }'

    db.putItem(jsonData, table)
    self.assertIsNotNone(table.get_item(Key={"name":"doggy"}).get("Item"))

  def test_getItem_json(self):
    print("Running getItem_json test")
    table = self.dynamodb.Table('users')
    self.assertNotEqual(table,"Unable to create table")
    self.assertEqual(table.table_status,"ACTIVE")

    jsonData = {
      'Key':{'email':'sharks@mentii.me'},
    }

    print(table.table_name)
    print(table.scan())

    #print(db.getItem(jsonData, table))
    self.assertIsNotNone(table.get_item(Key={"email":"test3@mentii.me"}).get("Item"))

  def test_getItem_string(self):
    print("Running getItem_string test")
    table = self.dynamodb.Table('users')
    self.assertNotEqual(table,"Unable to create table")
    self.assertEqual(table.table_status,"ACTIVE")

    jsonData = '{\
      "Key": {"email":"test2@mentii.me"},\
      "AttributesToGet": ["password"]\
    }'
    db.getItem(jsonData, table)
    self.assertIsNotNone(table.get_item(Key={"email":"test2@mentii.me"}).get("Item"))

  def test_updateItem_json(self):
    print("Running updateItem_json test")
    table = self.dynamodb.Table('users')
    self.assertNotEqual(table,"Unable to create table")
    self.assertEqual(table.table_status,"ACTIVE")

    jsonData = {
      "Key": {"email": "test4@mentii.me"},
      "UpdateExpression": "SET active = :a",
      "ExpressionAttributeValues": { ":a": "T" },
      "ReturnValues" : "UPDATED_NEW"
    }

    db.updateItem(jsonData, table)
    item = table.get_item(Key={"email":"test4@mentii.me"}).get("Item")

    self.assertIsNotNone(item)
    self.assertEqual(item.get("active"), "T")

  def test_updateItem_string(self):
    print("Running updateItem_string test")
    table = self.dynamodb.Table('users')
    self.assertNotEqual(table,"Unable to create table")
    self.assertEqual(table.table_status,"ACTIVE")

    jsonData = '{\
      "Key": {"email": "test3@mentii.me"},\
      "UpdateExpression": "SET active = :a",\
      "ExpressionAttributeValues": { ":a": "F" },\
      "ReturnValues" : "UPDATED_NEW"\
    }'

    db.updateItem(jsonData, table)
    item = table.get_item(Key={"email":"test3@mentii.me"}).get("Item")

    self.assertIsNotNone(item)
    self.assertEqual(item.get("active"), "F")

  def test_deleteItem_string(self):
    print("Running deleteItem_string test")
    table = self.dynamodb.Table('users')
    self.assertNotEqual(table,"Unable to create table")
    self.assertEqual(table.table_status,"ACTIVE")

    jsonData = '{\
      "email" : "sharks@mentii.me"\
    }'

    db.deleteItem(jsonData, table)
    self.assertIsNone(table.get_item(Key={"email":"sharks@mentii.me"}).get("Item"))

  def test_deleteItem_json(self):
    print("Running deleteItem_json test")
    table = self.dynamodb.Table('users')
    self.assertNotEqual(table,"Unable to create table")
    self.assertEqual(table.table_status,"ACTIVE")

    jsonData = {
      "email" : "lizards@mentii.me"
    }

    db.deleteItem(jsonData, table)
    self.assertIsNone(table.get_item(Key={"email":"lizards@mentii.me"}).get("Item"))
    #check response
    #check item is deleted from db

  def test_deleteItem_fail(self):
    print("Running deleteItem fail test case")
    table = self.dynamodb.Table('users')
    self.assertNotEqual(table,"Unable to create table")
    self.assertEqual(table.table_status,"ACTIVE")

    jsonData = {
      "email" : "lizards@mentii.me"
    }

    db.deleteItem(jsonData, table)
    self.assertIsNone(table.get_item(Key={"email":"lizards@mentii.me"}).get("Item"))

#################### Table Action Tests #################################

  def test_query(self):
    print("Running query test")
    table = self.dynamodb.Table('users')
    self.assertNotEqual(table,"Unable to create table")
    self.assertEqual(table.table_status,"ACTIVE")

    response = db.query("activationId", "abcde", table)
    for i in response[u'Items']:
      print(json.dumps(i, cls=DecimalEncoder))
    #check response
    #check query matches

  def test_scan(self):
    print("Running scan test")
    table = self.dynamodb.Table('users')
    self.assertNotEqual(table,"Unable to create table")
    self.assertEqual(table.table_status,"ACTIVE")

    response = db.scan(table)
    print(response)

  def test_scanFilter(self):
    print("Running scanFilter test")
    table = self.dynamodb.Table('users')
    self.assertNotEqual(table,"Unable to create table")
    self.assertEqual(table.table_status,"ACTIVE")

    attributeName = 'active'

    attribute = 'T'

    response = db.scanFilter(attributeName, attribute, table)
    for i in response['Items']:
      print(json.dumps(i, cls=DecimalEncoder))

  def test_deleteTable(self):
    print("Running deleteTable test")
    db.deleteTable("users", self.dynamodb)

    tables = self.dynamodbClient.list_tables()
    tableNames = tables.get("TableNames")
    for name in tableNames:
      self.assertNotEqual(name, "users")