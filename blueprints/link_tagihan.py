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

# Menu awal Produk
def link_tagihan(incoming_msg, phone_number, bot_responses):
    respon_billing = requests.post(app.config['URL']+"/billing/list", headers={"Authorization": "Bearer " + save_redis.get("%s::token" %(phone_number))})
    respon_billing = respon_billing.json()
    list_billing = respon_billing['data']
    message = []

    if save_redis.get("%s::menu" %(phone_number)) == "link":
        if list_billing != 0:
            message_bubble = [bot_responses]
            all_bubble = []
            for index, item in enumerate(list_billing):
                tiap_data = []
                tiap_data.append("%s. Pelanggan: %s" %(index+1, item['customer_name']))
                tiap_data.append("    Produk: %s" % (item['product_name']))
                tiap_data.append("    Unit: %s" % (item['unit_name']))

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
            message.append("Anda belum mengisi tagihan! Isi dulu yuk di menu *buat tagihan*")

        message.append("Silakan ketik no tagihan yang ingin Anda buat Link-nya")
        pesan = []
        pesan.append("Ketik *Pengaturan* untuk ke halaman Pengaturan")
        pesan.append("Ketik *Beranda* untuk kembali ke halaman Beranda")
        message.append(("\n").join(pesan))

        save_redis.set("%s::menu" %(phone_number), json.dumps({"link": "tambah"}))

    elif json.loads(save_redis.get("%s::menu" %(phone_number)))['link'] == 'tambah':
        no_billing = re.findall(".+", incoming_msg)
        no_billing = regex_num(no_billing[0])
        if int(no_billing) > len(list_billing):
            message.append("Nomor Tagihan yang Anda masukkan tidak tersedia! Pilih lagi yuk nomornya")
            message.append("")
            message.append("Silakan ketik *Tagihan* untuk membuat tagihan atau ketik *Link* untuk ke halaman sebelumnya")
        else:
            tambah = requests.post(app.config['URL']+"/canopus/user_payment/" + str(list_billing[int(no_billing) - 1]['billing_id']), headers={"Authorization": "Bearer " + save_redis.get("%s::token" %(phone_number))})
            send_wa = requests.post(app.config['URL']+"/billing/send/wa",
                                    headers={"Authorization": "Bearer " + save_redis.get("%s::token" %(phone_number))},
                                    json={
                                        "billing_id":int(list_billing[int(no_billing) - 1]['billing_id'])
                                    }
                                   )
            respon_link = tambah.json()
            if tambah.status_code == 200:
                message.append("Klik tautan di bawah ini untuk mengirim Link Tagihan ke pelanggan Anda melalui whatsapp")
                send_wa = send_wa.json()["data"]["wa_template"]
                send_wa = send_wa.replace(" ", "%20")
                message.append(send_wa)
                message.append("Atau kirim Link Tagihan berikut ini ke pelanggan Anda secara manual")
                message.append(respon_link['data'])
            else:
                message.append(respon_link["message"]["body"])
                message.append("Link Tagihan gagal dibuat! ")

            pesan = []
            pesan.append("Ketik *Link* untuk kembali ke halaman link")
            pesan.append("Ketik *Pengaturan* untuk kembali ke halaman Pengaturan")
            pesan.append("Ketik *Beranda* untuk kembali ke halaman Beranda")
            message.append(("\n").join(pesan))
            save_redis.set("%s::menu" %(phone_number), "link")

    return message
