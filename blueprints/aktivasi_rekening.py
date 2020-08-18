import requests
import re
import config
import json
from blueprints import app
from blueprints import save_redis
from flask import Flask
from flask import request
from functions import regex
from functions import regex_num

# Menu awal aktivasi rekening
def aktivasi_rekening(incoming_msg, phone_number, bot_responses):
    respon_produk = requests.post(app.config['URL']+"/product/all", headers={"Authorization": "Bearer " + save_redis.get("%s::token" %(phone_number))})
    respon_produk = respon_produk.json()
    list_produk = respon_produk["data"]['records']
    message = []

    if save_redis.get("%s::menu" %(phone_number)) == "aktivasi_rekening":
        if respon_produk["data"]["count"] != 0:
            message.append(bot_responses)
            message_bubble = [""]
            all_bubble = []
            for index, item in enumerate(list_produk):
                tiap_data = []
                tiap_data.append("%s. Nama: %s" % (index+1, item['name']))
                tiap_data.append("    Bank: %s %s a.n %s \n" % (item['bank_name'], item['account_number'], item['account_name']))
                tiap_data = ('\n').join(tiap_data)
                if len(message_bubble[0]) + len(tiap_data) < 1600:
                    message_bubble.append(tiap_data)
                    message_bubble = ('\n').join(message_bubble)
                    message_bubble = [message_bubble]
                else:
                    all_bubble.append(message_bubble)
                    message_bubble = ['']
                    message_bubble.append(tiap_data)
                    message_bubble = ('\n').join(message_bubble)
                    message_bubble = [message_bubble]
            all_bubble.append(message_bubble)
            for bubble in all_bubble:
                message.append(bubble)

        else:
            message.append("Anda belum mengisi produk!")

        message.append("Silakan ketik no produk yang rekeningnya ingin Anda aktivasi")
        pesan = []
        pesan.append("Ketik *Pengaturan* untuk kembali ke halaman Pengaturan")
        pesan.append("Ketik *Beranda* untuk kembali ke halaman Beranda")
        message.append(("\n").join(pesan))
        save_redis.set("%s::menu" %(phone_number), json.dumps({"aktivasi_rekening": "aktivasi"}))

    else:
        no_produk = re.findall(".+", incoming_msg)
        no_produk = regex_num(no_produk[0])
        if int(no_produk) > len(list_produk):
            message.append("Nomor Produk yang Anda masukkan tidak tersedia!")
        else:
            tambah = requests.put(app.config['URL']+"/product/account/" + str(list_produk[int(no_produk)-1]['id']),
                                  headers={"Authorization": "Bearer " + save_redis.get("%s::token" %(phone_number))},
                                  json={
                "bank_code": list_produk[int(no_produk)-1]['bank_code'],
                "account_number": list_produk[int(no_produk)-1]['account_number'],
                "account_name": list_produk[int(no_produk)-1]['account_name']
            })

            login_admin = requests.post(app.config['URL']+"/users/login", json={"email": app.config['USERNAME'], "password": app.config['PASSWORD']})
            login_admin = login_admin.json()
            token_admin = login_admin['data']['access_token']

            aktivasi_admin = requests.post(app.config['URL']+"/product/account/activate/" + str(list_produk[int(no_produk)-1]['id']),
                                           headers={"Authorization": "Bearer " + token_admin},
                                           json={
                "bank_code": list_produk[int(no_produk)-1]['bank_code'],
                "account_number": list_produk[int(no_produk)-1]['account_number'],
                "account_name": list_produk[int(no_produk)-1]['account_name']
            })

            if aktivasi_admin.status_code == 200:
                message.append("Nomor Rekening berhasil diaktivasi! Sekarang Anda bisa melakukan penagihan dengan cepat dan penghuni Anda bisa melakukan pembayaran dengan mudah :)")
            elif aktivasi_admin.status_code == 400:
                message.append(aktivasi_admin.json()["message"]["body"])
                message.append("Nomor Rekening sudah pernah diaktivasi!")
            else:
                message.append(aktivasi_admin.json()["message"]["body"])
                message.append("Nomor Rekening gagal diaktivasi! Apakah Nomor Rekening tersebut sudah benar? Mungkin bisa dicek lagi ya..")

        pesan = []
        pesan.append("Ketik *Aktivasi Rekening* untuk kembali ke halaman Aktivasi Rekening")
        pesan.append("Ketik *Pengaturan* untuk kembali ke halaman Pengaturan")
        pesan.append("Ketik *Beranda* untuk kembali ke halaman Beranda")
        message.append(("\n").join(pesan))
        save_redis.set("%s::menu" %(phone_number), "aktivasi_rekening")

    return message
