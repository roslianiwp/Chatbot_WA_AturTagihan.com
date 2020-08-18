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
# from tests.test_formula_edit import test_edit_formula_success

with open("tests/formula/get_all.json") as file:
    all_formula = json.load(file)
    
with open("tests/formula/failed_add.json") as file:
    add_formula = json.load(file)

with open("tests/product/get_all.json") as file:
    all_produk = json.load(file)
    
with open("tests/unit_type/get_all.json") as file:
    all_unit_type = json.load(file)
    
with open("tests/billing_type/get_all.json") as file:
    all_billing_type = json.load(file)
    
with open("tests/price/get_all.json") as file:
    all_price = json.load(file)

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
            
            elif args[0] == app.config['URL']+"/product/all":
                return MockResponse(all_produk, 200)
            
            elif args[0] == app.config["URL"]+"/unit_type/all":
                return MockResponse(all_unit_type, 200)
            
            elif args[0] == app.config["URL"]+"/billing_type/all":
                return MockResponse(all_billing_type, 200)
            
            elif args[0] == app.config["URL"]+"/price/all":
                return MockResponse(all_price, 200)
                
            elif args[0] == app.config["URL"]+"/formula":
                return MockResponse(add_formula, 400)
            
            else:
                return MockResponse(None, 404)
    
    # SUCCESS
    @mock.patch('requests.post', side_effect=mocked_requests_aturtagihan_add_formula)
    def test_add_formula_success(self, get_mock, client):
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
        data = send_message("6281320003997", "tambah")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer '+app.config['TOKEN']},
                            content_type='application/json')
        
        # MASUKKAN NOMOR PRODUK
        data = send_message("6281320003997", "1")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer '+app.config['TOKEN']},
                            content_type='application/json')
        
        # MASUKKAN NOMOR JENIS UNIT
        data = send_message("6281320003997", "1")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer '+app.config['TOKEN']},
                            content_type='application/json')
        
        # MASUKKAN NOMOR JENIS TAGIHAN
        data = send_message("6281320003997", "1")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer '+app.config['TOKEN']},
                            content_type='application/json')
        
        # MASUKKAN JENIS PERHITUNGAN
        data = send_message("6281320003997", "1")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer '+app.config['TOKEN']},
                            content_type='application/json')
        
        # MASUKKAN KATEGORI TAGIHAN
        data = send_message("6281320003997", "1")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer '+app.config['TOKEN']},
                            content_type='application/json')
        
        # MASUKKAN HARGA
        data = send_message("6281320003997", "1")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer '+app.config['TOKEN']},
                            content_type='application/json')
        
        # MASUKKAN FORMULA
        data = send_message("6281320003997", "price.base_price * unit.size")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer '+app.config['TOKEN']},
                            content_type='application/json')

    # JENIS UNIT TIDAK ADA
    @mock.patch('requests.post', side_effect=mocked_requests_aturtagihan_add_formula)
    def test_add_formula_1(self, get_mock, client):
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
        data = send_message("6281320003997", "tambah")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer '+app.config['TOKEN']},
                            content_type='application/json')
        
        # MASUKKAN NOMOR PRODUK
        data = send_message("6281320003997", "2")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer '+app.config['TOKEN']},
                            content_type='application/json')
        
    # JENIS TAGIHAN TIDAK ADA
    @mock.patch('requests.post', side_effect=mocked_requests_aturtagihan_add_formula)
    def test_add_formula_2(self, get_mock, client):
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
        data = send_message("6281320003997", "tambah")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer '+app.config['TOKEN']},
                            content_type='application/json')
        
        # MASUKKAN NOMOR PRODUK
        data = send_message("6281320003997", "3")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer '+app.config['TOKEN']},
                            content_type='application/json')
        
        # MASUKKAN NOMOR JENIS UNIT
        data = send_message("6281320003997", "5")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer '+app.config['TOKEN']},
                            content_type='application/json')
        
    # KATEGORI TAGIHAN 3
    @mock.patch('requests.post', side_effect=mocked_requests_aturtagihan_add_formula)
    def test_add_formula_3(self, get_mock, client):
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
        data = send_message("6281320003997", "tambah")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer '+app.config['TOKEN']},
                            content_type='application/json')
        
        # MASUKKAN NOMOR PRODUK
        data = send_message("6281320003997", "1")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer '+app.config['TOKEN']},
                            content_type='application/json')
        
        # MASUKKAN NOMOR JENIS UNIT
        data = send_message("6281320003997", "1")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer '+app.config['TOKEN']},
                            content_type='application/json')
        
        # MASUKKAN NOMOR JENIS TAGIHAN
        data = send_message("6281320003997", "1")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer '+app.config['TOKEN']},
                            content_type='application/json')
        
        # MASUKKAN JENIS PERHITUNGAN
        data = send_message("6281320003997", "1")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer '+app.config['TOKEN']},
                            content_type='application/json')
        
        # MASUKKAN KATEGORI TAGIHAN
        data = send_message("6281320003997", "3")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer '+app.config['TOKEN']},
                            content_type='application/json')