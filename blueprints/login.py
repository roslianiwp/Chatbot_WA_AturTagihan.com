import requests
import re
import config
import json
from blueprints import app
from blueprints import save_redis
from flask import Flask
from flask import request
from functions import regex

def login(incoming_msg, phone_number, bot_responses):
    message = []
    
    # user diminta memasukkan email
    if save_redis.get("%s::menu" %(phone_number)) == "login":
        message.append("Pertama, silakan ketik Email Anda")
        save_redis.set("%s::menu" %(phone_number), json.dumps({"login":"email"})) 
    
    # user diminta memasukkan password
    # menyimpan data email
    elif json.loads(save_redis.get("%s::menu" %(phone_number)))["login"] == "email" :
        email = re.findall("^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$", incoming_msg)
        
        # format email benar
        if email != []:
            save_redis.set("%s::email" %(phone_number), email[0])
            save_redis.set("%s::menu" %(phone_number), json.dumps({'login':'password'}))
            message.append("Baik, email Anda adalah %s" % (email[0]))
            message.append("Terakhir, silakan ketik Password Anda")
        
        # format email salah
        else:
            message.append("Email yang Anda masukkan tidak sesuai")
            message.append("Silakan masukkan kembali Email Anda")

    # menyimpan data password
    elif json.loads(save_redis.get("%s::menu" %(phone_number)))['login'] == 'password':
        passwordstr = re.findall(".+\S+$", incoming_msg)
        rq_login = requests.post(app.config['URL']+"/users/login", json={"email":save_redis.get("%s::email" %(phone_number)), "password":passwordstr[0]})
        resp_login = rq_login.json()
        print("+++++++++++++++++ email: ", save_redis.get("%s::email" %(phone_number)))
        print("+++++++++++++++++ password: ", passwordstr[0])
        if rq_login.status_code == 200:
            message = []
            save_redis.set("%s::token" %(phone_number), resp_login["data"]["access_token"])
            save_redis.set("%s::name" %(phone_number), resp_login["data"]["name"])
            message.append("Halo %s!" %(save_redis.get("%s::name"%(phone_number))))
            message.append("Anda berhasil masuk! Sekarang Anda bisa akses fitur-fitur Hedwig")
            
            send_message = ["Apa yang bisa Hedwig bantu?"]
            send_message.append("1. *buat tagihan* - membuat tagihan")
            send_message.append("2. *riwayat tagihan* - melihat riwayat tagihan")
            send_message.append("3. *pengaturan* - untuk masuk ke menu produk, jenis tagihan, jenis unit, harga, formula, pelanggan, unit, dan aktivasi rekening")
            send_msg = ["Silakan pilih menu yang Anda inginkan ya"]
            send_msg.append("")
            send_msg.append("(contoh: *1* atau *buat tagihan*)")
            message.append(("\n").join(send_message))
            message.append(("\n").join(send_msg))
            
            save_redis.set("%s::submenu"%(phone_number),"beranda")
        else :
            message = []
            message.append("Email / Password salah. Ulangi masuk dengan ketik *masuk* atau ketik *registrasi* untuk mendaftarkan akun Anda")
        
        save_redis.delete("%s::email" %(phone_number), "")
        save_redis.delete("%s::menu"%(phone_number), "")

    return message
