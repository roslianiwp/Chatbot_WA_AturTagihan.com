import config
import pytest
import json
import redis
from unittest import mock
from unittest.mock import patch
from flask import request
from . import client
from blueprints import app
from tests.fungsi.fungsi import send_message

with open("tests/formula/get_all.json") as file:
    all_formula = json.load(file)
    
with open("tests/formula/delete.json") as file:
    delete_formula = json.load(file)

class TestAddFormula():
    def mocked_requests_get(*args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code
            def json(self):
                return self.json_data
        if args[0] == "https://messages-sandbox.nexmo.com/v0.1/messages":
            return MockResponse({"message_uuid":"e4b1a241-1172-4fd4-9b12-7c82ce2f1517"}, 202)
    
    def mocked_requests_aturtagihan_add_formula(*args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code
            
            def json(self):
                return self.json_data
        if len(args) > 0:
            if args[0] == app.config['URL']+"/formula/all":
                return MockResponse(all_formula, 200)
            else:
                return MockResponse(None, 404)
            
    def mocked_requests_aturtagihan_delete_formula(*args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code
            
            def json(self):
                return self.json_data
        if len(args) > 0:            
            if args[0] == app.config["URL"]+"/formula/340":
                return MockResponse(delete_formula, 200)
            else:
                return MockResponse(None, 404)
    
    # SUCCESS
    @mock.patch('requests.post', side_effect=mocked_requests_aturtagihan_add_formula)
    @mock.patch('requests.delete', side_effect=mocked_requests_aturtagihan_delete_formula)
    def test_delete_formula_success(self, delete_mock, get_mock, client):
        # PENGATURAN
        data = send_message("6281320003997", "pengaturan")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer '+app.config['TOKEN']},
                            content_type='application/json')
        
        # PILIH MENU FORMULA
        data = send_message("6281320003997", "formula")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer '+app.config['TOKEN']},
                            content_type='application/json')

        # PILIH MENU TAMBAH
        data = send_message("6281320003997", "hapus 1")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer '+app.config['TOKEN']},
                            content_type='application/json')
        
    # HAPUS 100
    @mock.patch('requests.post', side_effect=mocked_requests_aturtagihan_add_formula)
    @mock.patch('requests.delete', side_effect=mocked_requests_aturtagihan_delete_formula)
    def test_delete_formula_100(self, delete_mock, get_mock, client):
        # PENGATURAN
        data = send_message("6281320003997", "pengaturan")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer '+app.config['TOKEN']},
                            content_type='application/json')
        
        # PILIH MENU FORMULA
        data = send_message("6281320003997", "formula")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer '+app.config['TOKEN']},
                            content_type='application/json')

        # PILIH MENU TAMBAH
        data = send_message("6281320003997", "hapus 100")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer '+app.config['TOKEN']},
                            content_type='application/json')