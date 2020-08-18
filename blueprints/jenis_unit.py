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

# Menu awal jenis unit
def jenis_unit(incoming_msg, phone_number, bot_responses):
    respon_jenis_unit = requests.post(app.config['URL']+"/unit_type/all", headers={"Authorization": "Bearer " + save_redis.get("%s::token" %(phone_number))})
    respon_jenis_unit = respon_jenis_unit.json()
    list_jenis_unit = respon_jenis_unit["data"]['records']
    message = []
    if "jenis_unit" in save_redis.get("%s::menu" %(phone_number)):
        if "tambah" in incoming_msg.lower():
            message = tambah_jenis_unit(incoming_msg, phone_number)
        elif "ubah" in incoming_msg.lower():
            incoming_msg = incoming_msg.lower()
            no_jenis_unit = re.findall("ubah.+", incoming_msg.lower())
            no_jenis_unit = regex_num(no_jenis_unit[0])
            if int(no_jenis_unit) > len(respon_jenis_unit['data']['records']):
                message.append("Nomor Jenis Unit yang Anda masukkan tidak tersedia!")
                message.append("")
                message.append("Silahkan ketik *Jenis Unit* untuk kembali ke halaman sebelumnya")
            else:
                id_jenis_produk = respon_jenis_unit['data']['records'][int(no_jenis_unit)-1]['id']
                message = ubah_jenis_unit(incoming_msg, phone_number, id_jenis_produk)
        elif "hapus" in incoming_msg.lower():
            message = hapus_jenis_unit(incoming_msg, phone_number)
        elif save_redis.get("%s::menu" %(phone_number)) == "jenis_unit":
            if respon_jenis_unit["data"]["count"] != 0:
                message_bubble = [bot_responses]
                all_bubble = []
                for index, item in enumerate(list_jenis_unit):
                    tiap_data = []
                    tiap_data.append("%s. Nama: %s" % (index+1, item['name']))
                    tiap_data.append("    Produk: %s" % (item['product_name']))
                    tiap_data.append("    Deskripsi: %s \n" %
                                     (item['description']))
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
                message.append("Anda belum mengisi jenis unit!")

            pesan = []
            pesan.append("Silahkan ketik menu berikut ini")
            pesan.append("- Ketik *tambah* untuk menambahkan Jenis Unit")
            pesan.append("- Ketik *ubah* <spasi> *no_jenis_unit* untuk mengubah Jenis Unit")
            pesan.append("- Ketik *hapus* <spasi> *no_jenis_unit* untuk menghapus Jenis Unit")
            pesan.append("")
            pesan.append("Ketik *Pengaturan* untuk kembali ke halaman Pengaturan")
            pesan.append("Ketik *Beranda* untuk kembali ke Menu")
            message.append(("\n").join(pesan))

        else:
            read = json.loads(save_redis.get("%s::menu" %(phone_number)))
            if 'tambah' in read["jenis_unit"]:
                message = tambah_jenis_unit(incoming_msg, phone_number)
            elif 'ubah' in read["jenis_unit"]:
                message = ubah_jenis_unit(incoming_msg, phone_number, id=None)

    return message

def fungsi_jenis_unit(phone_number, incoming_msg):
    message = []
    
    respon_produk = requests.post(app.config['URL']+"/product/all", headers={"Authorization": "Bearer " + save_redis.get("%s::token" %(phone_number))})
    respon_produk = respon_produk.json()
    list_produk = respon_produk["data"]["records"]
    
    # user diminta memasukkan nama jenis unit
    # menyimpan no produk
    if save_redis.get("%s::jenis_unit"%(phone_number)) == "no_produk":
        incoming_msg = incoming_msg.strip()
        
        if int(incoming_msg) > len(list_produk):
            message.append("Nomor yang Anda masukkan tidak ada dalam daftar")
            message.append("Silakan masukkan lagi No Produk Anda")
        
        else:
            message.append("Silakan masukkan Nama Jenis Unit Anda:")
            save_redis.set("%s::no_produk" %(phone_number), list_produk[int(incoming_msg)-1]["id"])
            save_redis.set("%s::jenis_unit" %(phone_number), "nama")
            
    # user diminta memasukkan deskripsi jenis unit
    # menyimpan nama jenis unit
    elif save_redis.get("%s::jenis_unit"%(phone_number)) == "nama":
        incoming_msg = incoming_msg.strip()
        save_redis.set("%s::nama_jenis_unit" %(phone_number),incoming_msg)
        message.append("Silakan masukkan Deskripsi Jenis Unit Anda:")
        save_redis.set("%s::jenis_unit" %(phone_number),"deskripsi")
    
    # menyimpan deskripsi jenis unit 
    elif save_redis.get("%s::jenis_unit"%(phone_number)) == "deskripsi":
        incoming_msg = incoming_msg.strip()
        
        if "tambah" in save_redis.get("%s::menu" %(phone_number)):
            tambah = requests.post(app.config['URL']+"/unit_type",
                                    headers={"Authorization": "Bearer " + save_redis.get("%s::token" %(phone_number))},
                                    json={
                                        "name": save_redis.get("%s::nama_jenis_unit" %(phone_number)),
                                        "description": incoming_msg,
                                        "product_id": int(save_redis.get("%s::no_produk" %(phone_number)))
                                    }
                                  )
            if tambah.status_code == 200:
                message.append("Jenis Unit berhasil ditambahkan")
            else:
                message.append("Jenis Unit gagal ditambahkan")
                message.append(tambah.json()["message"]["body"])
            
        elif "ubah" in save_redis.get("%s::menu" %(phone_number)):
            ubah = requests.put(app.config['URL']+"/unit_type/"+save_redis.get("%s::id_jenis_unit" %(phone_number)),
                                    headers={"Authorization": "Bearer " + save_redis.get("%s::token" %(phone_number))},
                                    json={
                                        "name": save_redis.get("%s::nama_jenis_unit" %(phone_number)),
                                        "description": incoming_msg,
                                        "product_id": int(save_redis.get("%s::no_produk" %(phone_number)))
                                    }
                                  )
            if ubah.status_code == 200:
                message.append("Jenis Unit berhasil diubah")
            else:
                message.append("Jenis Unit gagal diubah")
                message.append(ubah.json()["message"]["body"])
        
        pesan = []
        pesan.append("Ketik *Jenis Unit* untuk kembali ke halaman Jenis Unit")
        pesan.append("Ketik *Pengaturan* untuk kembali ke halaman Pengaturan")
        pesan.append("Ketik *Beranda* untuk kembali ke halaman Beranda")
        message.append(("\n").join(pesan))
        
        save_redis.set("%s::menu" %(phone_number), "jenis_unit")
        save_redis.delete("%s::nama_jenis_unit" %(phone_number), "")
        save_redis.delete("%s::no_produk" %(phone_number), "")
    
    return message

# Menu tambah jenis unit
def tambah_jenis_unit(incoming_msg, phone_number):
    message = []
    respon_produk = requests.post(app.config['URL']+"/product/all", headers={"Authorization": "Bearer " + save_redis.get("%s::token" %(phone_number))})
    respon_produk = respon_produk.json()
    if save_redis.get("%s::menu" %(phone_number)) == "jenis_unit":
        list_produk = respon_produk['data']['records']
        if respon_produk["data"]["count"] != 0:
            message_bubble = [""]
            all_bubble = []
            for index, produk in enumerate(list_produk):
                tiap_data = []
                tiap_data.append("%s. %s" % (index+1, produk['name']))
                tiap_data = ('\n').join(tiap_data)

                if len(message_bubble[0]) + len(tiap_data) >= 1600:
                    all_bubble.append(message_bubble)
                    message_bubble = ['']
                message_bubble.append(tiap_data)
                message_bubble = ('\n').join(message_bubble)
                message_bubble = [message_bubble]
                
            all_bubble.append(message_bubble)

            for bubble in all_bubble:
                message.append(bubble)

            message.append("Silakan masukkan Nomor Produk Anda")

            save_redis.set("%s::menu" %(phone_number),json.dumps({"jenis_unit": "tambah"}))
            save_redis.set("%s::jenis_unit"%(phone_number), "no_produk")
        else:
            message.append("Anda belum mengisi Produk, silakan isi produk terlebih dahulu!")
            send_message = ["Ketik *Jenis Unit* untuk ke menu Jenis Unit"]
            send_message.append("Ketik *Pengaturan* untuk ke menu Pengaturan")
            send_message.append("Ketik *Beranda* untuk ke menu Beranda")

    else:
        message = fungsi_jenis_unit(phone_number, incoming_msg)

    return message

# Menu ubah jenis unit
def ubah_jenis_unit(incoming_msg, phone_number, id):
    message = []
    respon_produk = requests.post(app.config['URL']+"/product/all", headers={"Authorization": "Bearer " + save_redis.get("%s::token" %(phone_number))})
    respon_produk = respon_produk.json()

    if id != None:
        respon_jenis_unit = requests.get(app.config['URL']+"/unit_type/" + str(id),
                                         headers={"Authorization": "Bearer " + save_redis.get("%s::token" %(phone_number))}
                                        )
        save_redis.set("%s::id_jenis_unit" %(phone_number),id)

        respon_jenis_unit = respon_jenis_unit.json()
        isi_jenis_unit = []
        isi_jenis_unit.append("Berikut inilah Jenis Unit yang ingin Anda ubah:")
        isi_jenis_unit.append("%s. Nama: %s" % (1, respon_jenis_unit['data']["name"]))
        isi_jenis_unit.append("    Produk: %s" % (respon_jenis_unit['data']['product_name']))
        isi_jenis_unit.append("    Deskripsi: %s\n" %(respon_jenis_unit['data']['description']))

        kirim_msg = ("\n").join(isi_jenis_unit)
        message.append(kirim_msg)

        list_produk = respon_produk['data']['records']
        if respon_produk["data"]["count"] != 0:
            message_bubble = ["Silahkan pilih nomor Produk Anda: "]
            all_bubble = []
            for index, produk in enumerate(list_produk):
                tiap_data = []
                tiap_data.append("%s. %s" % (index+1, produk['name']))
                tiap_data = ('\n').join(tiap_data)

                if len(message_bubble[0]) + len(tiap_data) >= 1600:
                    all_bubble.append(message_bubble)
                    message_bubble = ['']
                message_bubble.append(tiap_data)
                message_bubble = ('\n').join(message_bubble)
                message_bubble = [message_bubble]
                
            all_bubble.append(message_bubble)

            for bubble in all_bubble:
                message.append(bubble)

            message.append("Silakan masukkan Nomor Produk Anda")

            save_redis.set("%s::menu" %(phone_number),json.dumps({"jenis_unit": "ubah"}))
            save_redis.set("%s::jenis_unit"%(phone_number), "no_produk")

        else:
            message.append("Anda belum mengisi Produk, silakan isi produk terlebih dahulu!")
            send_message = ["Ketik *Jenis Unit* untuk ke menu Jenis Unit"]
            send_message.append("Ketik *Pengaturan* untuk ke menu Pengaturan")
            send_message.append("Ketik *Beranda* untuk ke menu Beranda")

    else:
        message += fungsi_jenis_unit(phone_number, incoming_msg)

    return message

# Menu hapus jenis unit
def hapus_jenis_unit(id, phone_number):
    message = []
    id = id.lower()
    respon_jenis_unit = requests.post(app.config['URL']+"/unit_type/all", headers={"Authorization": "Bearer " + save_redis.get("%s::token" %(phone_number))})
    respon_jenis_unit = respon_jenis_unit.json()
    no_jenis_unit = re.findall("hapus.+", id.lower())
    no_jenis_unit = regex_num(no_jenis_unit[0])
    
    if int(no_jenis_unit) <= len(respon_jenis_unit['data']['records']):
        id_jenis_produk = respon_jenis_unit['data']['records'][int(no_jenis_unit)-1]['id']
        hapus = requests.delete(app.config['URL']+"/unit_type/" + str(id_jenis_produk),
                                headers={"Authorization": "Bearer " + save_redis.get("%s::token" %(phone_number))})
        if hapus.status_code == 200:
            message.append("Jenis Unit berhasil dihapus")
        else:
            message.append("Jenis Unit gagal dihapus")
            message.append(hapus.json()["message"]["body"])
    else:
        message.append("Nomor Jenis Unit yang Anda masukkan salah")
        message.append("Silahkan ulangi kembali")

    pesan = []
    pesan.append("Ketik *Jenis Unit* untuk kembali ke halaman Jenis Unit")
    pesan.append("Ketik *Pengaturan* untuk kembali ke halaman Pengaturan")
    pesan.append("Ketik *Beranda* untuk kembali ke halaman Beranda")
    message.append(('\n').join(pesan))
    save_redis.set("%s::menu" %(phone_number), "jenis_unit")

    return message
