import requests, re
import locale
import config
from blueprints import app
from flask import Flask, request
from datetime import datetime

def bot_reply(send_message, phone_number):
    url = "https://messages-sandbox.nexmo.com/v0.1/messages"
    payload = {
        "from": { "type": "whatsapp", "number": "14157386170" },
        "to": { "type": "whatsapp", "number": phone_number },
        "message": {
            "content": {
                "type": "text",
                "text": send_message
            }
        }
    }
    headers = {
        'Authorization': 'Bearer ' + app.config['TOKEN'],
        'Content-Type': 'application/json',
        'Cookie': '__cfduid=' + app.config['COOKIE']
    }
    response = requests.request("POST", url, headers=headers, json = payload)

def regex(value):
    value = value.strip()
    if ":" in value:
        value = re.findall(":.+\S+$", value)
        value = value[0].replace(":","")
    else:
        value = re.findall(".+\S+$", value)
    value = value.strip()
    return value

def regex_num(value):
    if ":" in value:
        value = re.findall(":.\d*", value)
        value = value[0].replace(":","")
        value = value.strip()
    else:
        value = re.findall("\d[0-9]*", value)
        value = value[0].strip()
    return value

def formatrupiah(uang):
    y = str(uang)
    if len(y) <= 3 :
        return 'Rp ' + y     
    else :
        p = y[-3:]
        q = y[:-3]
        return formatrupiah(q) + '.' + p

def convertDate(waktu):
    formatIso = datetime.strptime(waktu[:-6], "%Y-%m-%dT%H:%M:%S")
    return formatIso.strftime("%a, %d %b %Y")