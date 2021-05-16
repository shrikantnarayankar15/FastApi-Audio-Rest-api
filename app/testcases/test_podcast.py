from fastapi.testclient import TestClient
from main import app
import logging
import unittest
from config.validation_errors import *

logging.basicConfig(level=logging.DEBUG)
mylogger = logging.getLogger()

client = TestClient(app)

class TestClass(unittest.TestCase):

    def testPodcast_400(self):
        response = client.get("/podcast/1000001")
        jsonData = response.json()
        status_code = response.status_code
        assert status_code == 400
        mylogger.error(jsonData)

    def test_get_Podcast_200(self):
        response = client.get("/podcast/1")
        status_code = response.status_code
        jsonData = response.json()
        keys = jsonData.keys()
        assert status_code == 200, jsonData
        sortKeys = sorted(list(keys))
        mylogger.info(sortKeys)
        self.assertCountEqual(sortKeys,  ['duration', 'host', 'id', 'name', 'participants', 'uploadTime'])
        self.assertListEqual(sortKeys,  ['duration', 'host', 'id', 'name', 'participants', 'uploadTime'])
        assert status_code == 200, jsonData

    def test_post_Podcast_Already_exist(self):
        request = {
            "id": 1,
            "uploadTime": "2021-05-15T23:14:47.537507",
            "host": "string",
            "name": "string",
            "duration": 100,
            "participants": [
            "string1",
            "string2",
            "string3",
            "string4"
            ]
        }
        response = client.post('/podcast', json=request)
        assert response.json() == {'detail': 'User Already Exist'}
        assert response.status_code == 400
        mylogger.error(response.json())
    
    def test_post_Podcast_validation(self):

        request = {
            "id": 1,
            "uploadTime": "2021-05-15T23:14:47.537507",
            "host": "lol",
            "name": "name"*100,
            "duration": 100,
            "participants": ["string"]
        }
        
        response = client.post('/song', json=request)
        mylogger.error(response.json())
        assert response.json() == max_100_string_error

    def test_post_Podcast_validateParticipantList(self):

        request = {
            "id": 1,
            "uploadTime": "2021-05-15T23:14:47.537507",
            "host": "lol",
            "name": "name",
            "duration": 100,
            "participants": ["string"]*11
        }
        
        response = client.post('/podcast', json=request)
        mylogger.error(response.json())
        assert response.json() == max_10_participant_error
