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

    def testAudibook_400(self):
        response = client.get("/audiobook/10000011")
        jsonData = response.json()
        status_code = response.status_code
        assert status_code == 400, jsonData

    def test_get_Audibook_200(self):
        response = client.get("/audiobook/1000001")
        status_code = response.status_code
        jsonData = response.json()
        keys = jsonData.keys()
        assert status_code == 200, jsonData
        mylogger.info(keys)
        sortKeys = sorted(list(keys))
        self.assertCountEqual(sortKeys, ['author', 'duration', 'id', 'narrator', 'title', 'uploadTime'])
        self.assertListEqual(sortKeys, ['author', 'duration', 'id', 'narrator', 'title', 'uploadTime'])
        assert status_code == 200, jsonData

    def test_post_Audibook_Already_exist(self):
        request = {
            "id": 1000001,
            "title": "string",
            "author": "string",
            "narrator": "string",
            "duration": 0,
            "uploadTime": "2021-05-15T05:13:48.678Z"
            }

        response = client.post('/audiobook', json=request)
        assert response.json() == {'detail': 'User Already Exist'}
        assert response.status_code == 400
    
    def test_post_Audibook_validation(self):
        request = {
            "id": 1000001,
            "title": "string"*100,
            "author": "string",
            "narrator": "string",
            "duration": 0,
            "uploadTime": "2021-05-15T05:13:48.678Z"
            }

        
        response = client.post('/audiobook', json=request)
        assert response.json() == max_100_string_error_title