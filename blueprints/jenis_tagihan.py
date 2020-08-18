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

# Menu awal jenis tagihan
def jenis_tagihan(incoming_msg, phone_number, bot_responses):
    respon_jenis_tagihan = requests.post(app.config['URL']+"/billing_type/all", headers={"Authorization": "Bearer " + save_redis.get("%s::token" %(phone_number))})
    respon_jenis_tagihan = respon_jenis_tagihan.json()
    list_jenis_tagihan = respon_jenis_tagihan["data"]['records']
    message = []
    if "jenis_tagihan" in save_redis.get("%s::menu" %(phone_number)):
        if "tambah" in incoming_msg.lower():
            message = tambah_jenis_tagihan(incoming_msg, phone_number)
        elif "ubah" in incoming_msg.lower():
            no_jenis_tagihan = re.findall("ubah.+", incoming_msg.lower())
            no_jenis_tagihan = regex_num(no_jenis_tagihan[0])
            if int(no_jenis_tagihan) > len(list_jenis_tagihan):
                message.append("Nomor Jenis Tagihan yang Anda masukkan tidak tersedia!")
                message.append("")
                message.append("Silakan ketik *Jenis Tagihan* untuk kembali ke halaman sebelumnya")
            else:
                id_jenis_tagihan = respon_jenis_tagihan['data']['records'][int(no_jenis_tagihan)-1]['id']
                message = ubah_jenis_tagihan(incoming_msg, phone_number, id_jenis_tagihan)
        elif "hapus" in incoming_msg.lower():
            save_redis.set("%s::jenis_tagihan" %(phone_number), "hapus")
            message = hapus_jenis_tagihan(incoming_msg, phone_number)
        elif save_redis.get("%s::menu" %(phone_number)) == "jenis_tagihan":
            if respon_jenis_tagihan["data"]["count"] != 0:
                message_bubble = [bot_responses]
                all_bubble = []
                for index, billing in enumerate(list_jenis_tagihan):
                    tiap_data = []
                    tiap_data.append("%s. Nama: %s" %(index+1, billing['name']))
                    tiap_data.append("    Kategori: %s" %(billing['billing_category']))
                    tiap_data.append("    Produk: %s\n" %(billing['product_name']))
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

            else:
                message.append("Anda belum mengisi jenis tagihan!")
            
            pesan = []
            pesan.append("Silakan ketik menu berikut ini")
            pesan.append("- Ketik *tambah* untuk menambahkan Jenis Tagihan")
            pesan.append("- Ketik *ubah* <spasi> *no_jenis_tagihan* untuk mengubah Jenis Tagihan")
            pesan.append("- Ketik *hapus* <spasi> *no_jenis_tagihan* untuk menghapus Jenis Tagihan")
            pesan.append("")
            pesan.append("Ketik *Pengaturan* untuk kembali ke halaman Pengaturan")
            pesan.append("Ketik *Beranda* untuk kembali ke menu Beranda")
            message.append(("\n").join(pesan))

        else:
            read = json.loads(save_redis.get("%s::menu" %(phone_number)))
            if 'tambah' in read["jenis_tagihan"]:
                message = tambah_jenis_tagihan(incoming_msg, phone_number)
            elif 'ubah' in read["jenis_tagihan"]:
                message = ubah_jenis_tagihan(incoming_msg, phone_number, id=None)

    return message

def fungsi_tagihan(phone_number, incoming_msg):
    message = []
    
    respon_produk = requests.post(app.config['URL']+"/product/all", headers={"Authorization": "Bearer " + save_redis.get("%s::token" %(phone_number))})
    respon_produk = respon_produk.json()
    list_produk = respon_produk["data"]["records"]
    
    # user diminta memasukkan nama jenis tagihan
    # menyimpan no produk
    if save_redis.get("%s::jenis_tagihan"%(phone_number)) == "no_produk":
        incoming_msg = incoming_msg.strip()
        
        if int(incoming_msg) > len(list_produk):
            message.append("Nomor yang Anda masukkan tidak ada dalam daftar")
            message.append("Silakan masukkan lagi No Produk Anda")
        
        else:
            message.append("Silakan masukkan Nama Jenis tagihan Anda")
            save_redis.set("%s::no_produk" %(phone_number), list_produk[int(incoming_msg)-1]["id"])
            save_redis.set("%s::jenis_tagihan" %(phone_number), "nama")
            
    # user diminta memasukkan kategori tagihan
    # menyimpan nama tagihan
    elif save_redis.get("%s::jenis_tagihan"%(phone_number)) == "nama":
        incoming_msg = incoming_msg.strip()
        
        isi_tipe_tagihan = []
        isi_tipe_tagihan.append("1. IPL")
        isi_tipe_tagihan.append("2. Listrik")
        isi_tipe_tagihan.append("3. Air")
        message.append(("\n").join(isi_tipe_tagihan))
        
        save_redis.set("%s::nama" %(phone_number),incoming_msg)
        save_redis.set("%s::jenis_tagihan" %(phone_number),"kategori_tagihan")
        message.append("Silakan masukkan No Kategori yang ingin Anda tambahkan")
        
    # menyimpan kategori tagihan
    elif save_redis.get("%s::jenis_tagihan"%(phone_number)) == "kategori_tagihan":
        incoming_msg = incoming_msg.strip()
        
        if incoming_msg == "1":
            kategori = "ipl"
        elif incoming_msg == "2":
            kategori = "listrik"
        elif incoming_msg == "3":
            kategori = "air"
        
        if "tambah" in save_redis.get("%s::menu" %(phone_number)):
            tambah = requests.post(app.config['URL']+"/billing_type",
                                    headers={"Authorization": "Bearer " + save_redis.get("%s::token" %(phone_number))},
                                    json={
                                        "name": save_redis.get("%s::nama" %(phone_number)),
                                        "product_id": int(save_redis.get("%s::no_produk" %(phone_number))),
                                        "billing_category": kategori
                                    }
                                  )
            if tambah.status_code == 200:
                message.append("Jenis Tagihan berhasil ditambahkan")
            else:
                message.append("Jenis Tagihan gagal ditambahkan")
                message.append(tambah.json()["message"]["body"])
            
        elif "ubah" in save_redis.get("%s::menu" %(phone_number)):
            ubah = requests.put(app.config['URL']+"/billing_type/"+str(save_redis.get("%s::id_jenis_tagihan" %(phone_number))),
                                    headers={"Authorization": "Bearer " + save_redis.get("%s::token" %(phone_number))},
                                    json={
                                        "name": save_redis.get("%s::nama" %(phone_number)),
                                        "product_id": int(save_redis.get("%s::no_produk" %(phone_number))),
                                        "billing_category": kategori
                                    }
                                  )
            if ubah.status_code == 200:
                message.append("Jenis Tagihan berhasil diubah")
            else:
                message.append("Jenis Tagihan gagal diubah")
                message.append(ubah.json()["message"]["body"])
        
        pesan = []
        pesan.append("Ketik *Jenis Tagihan* untuk kembali ke halaman Jenis Tagihan")
        pesan.append("Ketik *Pengaturan* untuk kembali ke halaman Pengaturan")
        pesan.append("Ketik *Beranda* untuk kembali ke halaman Beranda")
        message.append(("\n").join(pesan))
        
        save_redis.set("%s::menu" %(phone_number), "jenis_tagihan")
        save_redis.delete("%s::jenis_tagihan" %(phone_number), "")
        save_redis.delete("%s::nama" %(phone_number), "")
        save_redis.delete("%s::no_produk" %(phone_number), "")
    
    return message

# Menu tambah jenis tagihan
def tambah_jenis_tagihan(incoming_msg,phone_number):
    message = []
    respon_produk = requests.post(app.config['URL']+"/product/all", headers={"Authorization": "Bearer " + save_redis.get("%s::token" %(phone_number))})
    respon_produk = respon_produk.json()
    if save_redis.get("%s::menu" %(phone_number)) == "jenis_tagihan":
        list_produk = respon_produk['data']['records']
        if respon_produk["data"]["count"] != 0:
            isi_produk = []
            for index, produk in enumerate(list_produk):
                isi_produk.append("%s. %s" % (index+1, produk['name']))
            message.append(("\n").join(isi_produk))

            message.append("Silakan masukkan Nomor Produk Anda")

            save_redis.set("%s::menu" %(phone_number),json.dumps({"jenis_tagihan": "tambah"}))
            save_redis.set("%s::jenis_tagihan"%(phone_number), "no_produk")

        else:
            message.append("Anda belum mengisi Produk, silakan isi produk terlebih dahulu!")
            send_message = ["Ketik *Jenis Tagihan* untuk ke menu Jenis Tagihan"]
            send_message.append("Ketik *Pengaturan* untuk ke menu Pengaturan")
            send_message.append("Ketik *Beranda* untuk ke menu Beranda")
            message.append(("\n").join(send_message))

    else:
        message = fungsi_tagihan(phone_number, incoming_msg)

    return message

# Menu ubah jenis tagihan
def ubah_jenis_tagihan(incoming_msg, phone_number, id):
    message = []
    respon_produk = requests.post(
        app.config['URL']+"/product/all", headers={"Authorization": "Bearer " + save_redis.get("%s::token" %(phone_number))})
    respon_produk = respon_produk.json()

    if id != None:
        respon_jenis_tagihan = requests.get(app.config['URL']+"/billing_type/" + str(id),
                                            headers={"Authorization": "Bearer " + save_redis.get("%s::token" %(phone_number))}
                                           )
        save_redis.set("%s::id_jenis_tagihan" %(phone_number), id)
        respon_jenis_tagihan = respon_jenis_tagihan.json()
        isi_jenis_tagihan = []
        isi_jenis_tagihan.append("Berikut inilah Jenis tagihan yang ingin Anda ubah:")
        isi_jenis_tagihan.append("Nama: %s" % (respon_jenis_tagihan['data']["name"]))
        isi_jenis_tagihan.append("Produk: %s" % (respon_jenis_tagihan['data']["product_name"]))
        isi_jenis_tagihan.append("Kategori: %s" % (respon_jenis_tagihan['data']['billing_category']))
        message.append(("\n").join(isi_jenis_tagihan))

        list_produk = respon_produk['data']['records']
        if respon_produk["data"]["count"] != 0:
            message_bubble = ["Berikut ini adalah Produk Anda: "]
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

            save_redis.set("%s::menu" %(phone_number),json.dumps({"jenis_tagihan": "ubah"}))
            save_redis.set("%s::jenis_tagihan"%(phone_number), "no_produk")

        else:
            message.append("Anda belum mengisi Produk, silakan isi produk terlebih dahulu!")
            send_message = ["Ketik *Jenis Tagihan* untuk ke menu Jenis Tagihan"]
            send_message.append("Ketik *Pengaturan* untuk ke menu Pengaturan")
            send_message.append("Ketik *Beranda* untuk ke menu Beranda")
            message.append(("\n").join(send_message))

    else:
        message += fungsi_tagihan(phone_number, incoming_msg)

    return message

# Menu hapus jenis tagihan
def hapus_jenis_tagihan(id, phone_number):
    message = []
    respon_jenis_tagihan = requests.post(app.config['URL']+"/billing_type/all", headers={"Authorization": "Bearer " + save_redis.get("%s::token" %(phone_number))})
    respon_jenis_tagihan = respon_jenis_tagihan.json()
    no_jenis_tagihan = re.findall("hapus.+", id.lower())
    no_jenis_tagihan = regex_num(no_jenis_tagihan[0])
    if int(no_jenis_tagihan) <= len(respon_jenis_tagihan['data']['records']):
        id_jenis_tagihan = respon_jenis_tagihan['data']['records'][int(no_jenis_tagihan)-1]['id']
        hapus = requests.delete(app.config['URL']+"/billing_type/" + str(id_jenis_tagihan),
                                headers={"Authorization": "Bearer " + save_redis.get("%s::token" %(phone_number))})
        if hapus.status_code == 200:
            message.append("Jenis Tagihan berhasil dihapus!")
        else:
            message.append("Jenis Tagihan gagal dihapus! ")

    else:
        message.append("Nomor Jenis Tagihan yang Anda masukkan salah")
        message.append("Silakan ulangi kembali")

    pesan = []
    pesan.append("Ketik *Jenis Tagihan* untuk kembali ke halaman Jenis Tagihan")
    pesan.append("Ketik *Pengaturan* untuk kembali ke halaman Pengaturan")
    pesan.append("Ketik *Beranda* untuk kembali ke halaman Beranda")
    message.append(("\n").join(pesan))

    return message