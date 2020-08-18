import pytest
import json
import redis
import config
from blueprints import app
from unittest import mock
from unittest.mock import patch
from flask import request
from . import client
from tests.fungsi.fungsi import send_message



with open("tests/billing/get_all_1600.json") as file:
    all_billing_1600 = json.load(file)

class TestLinkTagihan():

    def mocked_requests_get(*args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code
            def json(self):
                return self.json_data
        if args[0] == "https://messages-sandbox.nexmo.com/v0.1/messages":
            return MockResponse({"message_uuid":"e4b1a241-1172-4fd4-9b12-7c82ce2f1517"}, 202)

    def mocked_requests_aturtagihan_link_tagihan_success(*args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code
            
            def json(self):
                return self.json_data
        if len(args) > 0:
            if args[0] == app.config['URL'] + "/billing/list":
                return MockResponse({
                                "rescode": "0000",
                                "message": {
                                    "title": "Success",
                                    "body": "Success"
                                },
                                "data": [
                                    {
                                    "billing_id": 2386,
                                    "unit_id": 3212,
                                    "unit_name": "unit 10 kamar test",
                                    "current_balance": 50002,
                                    "previous_balance": 0,
                                    "charge": 0,
                                    "total": 50002,
                                    "billing_periode": "2020-06-26T00:00:00+07:00",
                                    "billing_start_date": "2020-06-26T00:00:00+07:00",
                                    "billing_end_date": "2020-06-27T00:00:00+07:00",
                                    "billing_status": 3,
                                    "billing_channel_payment": 0,
                                    "product_id": 1148,
                                    "product_name": "Testing Perumahan Plis",
                                    "customer_id": 3245,
                                    "customer_name": "Rosliani"
                                    },
                                    {
                                    "billing_id": 2443,
                                    "unit_id": 3212,
                                    "unit_name": "unit 10 kamar test",
                                    "current_balance": 50002,
                                    "previous_balance": 0,
                                    "charge": 0,
                                    "total": 50002,
                                    "billing_periode": "2020-07-07T00:00:00+07:00",
                                    "billing_start_date": "2020-07-07T00:00:00+07:00",
                                    "billing_end_date": "2020-07-28T00:00:00+07:00",
                                    "billing_status": 0,
                                    "billing_channel_payment": 0,
                                    "product_id": 1148,
                                    "product_name": "Testing Perumahan Plis",
                                    "customer_id": 3245,
                                    "customer_name": "Rosliani"
                                    },
                                    {
                                    "billing_id": 2472,
                                    "unit_id": 3330,
                                    "unit_name": "Kamisday",
                                    "current_balance": 4040,
                                    "previous_balance": 0,
                                    "charge": 0,
                                    "total": 4040,
                                    "billing_periode": "2020-07-01T00:00:00+07:00",
                                    "billing_start_date": "2020-07-09T00:00:00+07:00",
                                    "billing_end_date": "2020-07-10T00:00:00+07:00",
                                    "billing_status": 0,
                                    "billing_channel_payment": 0,
                                    "product_id": 1161,
                                    "product_name": "Kamis",
                                    "customer_id": 3262,
                                    "customer_name": "Thursday"
                                    },
                                    {
                                    "billing_id": 2472,
                                    "unit_id": 3330,
                                    "unit_name": "Kamisday",
                                    "current_balance": 4040,
                                    "previous_balance": 0,
                                    "charge": 0,
                                    "total": 4040,
                                    "billing_periode": "2020-07-01T00:00:00+07:00",
                                    "billing_start_date": "2020-07-09T00:00:00+07:00",
                                    "billing_end_date": "2020-07-10T00:00:00+07:00",
                                    "billing_status": 0,
                                    "billing_channel_payment": 0,
                                    "product_id": 1161,
                                    "product_name": "Kamis",
                                    "customer_id": 3262,
                                    "customer_name": "Thursday"
                                    },
                                    {
                                    "billing_id": 2472,
                                    "unit_id": 3330,
                                    "unit_name": "Kamisday",
                                    "current_balance": 4040,
                                    "previous_balance": 0,
                                    "charge": 0,
                                    "total": 4040,
                                    "billing_periode": "2020-07-01T00:00:00+07:00",
                                    "billing_start_date": "2020-07-09T00:00:00+07:00",
                                    "billing_end_date": "2020-07-10T00:00:00+07:00",
                                    "billing_status": 0,
                                    "billing_channel_payment": 0,
                                    "product_id": 1161,
                                    "product_name": "Kamis",
                                    "customer_id": 3262,
                                    "customer_name": "Thursday"
                                    },
                                    {
                                    "billing_id": 2472,
                                    "unit_id": 3330,
                                    "unit_name": "Kamisday",
                                    "current_balance": 4040,
                                    "previous_balance": 0,
                                    "charge": 0,
                                    "total": 4040,
                                    "billing_periode": "2020-07-01T00:00:00+07:00",
                                    "billing_start_date": "2020-07-09T00:00:00+07:00",
                                    "billing_end_date": "2020-07-10T00:00:00+07:00",
                                    "billing_status": 0,
                                    "billing_channel_payment": 0,
                                    "product_id": 1161,
                                    "product_name": "Kamis",
                                    "customer_id": 3262,
                                    "customer_name": "Thursday"
                                    },
                                    {
                                    "billing_id": 2472,
                                    "unit_id": 3330,
                                    "unit_name": "Kamisday",
                                    "current_balance": 4040,
                                    "previous_balance": 0,
                                    "charge": 0,
                                    "total": 4040,
                                    "billing_periode": "2020-07-01T00:00:00+07:00",
                                    "billing_start_date": "2020-07-09T00:00:00+07:00",
                                    "billing_end_date": "2020-07-10T00:00:00+07:00",
                                    "billing_status": 0,
                                    "billing_channel_payment": 0,
                                    "product_id": 1161,
                                    "product_name": "Kamis",
                                    "customer_id": 3262,
                                    "customer_name": "Thursday"
                                    },
                                    {
                                    "billing_id": 2472,
                                    "unit_id": 3330,
                                    "unit_name": "Kamisday",
                                    "current_balance": 4040,
                                    "previous_balance": 0,
                                    "charge": 0,
                                    "total": 4040,
                                    "billing_periode": "2020-07-01T00:00:00+07:00",
                                    "billing_start_date": "2020-07-09T00:00:00+07:00",
                                    "billing_end_date": "2020-07-10T00:00:00+07:00",
                                    "billing_status": 0,
                                    "billing_channel_payment": 0,
                                    "product_id": 1161,
                                    "product_name": "Kamis",
                                    "customer_id": 3262,
                                    "customer_name": "Thursday"
                                    },
                                    {
                                    "billing_id": 2472,
                                    "unit_id": 3330,
                                    "unit_name": "Kamisday",
                                    "current_balance": 4040,
                                    "previous_balance": 0,
                                    "charge": 0,
                                    "total": 4040,
                                    "billing_periode": "2020-07-01T00:00:00+07:00",
                                    "billing_start_date": "2020-07-09T00:00:00+07:00",
                                    "billing_end_date": "2020-07-10T00:00:00+07:00",
                                    "billing_status": 0,
                                    "billing_channel_payment": 0,
                                    "product_id": 1161,
                                    "product_name": "Kamis",
                                    "customer_id": 3262,
                                    "customer_name": "Thursday"
                                    },
                                    {
                                    "billing_id": 2472,
                                    "unit_id": 3330,
                                    "unit_name": "Kamisday",
                                    "current_balance": 4040,
                                    "previous_balance": 0,
                                    "charge": 0,
                                    "total": 4040,
                                    "billing_periode": "2020-07-01T00:00:00+07:00",
                                    "billing_start_date": "2020-07-09T00:00:00+07:00",
                                    "billing_end_date": "2020-07-10T00:00:00+07:00",
                                    "billing_status": 0,
                                    "billing_channel_payment": 0,
                                    "product_id": 1161,
                                    "product_name": "Kamis",
                                    "customer_id": 3262,
                                    "customer_name": "Thursday"
                                    },
                                    {
                                    "billing_id": 2472,
                                    "unit_id": 3330,
                                    "unit_name": "Kamisday",
                                    "current_balance": 4040,
                                    "previous_balance": 0,
                                    "charge": 0,
                                    "total": 4040,
                                    "billing_periode": "2020-07-01T00:00:00+07:00",
                                    "billing_start_date": "2020-07-09T00:00:00+07:00",
                                    "billing_end_date": "2020-07-10T00:00:00+07:00",
                                    "billing_status": 0,
                                    "billing_channel_payment": 0,
                                    "product_id": 1161,
                                    "product_name": "Kamis",
                                    "customer_id": 3262,
                                    "customer_name": "Thursday"
                                    },
                                    {
                                    "billing_id": 2472,
                                    "unit_id": 3330,
                                    "unit_name": "Kamisday",
                                    "current_balance": 4040,
                                    "previous_balance": 0,
                                    "charge": 0,
                                    "total": 4040,
                                    "billing_periode": "2020-07-01T00:00:00+07:00",
                                    "billing_start_date": "2020-07-09T00:00:00+07:00",
                                    "billing_end_date": "2020-07-10T00:00:00+07:00",
                                    "billing_status": 0,
                                    "billing_channel_payment": 0,
                                    "product_id": 1161,
                                    "product_name": "Kamis",
                                    "customer_id": 3262,
                                    "customer_name": "Thursday"
                                    },
                                    {
                                    "billing_id": 2472,
                                    "unit_id": 3330,
                                    "unit_name": "Kamisday",
                                    "current_balance": 4040,
                                    "previous_balance": 0,
                                    "charge": 0,
                                    "total": 4040,
                                    "billing_periode": "2020-07-01T00:00:00+07:00",
                                    "billing_start_date": "2020-07-09T00:00:00+07:00",
                                    "billing_end_date": "2020-07-10T00:00:00+07:00",
                                    "billing_status": 0,
                                    "billing_channel_payment": 0,
                                    "product_id": 1161,
                                    "product_name": "Kamis",
                                    "customer_id": 3262,
                                    "customer_name": "Thursday"
                                    },
                                    {
                                    "billing_id": 2472,
                                    "unit_id": 3330,
                                    "unit_name": "Kamisday",
                                    "current_balance": 4040,
                                    "previous_balance": 0,
                                    "charge": 0,
                                    "total": 4040,
                                    "billing_periode": "2020-07-01T00:00:00+07:00",
                                    "billing_start_date": "2020-07-09T00:00:00+07:00",
                                    "billing_end_date": "2020-07-10T00:00:00+07:00",
                                    "billing_status": 0,
                                    "billing_channel_payment": 0,
                                    "product_id": 1161,
                                    "product_name": "Kamis",
                                    "customer_id": 3262,
                                    "customer_name": "Thursday"
                                    },
                                    {
                                    "billing_id": 2472,
                                    "unit_id": 3330,
                                    "unit_name": "Kamisday",
                                    "current_balance": 4040,
                                    "previous_balance": 0,
                                    "charge": 0,
                                    "total": 4040,
                                    "billing_periode": "2020-07-01T00:00:00+07:00",
                                    "billing_start_date": "2020-07-09T00:00:00+07:00",
                                    "billing_end_date": "2020-07-10T00:00:00+07:00",
                                    "billing_status": 0,
                                    "billing_channel_payment": 0,
                                    "product_id": 1161,
                                    "product_name": "Kamis",
                                    "customer_id": 3262,
                                    "customer_name": "Thursday"
                                    },
                                    {
                                    "billing_id": 2472,
                                    "unit_id": 3330,
                                    "unit_name": "Kamisday",
                                    "current_balance": 4040,
                                    "previous_balance": 0,
                                    "charge": 0,
                                    "total": 4040,
                                    "billing_periode": "2020-07-01T00:00:00+07:00",
                                    "billing_start_date": "2020-07-09T00:00:00+07:00",
                                    "billing_end_date": "2020-07-10T00:00:00+07:00",
                                    "billing_status": 0,
                                    "billing_channel_payment": 0,
                                    "product_id": 1161,
                                    "product_name": "Kamis",
                                    "customer_id": 3262,
                                    "customer_name": "Thursday"
                                    },
                                    {
                                    "billing_id": 2472,
                                    "unit_id": 3330,
                                    "unit_name": "Kamisday",
                                    "current_balance": 4040,
                                    "previous_balance": 0,
                                    "charge": 0,
                                    "total": 4040,
                                    "billing_periode": "2020-07-01T00:00:00+07:00",
                                    "billing_start_date": "2020-07-09T00:00:00+07:00",
                                    "billing_end_date": "2020-07-10T00:00:00+07:00",
                                    "billing_status": 0,
                                    "billing_channel_payment": 0,
                                    "product_id": 1161,
                                    "product_name": "Kamis",
                                    "customer_id": 3262,
                                    "customer_name": "Thursday"
                                    },
                                    {
                                    "billing_id": 2472,
                                    "unit_id": 3330,
                                    "unit_name": "Kamisday",
                                    "current_balance": 4040,
                                    "previous_balance": 0,
                                    "charge": 0,
                                    "total": 4040,
                                    "billing_periode": "2020-07-01T00:00:00+07:00",
                                    "billing_start_date": "2020-07-09T00:00:00+07:00",
                                    "billing_end_date": "2020-07-10T00:00:00+07:00",
                                    "billing_status": 0,
                                    "billing_channel_payment": 0,
                                    "product_id": 1161,
                                    "product_name": "Kamis",
                                    "customer_id": 3262,
                                    "customer_name": "Thursday"
                                    },
                                    {
                                    "billing_id": 2472,
                                    "unit_id": 3330,
                                    "unit_name": "Kamisday",
                                    "current_balance": 4040,
                                    "previous_balance": 0,
                                    "charge": 0,
                                    "total": 4040,
                                    "billing_periode": "2020-07-01T00:00:00+07:00",
                                    "billing_start_date": "2020-07-09T00:00:00+07:00",
                                    "billing_end_date": "2020-07-10T00:00:00+07:00",
                                    "billing_status": 0,
                                    "billing_channel_payment": 0,
                                    "product_id": 1161,
                                    "product_name": "Kamis",
                                    "customer_id": 3262,
                                    "customer_name": "Thursday"
                                    }
                                ]
                                }, 200)

            elif args[0] == app.config['URL'] + "/canopus/user_payment/2386":
                return MockResponse({
                                "rescode": "0000",
                                "message": {
                                    "title": "Success",
                                    "body": "Success"
                                },
                                "data": "https://canopus-auth.sumpahpalapa.com/transaction/payment/aadfdb0b2e32ec8c749f84f7"
                                }, 200)
            else:
                return MockResponse(None, 404)


    def mocked_requests_aturtagihan_link_tagihan_1600(*args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code
            
            def json(self):
                return self.json_data
        if len(args) > 0:
            if args[0] == app.config['URL'] + "/billing/list":
                return MockResponse(all_billing_1600, 200)

            elif args[0] == app.config['URL'] + "/canopus/user_payment/2386":
                return MockResponse({
                                "rescode": "0000",
                                "message": {
                                    "title": "Success",
                                    "body": "Success"
                                },
                                "data": "https://canopus-auth.sumpahpalapa.com/transaction/payment/aadfdb0b2e32ec8c749f84f7"
                                }, 200)
            else:
                return MockResponse(None, 404)

    def mocked_requests_aturtagihan_link_tagihan_no_tagihan(*args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code
            
            def json(self):
                return self.json_data
        if len(args) > 0:
            if args[0] == app.config['URL'] + "/billing/list":
                return MockResponse({
                        "rescode": "0000",
                        "message": {
                            "title": "Success",
                            "body": "Success"
                        },
                        "data": []}, 200)
            else:
                return MockResponse(None, 404)

    @mock.patch('requests.post', side_effect=mocked_requests_aturtagihan_link_tagihan_no_tagihan)
    def test_check_link_tagihan_no_tagihan(self, get_mock, client):
        data = send_message("6281320003997", "beranda")

        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                        headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')

        data = send_message("6281320003997", "riwayat tagihan")
        
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                        headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')

        data = send_message("6281320003997", "generate link")

        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')

    @mock.patch('requests.post', side_effect=mocked_requests_aturtagihan_link_tagihan_success)
    def test_check_link_tagihan_success(self, get_mock, client):
        data = send_message("6281320003997", "2")

        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')

    @mock.patch('requests.post', side_effect=mocked_requests_aturtagihan_link_tagihan_success)
    def test_check_link_tagihan_unsuccess(self, get_mock, client):
        data = send_message("6281320003997", "generate link")

        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')

        data = send_message("6281320003997", "100000")

        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')

    @mock.patch('requests.post', side_effect=mocked_requests_aturtagihan_link_tagihan_1600)
    def test_check_riwayat_tagihan_1(self, get_mock, client):
        data = send_message("6281320003997", "beranda")

        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')

        data = send_message("6281320003997", "riwayat tagihan")

        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')

        data = send_message("6281320003997", "1")

        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')

    @mock.patch('requests.post', side_effect=mocked_requests_aturtagihan_link_tagihan_1600)
    def test_check_riwayat_tagihan_2(self, get_mock, client):
        data = send_message("6281320003997", "beranda")

        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')

        data = send_message("6281320003997", "riwayat tagihan")

        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')

        data = send_message("6281320003997", "2")

        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')

    @mock.patch('requests.post', side_effect=mocked_requests_aturtagihan_link_tagihan_1600)
    def test_check_riwayat_tagihan_3(self, get_mock, client):
        data = send_message("6281320003997", "beranda")

        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')

        data = send_message("6281320003997", "riwayat tagihan")

        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')

        data = send_message("6281320003997", "3")

        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')
