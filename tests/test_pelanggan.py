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

with open("tests/customer/get_all.json") as file:
    all_customer = json.load(file)

with open("tests/product/get_all_1600.json") as file:
    all_product = json.load(file)
    
with open("tests/customer/add.json") as file:
    add_customer = json.load(file)
    
with open("tests/customer/delete.json") as file:
    delete_customer = json.load(file)

class TestPelanggan():
    
    def mocked_requests_get(*args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code
            def json(self):
                return self.json_data
        if args[0] == "https://messages-sandbox.nexmo.com/v0.1/messages":
            return MockResponse({"message_uuid":"e4b1a241-1172-4fd4-9b12-7c82ce2f1517"}, 202)
    
    def mocked_requests_aturtagihan_pelanggan(*args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code
            
            def json(self):
                return self.json_data
        if len(args) > 0:
            if args[0] == "https://magellan.sumpahpalapa.com/api/v1/customer/all":
                return MockResponse(all_customer, 200)
            if args[0] == "https://magellan.sumpahpalapa.com/api/v1/customer":
                return MockResponse(add_customer, 200)
            elif args[0] == "https://magellan.sumpahpalapa.com/api/v1/product/all":
                    return MockResponse(all_product, 200)
            else:
                return MockResponse(None, 404)
            
    def mocked_requests_aturtagihan_pelanggan_ubah(*args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code
            
            def json(self):
                return self.json_data
        if len(args) > 0:
            if args[0] == "https://magellan.sumpahpalapa.com/api/v1/customer/3215":
                return MockResponse(add_customer, 200)
            else:
                return MockResponse(None, 404)
            
    def mocked_requests_aturtagihan_pelanggan_get(*args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code
            
            def json(self):
                return self.json_data
        if len(args) > 0:
            if args[0] == "https://magellan.sumpahpalapa.com/api/v1/customer/3215":
                return MockResponse(add_customer, 200)
            else:
                return MockResponse(None, 404)
            
    def mocked_requests_aturtagihan_pelanggan_delete(*args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code
            
            def json(self):
                return self.json_data
        if len(args) > 0:
            if args[0] == "https://magellan.sumpahpalapa.com/api/v1/customer/3215":
                return MockResponse(delete_customer, 200)
            else:
                return MockResponse(None, 404)

    #TAMBAH PELANGGAN
    @mock.patch('requests.post', side_effect=mocked_requests_aturtagihan_pelanggan)
    @mock.patch('requests.get', side_effect=mocked_requests_aturtagihan_pelanggan_get)
    @mock.patch('requests.put', side_effect=mocked_requests_aturtagihan_pelanggan_ubah)
    @mock.patch('requests.delete', side_effect=mocked_requests_aturtagihan_pelanggan_delete)
    def test_check_jenis_unit(self, delete_mock, put_mock, get_mock, post_mock, client):
        data = send_message("6281320003997", "pengaturan")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')
        
        data = send_message("6281320003997", "6")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')

        data = send_message("6281320003997", "tambah")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')
        
        data = send_message("6281320003997", "derby")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')
        
        data = send_message("6281320003997", "derbygmail.com")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')
        
        data = send_message("6281320003997", "derby@gmail.com")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')
        
        data = send_message("6281320003997", "+s")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')
        
        data = send_message("6281320003997", "6285645692314")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')
        
        data = send_message("6281320003997", "6285645692314")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')
        
        data = send_message("6281320003997", "1234567891234567")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')
        
        data = send_message("6281320003997", "100000000")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')
        
        data = send_message("6281320003997", "1")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')
        
    #UBAH PELANGGAN
    @mock.patch('requests.post', side_effect=mocked_requests_aturtagihan_pelanggan)
    @mock.patch('requests.get', side_effect=mocked_requests_aturtagihan_pelanggan_get)
    @mock.patch('requests.put', side_effect=mocked_requests_aturtagihan_pelanggan_ubah)
    @mock.patch('requests.delete', side_effect=mocked_requests_aturtagihan_pelanggan_delete)
    def test_check_jenis_unit_ubah(self, delete_mock, put_mock, get_mock, post_mock, client):
        data = send_message("6281320003997", "pelanggan")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')
        
        data = send_message("6281320003997", "ubah 100000000")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')
        
        data = send_message("6281320003997", "pelanggan")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')
        
        data = send_message("6281320003997", "ubah 1")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')        

        data = send_message("6281320003997", "derby")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')
        
        data = send_message("6281320003997", "derby@gmail.com")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')
        
        data = send_message("6281320003997", "6285645692314")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')
        
        data = send_message("6281320003997", "1234567891234567")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')
        
        data = send_message("6281320003997", "1")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')
        
        data = send_message("6281320003997", "pelanggan")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')
        
    #HAPUS PELANGGAN
    @mock.patch('requests.post', side_effect=mocked_requests_aturtagihan_pelanggan)
    @mock.patch('requests.get', side_effect=mocked_requests_aturtagihan_pelanggan_get)
    @mock.patch('requests.put', side_effect=mocked_requests_aturtagihan_pelanggan_ubah)
    @mock.patch('requests.delete', side_effect=mocked_requests_aturtagihan_pelanggan_delete)
    def test_check_jenis_unit_hapus(self, delete_mock, put_mock, get_mock, post_mock, client):
        data = send_message("6281320003997", "hapus 100000000")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')
        
        data = send_message("6281320003997", "hapus 1")
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')