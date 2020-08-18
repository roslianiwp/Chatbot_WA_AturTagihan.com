import pytest 
import logging
import json
import hashlib
import uuid
import os
from blueprints import app
from flask import Flask, request, json

def call_client(request):
    client = app.test_client()
    return client

@pytest.fixture
def client(request):
    return call_client(request)

