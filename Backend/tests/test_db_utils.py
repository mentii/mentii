import unittest
import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
from utils import db_utils as db

class DbUtilsTest(unittest.TestCase):
  @classmethod
  def setUpClass(self):
    self.settingsName = "table_settings.json"
    self.mockData = "mock_data.json"
    self.dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')

  @classmethod
  def tearDownClass(self):
    self.dynamodb.get_table().delete()

  def test_createTableFromFile(self):
    table = db.createTableFromFile(self.settingsName, self.dynamodb)
    self.assertIsNotEqual(table,"Unable to create table")
    self.assertEqual(table.table_status,"ACTIVE")
    self.dynamodb.get_table().delete()

  def test_createTableFromFile_fail(self):
    table = db.createTableFromFile("bad_table_settings.json", self.dynamodb)
    self.assertEqual(table,"Unable to create table")

  def test_createTableFromJson(self):
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


    tableFromString = db.createTableFromJson(jsonDataString)
    tableFromJson = db.createTableFromJson(jsonData)

  def test_preloadDataFromFile(self):
  def test_preloadDataFromJson(self):
  def test_getTable(self):
  def test_putItem(self):
  def test_getItem(self):
  def test_updateItem(self):
  def test_deleteItem(self):
  def test_query(self):
  def test_scan(self):
  def test_deleteTable(self):