import unittest

import db_utils as db

import boto3
import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from mentii import class_ctrl 


#local DynamoDB
dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')

class ClassCtrlDBTests(unittest.TestCase):
  @classmethod
  def setUpClass(self):
    classSettingsName = "classes_settings.json"
    classMockData = "mock_classes.json"
    settingsName = "table_settings.json"
    mockData = "mock_data.json"

    table = db.createTableFromFile("./tests/"+settingsName, dynamodb)
    table = db.createTableFromFile("./tests/"+classSettingsName, dynamodb)

    db.preloadClassData("./tests/"+classMockData, table)
    db.preloadData("./tests/"+mockData, table)

  @classmethod
  def tearDownClass(self):
    table = db.getTable('classes', dynamodb).delete()

  def test_getActiveClassList(self):
    user =  "test@mentii.me"
    response = class_ctrl.getActiveClassList(dynamodb, user)
    print(response)

if __name__ == '__main__':
  if __package__ is None:
    import sys
    from os import path
    sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
    from mentii import class_ctrl
  else:
    from ..mentii import class_ctrl
  untest.main()
