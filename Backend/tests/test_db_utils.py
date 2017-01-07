import unittest
import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
from utils import db_utils as db

import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )


class DbUtilsTest(unittest.TestCase):
  @classmethod
  def setUpClass(self):
    self.settingsName = "table_settings.json"
    self.badSettingsName = "bad_table_settings.json"
    self.mockData = "mock_data.json"
    self.dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')
    self.dynamodbClient = boto3.client('dynamodb')

    #wipe local DB
    tables = self.dynamodbClient.list_tables()
    tableNames = tables.get("TableNames")
    try:
      for name in tableNames:
        self.dynamodb.Table(name).delete()
    except:
      print("Error deleting tableNames")
    #self.dynamodb.Table('users').delete()
    #self.dynamodb.Table('puppies').delete()
    #self.dynamodb.Table('cats').delete()


  @classmethod
  def tearDownClass(self):
    #wipe local DB
    tables = self.dynamodbClient.list_tables()
    tableNames = tables.get("TableNames")
    try:
      for name in tableNames:
        self.dynamodb.Table(name).delete()
    except:
      print("Error deleting tableNames")

  def test_create_table_from_file(self):
    table = db.createTableFromFile("./tests/" + self.settingsName, self.dynamodb)
    self.assertNotEqual(table,"Unable to create table")
    self.assertEqual(table.table_status,"ACTIVE")
    print(self.dynamodb.Table('users'))

  def test_create_table_from_file_fail(self):
    table = db.createTableFromFile("./tests/" + self.badSettingsName, self.dynamodb)
    self.assertEqual(table,"Unable to create table")

  def test_create_table_from_string(self):
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

  def test_create_table_from_string_fail(self):
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

  def test_create_table_from_json_fail(self):
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
'''
  def test_preload_data_from_file(self):

    self.assertIsNotEqual(table,"Unable to create table")
    self.assertEqual(table.table_status,"ACTIVE")

    response = db.preloadDataFromFile(self.mockData, table)

  def test_preload_data_from_json(self):
  def test_getTable(self):
  def test_putItem(self):
  def test_getItem(self):
  def test_updateItem(self):
  def test_deleteItem(self):
  def test_query(self):
  def test_scan(self):
  def test_deleteTable(self):'''