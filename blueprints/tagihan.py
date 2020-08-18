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
def tagihan(incoming_msg, phone_number, bot_responses):
    respon_produk = requests.post(app.config['URL']+"/product/all", headers={"Authorization": "Bearer " + save_redis.get("%s::token" %(phone_number))})
    respon_produk = respon_produk.json()
    list_produk = respon_produk["data"]['records']
    unit = requests.post(app.config['URL']+"/unit/all", headers={"Authorization": "Bearer " + save_redis.get("%s::token" %(phone_number))})
    respon_unit = unit.json()
    list_unit = respon_unit['data']['records']
    message = []

    if save_redis.get("%s::menu" %(phone_number)) == "tagihan":
        if respon_produk["data"]["count"] != 0:
            message_bubble = ["Ini adalah daftar Produknya %s: " %(save_redis.get("%s::name" %(phone_number)))]
            all_bubble = []
            for index, item in enumerate(list_produk):
                tiap_data = []
                tiap_data.append("%s. Nama: %s" % (index+1, item['name']))
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
            message.append("Sekarang, ketik no produk yang ingin dibuat tagihannya")

        else:
            message.append("Anda belum mengisi produk! Isi dulu yuk produknya..")

        pesan = []
        pesan.append("Ketik *Pengaturan* untuk kembali ke halaman Pengaturan")
        pesan.append("Ketik *Beranda* untuk kembali ke halaman Beranda")
        message.append(("\n").join(pesan))
        save_redis.set("%s::menu" %(phone_number), json.dumps({"tagihan": "tambah"}))

    elif json.loads(save_redis.get("%s::menu" %(phone_number)))['tagihan'] == 'tambah':
        no_produk = re.findall(".+", incoming_msg)
        no_produk = regex_num(no_produk[0])
        if int(no_produk) > len(list_produk):
            message.append("Nomor Produk yang Anda masukkan tidak ada! Isi lagi yuk pakai Nomor Produk yang lain..")
            message.append("")
            message.append("Atau Anda bisa ketik *tagihan* untuk kembali ke halaman sebelumnya")
        else:
            save_redis.set("%s::id_produk" %(phone_number), list_produk[int(no_produk) - 1]['id'])
            message.append("Selanjutnya, pilih nomor Unit Anda")
            jml_unit = 0
            pesan = []
            for index, unit in enumerate(list_unit):
                if list_produk[int(no_produk) - 1]['id'] == unit['product_id']:
                    pesan.append("%s. %s" % (index+1, unit['name']))
                    jml_unit += 1
            message.append("\n".join(pesan))

            if jml_unit == 0:
                message.append("Belum ada Unit untuk Produk: %s" %(list_produk[int(no_produk) - 1]['name']))
                pesan= []
                pesan.append("Anda belum mengisi unit, silakan isi unit terlebih dahulu!")
                message.append("\n".join(pesan))

            save_redis.set("%s::menu" %(phone_number), json.dumps({"tagihan": "tambah_dua"}))

    elif json.loads(save_redis.get("%s::menu" %(phone_number)))['tagihan'] == 'tambah_dua':
        no_unit = re.findall(".+", incoming_msg)
        no_unit = regex_num(no_unit[0])
        if int(no_unit) > len(list_unit):
            message.append("Nomor Unit yang Anda masukkan tidak tersedia! Isi lagi yuk pakai Nomor Unit yang lain..")
            message.append("")
            message.append("Ketik *Tagihan* untuk kembali ke halaman sebelumnya")
            message.append("Ketik *Pengaturan* untuk kembali ke halaman Pengaturan")
            message.append("Ketik *Beranda* untuk kembali ke halaman Beranda")
        else:
            save_redis.set("%s::id_unit" %(phone_number), list_unit[int(no_unit) - 1]['id'])
            message.append("Sekarang Hedwig  tahu kapan *Mulai Waktu Tagihan*?")
            message.append("Tulisnya pakai format *(yyyy-mm-dd)* ya")
            
            save_redis.set("%s::menu" %(phone_number), json.dumps({"tagihan": "tambah_tiga"}))

    elif json.loads(save_redis.get("%s::menu" %(phone_number)))['tagihan'] == 'tambah_tiga':
        mulai_waktu = re.findall(".+", incoming_msg)
        mulai_waktu = mulai_waktu[0]
        message.append("Kalau *Selesai Waktu Tagihan* nya kapan?")
        message.append("Ini juga pakai format *(yyyy-mm-dd)* ya")
        save_redis.set("%s::mulai_waktu" %(phone_number), mulai_waktu)
        save_redis.set("%s::menu" %(phone_number), json.dumps({"tagihan": "tambah_empat"}))

    elif json.loads(save_redis.get("%s::menu" %(phone_number)))['tagihan'] == "tambah_empat":
        selesai_waktu = re.findall(".+", incoming_msg)
        selesai_waktu = selesai_waktu[0]
        unit_id = int(save_redis.get("%s::id_unit" %(phone_number)))
        if "aturtagihan" in app.config['URL']:
            unit_id = [unit_id]
            
        tambah = requests.post(app.config['URL']+"/billing/generate",
                               headers={"Authorization": "Bearer " +
                                        save_redis.get("%s::token" %(phone_number))},
                               json={
            "product_id": int(save_redis.get("%s::id_produk" %(phone_number))),
            "periode": save_redis.get("%s::mulai_waktu" %(phone_number)),
            "unit_id": unit_id,
            "start_date": save_redis.get("%s::mulai_waktu" %(phone_number)),
            "end_date": selesai_waktu
        })

        resp_tambah = tambah.json()

        if tambah.status_code != 200:
            message.append(resp_tambah["message"]["body"])
            message.append("Tagihan gagal dibuat! Anda harus aktivasi rekening Anda terlebih dahulu atau lengkapi informasi properti Anda!")
        else:
            for indeks in range(len(resp_tambah['data'])):
                if resp_tambah['data'][indeks]['unit_id'] == int(save_redis.get("%s::id_unit" %(phone_number))):
                    billing_id = resp_tambah['data'][indeks]['id']
                    print('BILLING ID', billing_id)
            link = requests.post(app.config['URL']+"/canopus/user_payment/" + str(billing_id),
                                 headers={"Authorization": "Bearer " + save_redis.get("%s::token" %(phone_number))}
                                )
            send_wa = requests.post(app.config['URL']+"/billing/send/wa",
                                    headers={"Authorization": "Bearer " + save_redis.get("%s::token" %(phone_number))},
                                    json={
                                        "billing_id":int(billing_id)
                                    }
                                   )
            respon_link = link.json()
            send_wa = send_wa.json()["data"]["wa_template"]
            send_wa = send_wa.replace(" ", "%20")
            if link.status_code == 200:
                message.append("Tagihan berhasil dibuat!")
                message.append("Klik tautan di bawah ini untuk mengirim Link Tagihan ke pelanggan Anda melalui whatsapp")
                message.append(send_wa)
                message.append("Atau kirim Link Tagihan berikut ini ke pelanggan Anda secara manual")
                message.append(respon_link['data'])
            else:
                message.append(respon_link["message"]["body"])
                message.append("Link Tagihan gagal dibuat! Anda harus melengkapi informasi tagihan di menu *Pengaturan* dan verifikasi rekening untuk mengaktifkan pembayaran digital!")

        pesan = []
        pesan.append("Ketik *Tagihan* untuk kembali ke halaman sebelumnya")
        pesan.append("Ketik *Pengaturan* untuk kembali ke halaman Pengaturan")
        pesan.append("Ketik *Beranda* untuk kembali ke halaman Beranda")
        message.append(("\n").join(pesan))
        save_redis.set("%s::menu" %(phone_number), 'tagihan')

    return message
