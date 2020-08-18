from unittest import mock
from unittest.mock import patch
import pytest
from flask import request
import json
import redis
from . import client

with open("tests/product/get_all_1600.json") as file:
    all_produk = json.load(file)
    
with open("tests/aktivasi_rekening/aktivasi_rekening.json") as file:
    aktivasi_rekening = json.load(file)

class TestAktivasiRekening():
    def mocked_requests_get(*args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code
            def json(self):
                return self.json_data
        if args[0] == "https://messages-sandbox.nexmo.com/v0.1/messages":
            return MockResponse({"message_uuid":"e4b1a241-1172-4fd4-9b12-7c82ce2f1517"}, 202)
    
    def mocked_requests_aturtagihan_aktivasi_rekening(*args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code
            
            def json(self):
                return self.json_data
        if len(args) > 0:
            if args[0] == "https://magellan.sumpahpalapa.com/api/v1/product/all":
                return MockResponse(all_produk, 200)

            elif args[0] == "https://magellan.sumpahpalapa.com/api/v1/product/account/1129":
                return MockResponse(aktivasi_rekening,200)
                
            elif args[0] == "https://magellan.sumpahpalapa.com/api/v1/users/login":
                return MockResponse({
                        "rescode": "0000",
                        "message": {
                            "title": "Success",
                            "body": "Success"
                        },
                        "data": {
                            "id": 7014,
                            "created_at": "2020-06-14T03:24:24+07:00",
                            "created_by": 0,
                            # "updated_at": null,
                            # "updated_by": null,
                            # "deleted_at": null,
                            # "deleted_by": null,
                            "name": "Admin Alta",
                            "username": "adminalta",
                            "password": "$2a$08$X2ZhEL4ioWcDUshiCJYyZuO37UKArd2boE0YonmmLf5YlHZBQ/DLW",
                            "email": "adminalta@gmail.com",
                            "phone": "087746734175",
                            "role_id": 1,
                            "is_active": 1,
                            "is_admin": False,
                            # "company_id": null,
                            "company_name": "",
                            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE1OTQzNjkzMzMsImlkIjo3MDE0LCJpc19hZG1pbiI6ZmFsc2UsInJvbGVfaWQiOjF9.WbTEWub80xsD5tQGZIySS2u5rAnHt_X1qLlz0mx4x9M",
                            "expired_token": "2020-07-10T08:22:13.526376005Z"
                        }
                    },200)

            elif args[0] == "https://magellan.sumpahpalapa.com/api/v1/product/account/activate/1129":
                return MockResponse({
                            "rescode": "0000",
                            "message": {
                                "title": "Success",
                                "body": "Success"
                            },
                            "data": "Success Activating Payment"
                            },200)

            else:
                return MockResponse(None, 404)

    def mocked_requests_aturtagihan_aktivasi_rekening_400(*args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code
            
            def json(self):
                return self.json_data
        if len(args) > 0:
            if args[0] == "https://magellan.sumpahpalapa.com/api/v1/product/all":
                return MockResponse(all_produk, 200)

            elif args[0] == "https://magellan.sumpahpalapa.com/api/v1/product/account/1129":
                return MockResponse( {
                            "rescode": "0000",
                            "message": {
                                "title": "Success",
                                "body": "Success"
                            },
                            "data": {
                                "id": 1158,
                                "created_at": "2020-07-07T16:16:51+07:00",
                                "created_by": 7002,
                                "updated_at": "2020-07-07T16:22:02+07:00",
                                "updated_by": 7002,
                                # "deleted_at": null,
                                # "deleted_by": null,
                                "name": "Testing Plis",
                                "description": "Jalan Testing Perumahan 1 no 1",
                                "product_type_id": 2,
                                "product_type_name": "perumahan",
                                "user_id": 7002,
                                "logo": "",
                                "signature": "",
                                "start_date": 1,
                                "end_date": 15,
                                "invoice_description": "mush is the best",
                                "bank_code": "002",
                                "bank_name": "BANK BRI",
                                "account_number": "900928374",
                                "account_name": "mush",
                                "payment_activation": 1,
                                "email_template": "",
                                "sms_template": "",
                                "wa_template": ""
                            }
                        },200)
                
            elif args[0] == "https://magellan.sumpahpalapa.com/api/v1/users/login":
                return MockResponse({
                        "rescode": "0000",
                        "message": {
                            "title": "Success",
                            "body": "Success"
                        },
                        "data": {
                            "id": 7014,
                            "created_at": "2020-06-14T03:24:24+07:00",
                            "created_by": 0,
                            # "updated_at": null,
                            # "updated_by": null,
                            # "deleted_at": null,
                            # "deleted_by": null,
                            "name": "Admin Alta",
                            "username": "adminalta",
                            "password": "$2a$08$X2ZhEL4ioWcDUshiCJYyZuO37UKArd2boE0YonmmLf5YlHZBQ/DLW",
                            "email": "adminalta@gmail.com",
                            "phone": "087746734175",
                            "role_id": 1,
                            "is_active": 1,
                            "is_admin": False,
                            # "company_id": null,
                            "company_name": "",
                            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE1OTQzNjkzMzMsImlkIjo3MDE0LCJpc19hZG1pbiI6ZmFsc2UsInJvbGVfaWQiOjF9.WbTEWub80xsD5tQGZIySS2u5rAnHt_X1qLlz0mx4x9M",
                            "expired_token": "2020-07-10T08:22:13.526376005Z"
                        }
                    },200)

            elif args[0] == "https://magellan.sumpahpalapa.com/api/v1/product/account/activate/1129":
                return MockResponse({
                            "rescode": "0000",
                            "message": {
                                "title": "Success",
                                "body": "Success"
                            },
                            "data": "Success Activating Payment"
                            },400)

            else:
                return MockResponse(None, 404)

    def mocked_requests_aturtagihan_aktivasi_rekening_500(*args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code
            
            def json(self):
                return self.json_data
        if len(args) > 0:
            if args[0] == "https://magellan.sumpahpalapa.com/api/v1/product/all":
                return MockResponse(all_produk, 200)

            elif args[0] == "https://magellan.sumpahpalapa.com/api/v1/product/account/1129":
                return MockResponse( {
                            "rescode": "0000",
                            "message": {
                                "title": "Success",
                                "body": "Success"
                            },
                            "data": {
                                "id": 1158,
                                "created_at": "2020-07-07T16:16:51+07:00",
                                "created_by": 7002,
                                "updated_at": "2020-07-07T16:22:02+07:00",
                                "updated_by": 7002,
                                # "deleted_at": null,
                                # "deleted_by": null,
                                "name": "Testing Plis",
                                "description": "Jalan Testing Perumahan 1 no 1",
                                "product_type_id": 2,
                                "product_type_name": "perumahan",
                                "user_id": 7002,
                                "logo": "",
                                "signature": "",
                                "start_date": 1,
                                "end_date": 15,
                                "invoice_description": "mush is the best",
                                "bank_code": "002",
                                "bank_name": "BANK BRI",
                                "account_number": "900928374",
                                "account_name": "mush",
                                "payment_activation": 1,
                                "email_template": "",
                                "sms_template": "",
                                "wa_template": ""
                            }
                        },200)
                
            elif args[0] == "https://magellan.sumpahpalapa.com/api/v1/users/login":
                return MockResponse({
                        "rescode": "0000",
                        "message": {
                            "title": "Success",
                            "body": "Success"
                        },
                        "data": {
                            "id": 7014,
                            "created_at": "2020-06-14T03:24:24+07:00",
                            "created_by": 0,
                            # "updated_at": null,
                            # "updated_by": null,
                            # "deleted_at": null,
                            # "deleted_by": null,
                            "name": "Admin Alta",
                            "username": "adminalta",
                            "password": "$2a$08$X2ZhEL4ioWcDUshiCJYyZuO37UKArd2boE0YonmmLf5YlHZBQ/DLW",
                            "email": "adminalta@gmail.com",
                            "phone": "087746734175",
                            "role_id": 1,
                            "is_active": 1,
                            "is_admin": False,
                            # "company_id": null,
                            "company_name": "",
                            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE1OTQzNjkzMzMsImlkIjo3MDE0LCJpc19hZG1pbiI6ZmFsc2UsInJvbGVfaWQiOjF9.WbTEWub80xsD5tQGZIySS2u5rAnHt_X1qLlz0mx4x9M",
                            "expired_token": "2020-07-10T08:22:13.526376005Z"
                        }
                    },200)

            elif args[0] == "https://magellan.sumpahpalapa.com/api/v1/product/account/activate/1129":
                return MockResponse({
                            "rescode": "0000",
                            "message": {
                                "title": "Success",
                                "body": "Success"
                            },
                            "data": "Success Activating Payment"
                            },500)

            else:
                return MockResponse(None, 404)

    def mocked_requests_aturtagihan_aktivasi_rekening_no_produk(*args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code
            
            def json(self):
                return self.json_data
        if len(args) > 0:
            if args[0] == "https://magellan.sumpahpalapa.com/api/v1/product/all":
                return MockResponse({
                        "rescode": "0000",
                        "message": {
                            "title": "Success",
                            "body": "Success"
                        },
                        "data": {
                            "count": 0,
                            "pages": 1,
                            "records": [
                                {
                                    "id": 1129,
                                    "created_at": "2020-06-19T17:34:45+07:00",
                                    "created_by": 7002,
                                    "updated_at": "2020-06-23T13:10:04+07:00",
                                    "updated_by": 7002,
                                    # "deleted_at": null,
                                    # "deleted_by": null,
                                    "name": "PT Testing add Prod",
                                    "description": "Jalan Tidak Tahu",
                                    "product_type_id": 108,
                                    "product_type_name": "Kos",
                                    "user_id": 7002,
                                    "logo": "",
                                    "signature": "",
                                    "start_date": 1,
                                    "end_date": 5,
                                    "invoice_description": "",
                                    "bank_code": "002",
                                    "bank_name": "BANK BRI",
                                    "account_number": "900928374",
                                    "account_name": "Rizki Pangestu",
                                    "payment_activation": 1,
                                    "email_template": "",
                                    "sms_template": "",
                                    "wa_template": ""
                                }
                            ],
                            "offset": 0,
                            "limit": 30,
                            "page": 1,
                            "prevPage": 1,
                            "nextPage": 1
                        }
                }, 200)
            else:
                return MockResponse(None, 404)

    @mock.patch('requests.post', side_effect=mocked_requests_aturtagihan_aktivasi_rekening_no_produk)
    def test_check_aktivasi_rekening_no_produk(self, get_mock, client):        

        data = {
            "from": { "type": "whatsapp", "number": "14157386170" },
            "to": { "type": "whatsapp", "number": "6281320003997" },
            "message": {
                "content": {
                    "type": "text",
                    "text": "pengaturan"
                }
            }
        }
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')
                
        data = {
            "from": { "type": "whatsapp", "number": "14157386170" },
            "to": { "type": "whatsapp", "number": "6281320003997" },
            "message": {
                "content": {
                    "type": "text",
                    "text": "aktivasi rekening"
                }
            }
        }
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')
        
    @mock.patch('requests.post', side_effect=mocked_requests_aturtagihan_aktivasi_rekening)
    def test_check_aktivasi_rekening(self, get_mock, client):        

        data = {
            "from": { "type": "whatsapp", "number": "14157386170" },
            "to": { "type": "whatsapp", "number": "6281320003997" },
            "message": {
                "content": {
                    "type": "text",
                    "text": "1000"
                }
            }
        }
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')
        
        data = {
            "from": { "type": "whatsapp", "number": "14157386170" },
            "to": { "type": "whatsapp", "number": "6281320003997" },
            "message": {
                "content": {
                    "type": "text",
                    "text": "aktivasi rekening"
                }
            }
        }
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')

        data = {
            "from": { "type": "whatsapp", "number": "14157386170" },
            "to": { "type": "whatsapp", "number": "6281320003997" },
            "message": {
                "content": {
                    "type": "text",
                    "text": "1"
                }
            }
        }
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')

    @mock.patch('requests.post', side_effect=mocked_requests_aturtagihan_aktivasi_rekening_400)
    def test_check_aktivasi_rekening_400(self, get_mock, client):        
                
        data = {
            "from": { "type": "whatsapp", "number": "14157386170" },
            "to": { "type": "whatsapp", "number": "6281320003997" },
            "message": {
                "content": {
                    "type": "text",
                    "text": "aktivasi rekening"
                }
            }
        }
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')
        
        data = {
            "from": { "type": "whatsapp", "number": "14157386170" },
            "to": { "type": "whatsapp", "number": "6281320003997" },
            "message": {
                "content": {
                    "type": "text",
                    "text": "1"
                }
            }
        }
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')

    @mock.patch('requests.post', side_effect=mocked_requests_aturtagihan_aktivasi_rekening_500)
    def test_check_aktivasi_rekening_500(self, get_mock, client):        
                
        data = {
            "from": { "type": "whatsapp", "number": "14157386170" },
            "to": { "type": "whatsapp", "number": "6281320003997" },
            "message": {
                "content": {
                    "type": "text",
                    "text": "aktivasi rekening"
                }
            }
        }
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')
        
        data = {
            "from": { "type": "whatsapp", "number": "14157386170" },
            "to": { "type": "whatsapp", "number": "6281320003997" },
            "message": {
                "content": {
                    "type": "text",
                    "text": "1"
                }
            }
        }
        res = client.post('/webhooks/inbound-message',
                            data=json.dumps(data),
                            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1OTM1ODI4NDksImV4cCI6MTU5NDEwMTI0OSwianRpIjoiSVplVWxsbWVxeUR4IiwiYXBwbGljYXRpb25faWQiOiI2Nzg1NTA4NS01ZTUyLTQ2MmUtYjFmNC1lYzE0YTY2MWRmNDMifQ.mOEdzJFRT_EmcPN3ChQ4S_iYtJWxdXfCV5EECcAk1EnT9T_RCegFRArX0bBmYeLy_2VGg83TC_MDwxkS5IRpOvI5ihSTv_8f2Hn0J5wQ9LScaFH5YHJCsXB3iXyGVs7sd2vCH4BJR6JFY3A2OcK6VxNFONiCVuI4FozZCme2pvxBiAcsC-xcvORQ9i299Q4O9osWBmdgrqfjYTYKCX42wt76_mYaRQNlVofq-FGD31TZUSnnvvS-0XCVFemTWFZDdO9Zc7yoL4sT01EREJjiYgwuy98dAK-zZQ9AEc0Go_2thQArLoiUPYd1pNT-hOA9meYSPBp1qRegVr6U-FulLg'},
                            content_type='application/json')

