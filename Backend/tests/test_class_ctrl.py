import unittest


import boto3
import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from mentii import class_ctrl
from utils import db_utils as db


#local DynamoDB
dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')

class ClassCtrlDBTests(unittest.TestCase):
  @classmethod
  def setUpClass(self):
    self.dynamodbClient = boto3.client('dynamodb', endpoint_url='http://localhost:8000')

    #clean up local DB before tests
    tables = self.dynamodbClient.list_tables()
    tableNames = tables.get("TableNames")
    try:
      for name in tableNames:
        dynamodb.Table(name).delete()
    except:
      print("Error deleting tableNames")

    classSettingsName = "classes_settings.json"
    classMockData = "mock_classes.json"
    settingsName = "table_settings.json"
    mockData = "mock_data.json"

    user_table = db.createTableFromFile("./tests/"+settingsName, dynamodb)
    class_table = db.createTableFromFile("./tests/"+classSettingsName, dynamodb)

    db.preloadClassData("./tests/"+classMockData, class_table)
    db.preloadDataFromFile("./tests/"+mockData, user_table)

  @classmethod
  def tearDownClass(self):
    db.getTable('classes', dynamodb).delete()

  def test_getActiveClassList(self):
    user =  "test@mentii.me"
    response = class_ctrl.getActiveClassList(dynamodb, user)
    self.assertNotEqual(response, None)

  def test_getPublicClassList(self):
    user =  "test@mentii.me"
    response = class_ctrl.getPublicClassList(dynamodb, user)
    self.assertNotEqual(response, None)

  def test_getClassCodesFromUser(self):
    user =  "test@mentii.me"
    response = class_ctrl.getClassCodesFromUser(dynamodb, user)
    self.assertNotEqual(response, None)
    self.assertTrue(len(response) == 3)

if __name__ == '__main__':
  if __package__ is None:
    import sys
    from os import path
    sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
    from mentii import class_ctrl
  else:
    from ..mentii import class_ctrl
  unittest.main()
