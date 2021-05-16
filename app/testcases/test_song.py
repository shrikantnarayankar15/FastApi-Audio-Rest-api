from fastapi.testclient import TestClient
from main import app
import logging
import pytest
import unittest
from config.validation_errors import *

logging.basicConfig(level=logging.DEBUG)
mylogger = logging.getLogger()

client = TestClient(app)

class TestClass(unittest.TestCase):

    def testSong_400(self):
        response = client.get("/song/1000001")
        jsonData = response.json()
        status_code = response.status_code
        assert status_code == 400, jsonData

    def test_get_Song_200(self):
        response = client.get("/song/3")
        status_code = response.status_code
        jsonData = response.json()
        keys = jsonData.keys()
        assert status_code == 200, jsonData
        sortKeys = sorted(list(keys))
        self.assertCountEqual(sortKeys, ['duration', 'id', 'name', 'uploadTime'])
        self.assertListEqual(sortKeys, ['duration', 'id', 'name', 'uploadTime'])
        assert status_code == 200, jsonData

    def test_post_Song_Already_exist(self):
        request = {
            "id" : 3,
            "name": "string",
            "duration": 0,
            "uploadTime": "2021-05-15T05:14:40.431Z"
            }
        response = client.post('/song', json=request)
        assert response.json() == {'detail': 'User Already Exist'}
        assert response.status_code == 400
    
    def test_post_Song_validation(self):
        request = {
            "id" : 3,
            "name": "string"*100,
            "duration": 0,
            "uploadTime": "2021-05-15T05:14:40.431Z"
            }
        
        response = client.post('/song', json=request)
        assert response.json() == max_100_string_error