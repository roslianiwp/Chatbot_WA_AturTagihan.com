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
def produk(incoming_msg, phone_number, bot_responses):
    respon_produk = requests.post(app.config['URL']+"/product/all", headers={"Authorization": "Bearer " + save_redis.get("%s::token" %(phone_number))})
    respon_produk = respon_produk.json()
    list_produk = respon_produk["data"]['records']
    message = []
    if 'produk' in save_redis.get("%s::menu" %(phone_number)):
        if "tambah" in incoming_msg.lower():
            message = tambah_produk(incoming_msg, phone_number)
        elif "ubah" in incoming_msg.lower():
            no_produk = re.findall("ubah.+", incoming_msg.lower())
            no_produk = regex_num(no_produk[0])
            if int(no_produk) > len(respon_produk['data']['records']):
                message.append("Nomor Produk yang Anda masukkan tidak tersedia!")
                message.append("")
                message.append("Silakan ketik *Produk* untuk kembali ke halaman sebelumnya")
            else:
                id_produk = respon_produk['data']['records'][int(no_produk)-1]['id']
                message = ubah_produk(incoming_msg, phone_number,id_produk)

        elif "hapus" in incoming_msg.lower():
            save_redis.set("%s::produk" %(phone_number), "hapus")
            message = hapus_produk(incoming_msg, phone_number)

        elif (save_redis.get("%s::menu" %(phone_number))) == "produk":
            if respon_produk["data"]["count"] != 0:
                message_bubble = [bot_responses]
                all_bubble = []
                for index, item in enumerate(list_produk):
                    tiap_data = []
                    tiap_data.append("%s. Nama: %s" % (index+1, item['name']))
                    tiap_data.append("    Jenis Produk: %s" %
                                (item['product_type_name']))
                    tiap_data.append("    Alamat: %s" % (item['description']))
                    tiap_data.append("    Bank: %s %s a.n %s \n" % (
                        item['bank_name'], item['account_number'], item['account_name']))
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

            pesan = ["Apa yang bisa Hedwig bantu?"]
            pesan.append("- Ketik *tambah* untuk menambahkan Produk")
            pesan.append("- Ketik *ubah* <spasi> *no_produk* untuk mengubah Produk")
            pesan.append("- Ketik *hapus* <spasi> *no_produk* untuk menghapus Produk")
            pesan.append("")
            pesan.append("Ketik *Pengaturan* untuk kembali ke halaman Pengaturan")
            pesan.append("Ketik *Beranda* untuk kembali ke Menu")
            message.append(("\n").join(pesan))
        else:
            read = json.loads(save_redis.get("%s::menu" %(phone_number)))
            if 'tambah' in read["produk"]:
                message = tambah_produk(incoming_msg, phone_number)
            elif 'ubah' in read["produk"]:
                message = ubah_produk(incoming_msg, phone_number, id=None)
            
    return message

def fungsi_produk(phone_number, incoming_msg):
    message = []
    
    # user diminta memasukkan jenis produk
    # menyimpan data nama produk
    if save_redis.get("%s::produk" %(phone_number)) == "nama":
        incoming_msg = incoming_msg.strip()
        isi_produk = []
        if "aturtagihan" in app.config['URL']:
            list_tipe_produk = requests.post(app.config['URL']+"/product_type/all", headers={"Authorization": "Bearer " + save_redis.get("%s::token" %(phone_number))})
            list_tipe_produk = list_tipe_produk.json()
            list_tipe_produk = list_tipe_produk["data"]["records"]
            for index, tipe_produk in enumerate(list_tipe_produk):
                isi_produk.append("%s. %s"%(index+1, tipe_produk["name"]))
        else:
            isi_produk.append("Sekarang, pilih nomor Jenis Produk untuk menambahkan data Produk Anda: ")
            isi_produk.append("1. Apartemen") # no id 1
            isi_produk.append("2. Perumahan") # no id 2
            isi_produk.append("3. Kos\n") # no id 108
        kirim_msg = ("\n").join(isi_produk)
        message.append(kirim_msg)
        message.append("Jenis produk berapakah yang Anda inginkan?")
        save_redis.set("%s::nama" %(phone_number), incoming_msg)
        save_redis.set("%s::produk" %(phone_number), "jenis_produk")
    
    # user diminta memasukkan alamat produk
    # menyimpan data jenis produk
    elif save_redis.get("%s::produk" %(phone_number)) == "jenis_produk":
        incoming_msg = incoming_msg.strip()
        if "aturtagihan" in app.config['URL']:
            save_redis.set("%s::no_tipe_produk" %(phone_number), int(incoming_msg))
        else:
            if int(incoming_msg) == 3:
                save_redis.set("%s::no_tipe_produk" %(phone_number), 108)
            else:
                save_redis.set("%s::no_tipe_produk" %(phone_number), int(incoming_msg))
        message.append("Lalu, ketik Alamat dari Produk Anda")
        save_redis.set("%s::produk" %(phone_number), "alamat")
        
    # user diminta memasukkan tanggal cetak invoice
    # menyimpan data alamat
    elif save_redis.get("%s::produk" %(phone_number)) == "alamat":
        incoming_msg = incoming_msg.strip()
        save_redis.set("%s::alamat" %(phone_number), incoming_msg)
        message.append("Selanjutnya, setiap tanggal berapa Cetak Invoice Produk akan dilakukan?")
        message.append("(contoh: 1 atau 30)")
        save_redis.set("%s::produk" %(phone_number), "tgl_cetak")
        
    # user diminta memasukkan tgl jatuh tempo
    # menyimpan data tgl cetak
    elif save_redis.get("%s::produk" %(phone_number)) == "tgl_cetak":
        incoming_msg = incoming_msg.strip()
        save_redis.set("%s::cetak_invoice" %(phone_number), incoming_msg)
        message.append("Kalau tanggal Jatuh Tempo Produknya setiap tanggal berapa?")
        message.append("(contoh: 1 atau 30)")
        save_redis.set("%s::produk" %(phone_number), "tgl_jatuh_tempo")
    
    # user diminta memasukkan bank
    # menyimpan tgl jatuh tempo
    elif save_redis.get("%s::produk" %(phone_number)) == "tgl_jatuh_tempo":
        incoming_msg = incoming_msg.strip()
        save_redis.set("%s::tempo_invoice" %(phone_number), incoming_msg)
        message.append("Sekarang, ketik Nama Bank dari Produk Anda")
        message.append("(contoh: Bank Mandiri atau Bank Niaga)")
        save_redis.set("%s::produk" %(phone_number), "bank")
        
    # user diminta memasukkan nomor rekening
    # menyimpan bank
    elif save_redis.get("%s::produk" %(phone_number)) == "bank":
        incoming_msg = incoming_msg.strip()
        message.append("Baik, Anda menggunakan %s" %(incoming_msg))
        message.append("Selanjutnya, berapa Nomor Rekening Bank dari bank Anda?")
        message.append("(contoh: 99123248113)")
        save_redis.set("%s::produk" %(phone_number), "nomor_rekening")
        
        respon_bank_dropdown = requests.get(app.config['URL']+"/bank/dropdown",
                                            headers={"Authorization": "Bearer "+ save_redis.get("%s::token" %(phone_number))}
                                            )
        respon_bank_dropdown = respon_bank_dropdown.json()
        for bank in respon_bank_dropdown["data"]:
            if incoming_msg.upper() in bank['name']:
                bank_code = bank['code']
                save_redis.set("%s::bank_code" %(phone_number), bank_code)
                break
    
    # user diminta memasukkan nama pemilik rekening
    # menyimpan nomor rekening
    elif save_redis.get("%s::produk" %(phone_number)) == "nomor_rekening":
        incoming_msg = incoming_msg.strip()
        save_redis.set("%s::nomor_rekening" %(phone_number), incoming_msg)
        message.append("Kalau Nama Pemilik Rekening dari Rekening tersebut siapa?")
        message.append("(contoh: Rizki Pangestu)")
        save_redis.set("%s::produk" %(phone_number), "nama_rekening")
    
    # menyimpan pemilik rekening
    elif save_redis.get("%s::produk" %(phone_number)) == "nama_rekening":
        incoming_msg = incoming_msg.strip()

        if "tambah" in save_redis.get("%s::menu" %(phone_number)):
            tambah = requests.post(app.config['URL']+"/product",
                headers={"Authorization": "Bearer "+ save_redis.get("%s::token" %(phone_number))},
                json={
                    "name":save_redis.get("%s::nama" %(phone_number)),
                    "product_type_id": int(save_redis.get("%s::no_tipe_produk" %(phone_number))),
                    "description": save_redis.get("%s::alamat" %(phone_number)),
                    "start_date": int(save_redis.get("%s::cetak_invoice" %(phone_number))),
                    "end_date": int(save_redis.get("%s::tempo_invoice" %(phone_number))),
                    "bank_code": save_redis.get("%s::bank_code" %(phone_number)),
                    "account_number": save_redis.get("%s::nomor_rekening" %(phone_number)),
                    "account_name": incoming_msg
                })
            if tambah.status_code == 200:
                    message.append("Produk berhasil ditambahkan!")
            else:
                message.append("Produk gagal ditambahkan!")
                message.append(tambah.json()["message"]["body"])
            
        elif "ubah" in save_redis.get("%s::menu" %(phone_number)):
            ubah = requests.put(app.config['URL']+"/product/"+save_redis.get("%s::id_produk" %(phone_number)),
                headers={"Authorization": "Bearer "+ save_redis.get("%s::token" %(phone_number))},
                json={
                    "name":save_redis.get("%s::nama" %(phone_number)),
                    "product_type_id": int(save_redis.get("%s::no_tipe_produk" %(phone_number))),
                    "description": save_redis.get("%s::alamat" %(phone_number)),
                    "start_date": int(save_redis.get("%s::cetak_invoice" %(phone_number))),
                    "end_date": int(save_redis.get("%s::tempo_invoice" %(phone_number))),
                    "bank_code": save_redis.get("%s::bank_code" %(phone_number)),
                    "account_number": save_redis.get("%s::nomor_rekening" %(phone_number)),
                    "account_name": incoming_msg
                })
            if ubah.status_code == 200:
                    message.append("Produk berhasil diubah")
            else:
                message.append("Produk gagal diubah")
                message.append(ubah.json()["message"]["body"])
                
        pesan = []
        pesan.append("Ketik *Produk* untuk kembali ke halaman Produk")
        pesan.append("Ketik *Pengaturan* untuk kembali ke halaman Pengaturan")
        pesan.append("Ketik *Beranda* untuk kembali ke halaman Beranda")
        message.append(("\n").join(pesan))
        
        save_redis.set("%s::menu" %(phone_number), "produk")
        save_redis.delete("%s::nama" %(phone_number), "")
        save_redis.delete("%s::no_tipe_produk" %(phone_number), "")
        save_redis.delete("%s::cetak_invoice" %(phone_number), "")
        save_redis.delete("%s::tempo_invoice" %(phone_number), "")
        save_redis.delete("%s::bank_code" %(phone_number), "")
        save_redis.delete("%s::nomor_rekening" %(phone_number), "")
        
    return message
    
# Menu tambah produk
def tambah_produk(incoming_msg, phone_number):
    message = []
    if save_redis.get("%s::menu" %(phone_number)) == "produk":
        message.append("Pertama, silakan masukkan Nama Produk Anda")
        save_redis.set("%s::menu" %(phone_number), json.dumps({"produk":"tambah"}))
        save_redis.set("%s::produk"%(phone_number), "nama")
    else:
        message = fungsi_produk(phone_number, incoming_msg)
        
    return message

# # Menu ubah produk
def ubah_produk(incoming_msg, phone_number, id):
    message = []

    if id != None:
        respon_produk = requests.get(app.config['URL']+"/product/"+ str(id), headers={"Authorization": "Bearer " + save_redis.get("%s::token" %(phone_number))})
        save_redis.set("%s::id_produk" %(phone_number), id)
        respon_produk = respon_produk.json()
        isi_produk = []

        isi_produk.append("Berikut inilah Produk yang ingin Anda ubah:")

        isi_produk.append("%s. Nama: %s" % (1, respon_produk['data']["name"]))
        isi_produk.append("    Jenis Produk: %s" % (respon_produk['data']['product_type_name']))
        isi_produk.append("    Alamat: %s" % (respon_produk['data']['description']))
        isi_produk.append("    Bank: %s %s a.n %s \n" % (respon_produk['data']['bank_name'], respon_produk['data']['account_number'], respon_produk['data']['account_name']))

        kirim_msg = ("\n").join(isi_produk)
        message.append(kirim_msg)

        message.append("Silakan masukkan Nama Produk Anda")
        save_redis.set("%s::menu" %(phone_number), json.dumps({"produk":"ubah"}))
        save_redis.set("%s::produk"%(phone_number), "nama")

    else:
        message += fungsi_produk(phone_number, incoming_msg)

    return message

# Menu hapus Produk
def hapus_produk(id, phone_number):
    message = []
    respon_produk = requests.post(app.config['URL']+"/product/all", headers={"Authorization": "Bearer "+ save_redis.get("%s::token" %(phone_number))})
    respon_produk = respon_produk.json()
    no_produk = re.findall("hapus.+", id.lower())
    no_produk = regex_num(no_produk[0])

    if int(no_produk) <= len(respon_produk['data']['records']):
        id_produk = respon_produk['data']['records'][int(no_produk)-1]['id']
        hapus = requests.delete(app.config['URL']+"/product/" + str(id_produk), headers={"Authorization": "Bearer "+ save_redis.get("%s::token" %(phone_number))})
        if hapus.status_code == 200:
            message.append("Produk berhasil dihapus!")
        else:
            message.append("Produk gagal dihapus! ")
        
    else:
        message.append("Nomor Jenis Unit yang Anda masukkan salah")
        message.append("Silakan ulangi kembali")

    message.append("")
    pesan = ["Ketik *Produk* untuk kembali ke halaman Produk"]
    pesan.append("Ketik *Pengaturan* untuk kembali ke halaman Pengaturan")
    pesan.append("Ketik *Beranda* untuk kembali ke halaman Beranda")
    message.append(('\n').join(pesan))
    save_redis.set("%s::menu" %(phone_number), "produk")

    return message
