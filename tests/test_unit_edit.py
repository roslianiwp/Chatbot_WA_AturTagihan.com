from unittest import mock
from unittest.mock import patch
import pytest
from flask import request
import json
import redis
from . import client
from tests.fungsi.fungsi import send_message

with open("tests/unit/get_all.json") as file:
    all_unit = json.load(file)
    
with open("tests/unit/add.json") as file:
    add_unit = json.load(file)
    
with open("tests/product/get_all.json") as file:
    all_product = json.load(file)
    
with open("tests/unit_type/get_all.json") as file:
    all_unit_type = json.load(file)
    
with open("tests/customer/get_all.json") as file:
    all_customer = json.load(file)

class TestUnit():
    
    def mocked_requests_get(*args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code
            def json(self):
                return self.json_data
        if args[0] == "https://messages-sandbox.nexmo.com/v0.1/messages":
            return MockResponse({"message_uuid":"e4b1a241-1172-4fd4-9b12-7c82ce2f1517"}, 202)
    
    def mocked_requests_aturtagihan_get_all(*args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code
            
            def json(self):
                return self.json_data
        if len(args) > 0:
            if args[0] == "https://magellan.sumpahpalapa.com/api/v1/unit/all":
                return MockResponse(all_unit, 200)
            elif args[0] == "https://magellan.sumpahpalapa.com/api/v1/unit":
                return MockResponse(add_unit, 400)
            elif args[0] == "https://magellan.sumpahpalapa.com/api/v1/product/all":
                return MockResponse(all_product, 200)
            elif args[0] == "https://magellan.sumpahpalapa.com/api/v1/unit_type/all":
                return MockResponse(all_unit_type, 200)
            elif args[0] == "https://magellan.sumpahpalapa.com/api/v1/customer/all":
                return MockResponse(all_customer, 200)
            else:
                return MockResponse(None, 404)
            
    def mocked_requests_aturtagihan_get_id(*args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code
            
            def json(self):
                return self.json_data
        if len(args) > 0:
            if args[0] == "https://magellan.sumpahpalapa.com/api/v1/unit/3204":
                return MockResponse(add_unit, 200)
            else:
                return MockResponse(None, 404)
            
    def mocked_requests_aturtagihan_put_id(*args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code
            
            def json(self):
                return self.json_data
        if len(args) > 0:
            if args[0] == "https://magellan.sumpahpalapa.com/api/v1/unit/3204":
                return MockResponse(add_unit, 400)
            else:
                return MockResponse(None, 404)

    # SUCCESS
    @mock.patch('requests.post', side_effect=mocked_requests_aturtagihan_get_all)
    @mock.patch('requests.get', side_effect=mocked_requests_aturtagihan_get_id)
    @mock.patch('requests.put', side_effect=mocked_requests_aturtagihan_put_id)
    def test_edit_unit_success(self, put_mock, get_mock, post_mock, client):
        # PENGATURAN
        data = send_message("6281320003997", "pengaturan")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')
        
        # UNIT
        data = send_message("6281320003997", "unit")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')

        # UBAH
        data = send_message("6281320003997", "ubah 1")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')
        
        # NAMA UNIT
        data = send_message("6281320003997", "test")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')
        
        # UKURAN UNIT
        data = send_message("6281320003997", "40")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')
        
        # NOMOR PRODUK
        data = send_message("6281320003997", "1")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')
        
        # ALAMAT UNIT
        data = send_message("6281320003997", "test")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')
        
        # NOMOR JENIS UNIT
        data = send_message("6281320003997", "1")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')
        
        # PELANGGAN
        data = send_message("6281320003997", "1")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')
        
    # UBAH 100
    @mock.patch('requests.post', side_effect=mocked_requests_aturtagihan_get_all)
    def test_edit_unit_100(self, post_mock, client):
        # PENGATURAN
        data = send_message("6281320003997", "pengaturan")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')
        
        # UNIT
        data = send_message("6281320003997", "unit")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')

        # UBAH
        data = send_message("6281320003997", "ubah 100")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')
        
    # NOMOR PRODUK 100
    @mock.patch('requests.post', side_effect=mocked_requests_aturtagihan_get_all)
    @mock.patch('requests.get', side_effect=mocked_requests_aturtagihan_get_id)
    def test_edit_unit_no_produk_100(self, get_mock, post_mock, client):
        # PENGATURAN
        data = send_message("6281320003997", "pengaturan")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')
        
        # UNIT
        data = send_message("6281320003997", "unit")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')

        # UBAH
        data = send_message("6281320003997", "ubah 1")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')
        
        # NAMA UNIT
        data = send_message("6281320003997", "test")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')
        
        # UKURAN UNIT
        data = send_message("6281320003997", "40")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')
        
        # NOMOR PRODUK
        data = send_message("6281320003997", "100")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')
        
    # JENIS UNIT BELUM ADA
    @mock.patch('requests.post', side_effect=mocked_requests_aturtagihan_get_all)
    @mock.patch('requests.get', side_effect=mocked_requests_aturtagihan_get_id)
    def test_edit_unit_jenis_unit_belum_ada(self, get_mock, post_mock, client):
        # PENGATURAN
        data = send_message("6281320003997", "pengaturan")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')
        
        # UNIT
        data = send_message("6281320003997", "unit")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')

        # UBAH
        data = send_message("6281320003997", "ubah 1")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')
        
        # NAMA UNIT
        data = send_message("6281320003997", "test")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')
        
        # UKURAN UNIT
        data = send_message("6281320003997", "40")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')
        
        # NOMOR PRODUK
        data = send_message("6281320003997", "2")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')
        
        # ALAMAT UNIT
        data = send_message("6281320003997", "test")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')
        
    # JENIS UNIT 100
    @mock.patch('requests.post', side_effect=mocked_requests_aturtagihan_get_all)
    @mock.patch('requests.get', side_effect=mocked_requests_aturtagihan_get_id)
    @mock.patch('requests.put', side_effect=mocked_requests_aturtagihan_put_id)
    def test_edit_unit_jenis_unit_100(self, put_mock, get_mock, post_mock, client):
        # PENGATURAN
        data = send_message("6281320003997", "pengaturan")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')
        
        # UNIT
        data = send_message("6281320003997", "unit")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')

        # UBAH
        data = send_message("6281320003997", "ubah 1")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')
        
        # NAMA UNIT
        data = send_message("6281320003997", "test")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')
        
        # UKURAN UNIT
        data = send_message("6281320003997", "40")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')
        
        # NOMOR PRODUK
        data = send_message("6281320003997", "1")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')
        
        # ALAMAT UNIT
        data = send_message("6281320003997", "test")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')
        
        # NOMOR JENIS UNIT
        data = send_message("6281320003997", "100")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')
        
    # BELUM ADA PELANGGAN
    @mock.patch('requests.post', side_effect=mocked_requests_aturtagihan_get_all)
    @mock.patch('requests.get', side_effect=mocked_requests_aturtagihan_get_id)
    def test_edit_unit_belum_ada_pelanggan(self, get_mock, post_mock, client):
        # PENGATURAN
        data = send_message("6281320003997", "pengaturan")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')
        
        # UNIT
        data = send_message("6281320003997", "unit")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')

        # UBAH
        data = send_message("6281320003997", "ubah 1")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')
        
        # NAMA UNIT
        data = send_message("6281320003997", "test")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')
        
        # UKURAN UNIT
        data = send_message("6281320003997", "40")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')
        
        # NOMOR PRODUK
        data = send_message("6281320003997", "11")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')
        
        # ALAMAT UNIT
        data = send_message("6281320003997", "test")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')
        
        # NOMOR JENIS UNIT
        data = send_message("6281320003997", "6")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')