import re
import json
import config
import requests
from blueprints import app
from blueprints import save_redis
from flask import Flask
from flask import request
from functions import regex

def register(incoming_msg, phone_number, bot_responses):
    message = []
    
    # user diminta memasukkan nama lengkap
    if save_redis.get("%s::menu"%(phone_number)) == "daftar":
        message.append("Pertama, silakan masukkan Nama Lengkap Anda")
        save_redis.set("%s::menu"%(phone_number), json.dumps({"daftar":"nama"}))
    
    # user diminta memasukkan username
    # menyimpan data nama
    elif json.loads(save_redis.get("%s::menu"%(phone_number)))["daftar"] == "nama":
        incoming_msg = incoming_msg.strip()
        save_redis.set("%s::nama" %(phone_number), incoming_msg)
        save_redis.set("%s::menu" %(phone_number), json.dumps({'daftar':'username'}))
        message.append("Baik %s senang berkenalan denganmu!" %(incoming_msg))
        message.append("Sekarang, masukkan Username yang Anda inginkan")
    
    # user diminta memasukkan password
    # menyimpan data username
    elif json.loads(save_redis.get("%s::menu"%(phone_number)))["daftar"] == "username":
        incoming_msg = incoming_msg.strip()
        save_redis.set("%s::username" %(phone_number), incoming_msg)
        save_redis.set("%s::menu" %(phone_number), json.dumps({'daftar':'password'}))
        message.append("Selanjutnya, silakan masukkan Password Anda")
        message.append("Hedwig infokan ya, password harus berisi 8-16 karakter yang terdiri dari angka, huruf, karakter atau perpaduannya")
        
    # user diminta memasukkan email
    # menyimpan data password
    elif json.loads(save_redis.get("%s::menu"%(phone_number)))["daftar"] == "password":
        incoming_msg = incoming_msg.strip()
        incoming_msg_regex = re.findall("^[A-Za-z0-9!@#$%^&*-_+=]{8,16}$", incoming_msg)
        
        # format password benar
        if incoming_msg_regex != []:
            save_redis.set("%s::password" %(phone_number), incoming_msg_regex[0])
            save_redis.set("%s::menu" %(phone_number), json.dumps({'daftar':'email'}))
            message.append("Lalu, masukkan Email Anda")
        
        # format password salah
        else:
            message.append("Password yang Anda masukkan tidak sesuai")
            message.append("Password harus berisi 8-16 karakter yang terdiri dari angka, huruf, karakter atau perpaduannya")
            message.append("Silakan masukkan kembali Password Anda")
            
    # user diminta memasukkan telepon
    # menyimpan data email
    elif json.loads(save_redis.get("%s::menu"%(phone_number)))["daftar"] == "email":
        incoming_msg = incoming_msg.strip()
        incoming_msg_regex = re.findall("^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$", incoming_msg)
        
        # format email benar
        if incoming_msg_regex != []:
            save_redis.set("%s::email" %(phone_number), incoming_msg_regex[0])
            save_redis.set("%s::menu" %(phone_number), json.dumps({'daftar':'telepon'}))
            message.append("Hedwig belum tau nomor teleponmu nih! Masukkan Nomor Telepon Anda yuk")
        
        # format email salah
        else:
            message.append("Email yang Anda masukkan tidak sesuai")
            message.append("Silahkan masukkan kembali Email Anda")
            
    # user diminta memasukkan nama perusahaan
    # menyimpan data telepon
    elif json.loads(save_redis.get("%s::menu"%(phone_number)))["daftar"] == "telepon":
        incoming_msg = incoming_msg.strip()
        save_redis.set("%s::telepon" %(phone_number), incoming_msg)
        save_redis.set("%s::menu" %(phone_number), json.dumps({'daftar':'perusahaan'}))
        message.append("Terakhir, masukkan Nama Perusahaan Anda")
        
    # menyimpan data nama perusahaan
    elif json.loads(save_redis.get("%s::menu"%(phone_number)))["daftar"] == "perusahaan":
        incoming_msg = incoming_msg.strip()
        
        rq_register = requests.post(app.config['URL']+"/users/register",
                                    json={
                                        "name": save_redis.get("%s::nama" %(phone_number)),
                                        "username": save_redis.get("%s::username" %(phone_number)),
                                        "password": save_redis.get("%s::password" %(phone_number)),
                                        "email": save_redis.get("%s::email" %(phone_number)),
                                        "phone": save_redis.get("%s::telepon" %(phone_number)),
                                        "company_name": incoming_msg,
        })
        resp_register = rq_register.json()
        if resp_register['message']['title'] == 'Success':
            message = []
            rq_login = requests.post(app.config['URL']+"/users/login",
                                     json={
                                         "email": save_redis.get("%s::email" %(phone_number)),
                                         "password": save_redis.get("%s::password" %(phone_number))
            })
            resp_login = rq_login.json()
            save_redis.set("%s::token" %(phone_number), resp_login["data"]["access_token"])
            save_redis.set("%s::name" %(phone_number), resp_login["data"]["name"])
            message.append("Anda berhasil terdaftar")
            
            message.append("Halo %s! Hedwig siap membantu.. " %(save_redis.get("%s::name"%(phone_number))))
            
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
        else:
            send_message = []
            send_message.append("Akun Anda gagal terdaftar")
            send_message.append(resp_register["message"]["body"])
            message.append(('\n').join(send_message))
            
            send_message = ["Ketik *Daftar* untuk mendaftar lagi"]
            send_message.append("Ketik *Masuk* untuk masuk")
            
        save_redis.delete("%s::menu"%(phone_number),"")
        save_redis.delete("%s::nama" %(phone_number))
        save_redis.delete("%s::username" %(phone_number))
        save_redis.delete("%s::password" %(phone_number))
        save_redis.delete("%s::email" %(phone_number))
        save_redis.delete("%s::telepon" %(phone_number))
        
    return message