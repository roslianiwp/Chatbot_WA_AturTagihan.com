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

# Menu awal Pelanggan
def pelanggan(incoming_msg, phone_number, bot_responses):
    respon_pelanggan = requests.post(app.config['URL']+"/customer/all", headers={"Authorization": "Bearer " + save_redis.get("%s::token" %(phone_number))})
    respon_pelanggan = respon_pelanggan.json()
    list_pelanggan = respon_pelanggan["data"]['records']
    message = []
    if "pelanggan" in save_redis.get("%s::menu" %(phone_number)):
        if "tambah" in incoming_msg.lower():
            message = tambah_pelanggan(incoming_msg, phone_number)
        elif "ubah" in incoming_msg.lower():
            no_pelanggan = re.findall("ubah.+", incoming_msg.lower())
            no_pelanggan = regex_num(no_pelanggan[0])
            
            if int(no_pelanggan) > len(list_pelanggan):
                message.append("Nomor Pelanggan yang " + save_redis.get("%s::name" %(phone_number)) +" masukkan tidak tersedia!")
                message.append("")
                message.append("Ketik *Pelanggan* untuk kembali ke halaman sebelumnya")
            else:
                id_pelanggan = respon_pelanggan['data']['records'][int(no_pelanggan)-1]['id']
                message = ubah_pelanggan(incoming_msg, phone_number,id_pelanggan)
        elif "hapus" in incoming_msg.lower():
            save_redis.set("%s::menu" %(phone_number), json.dumps({"pelanggan":"hapus"}))
            message = hapus_pelanggan(incoming_msg, phone_number)

        elif save_redis.get("%s::menu" %(phone_number)) == "pelanggan":
            if respon_pelanggan["data"]["count"] != 0:
                message_bubble = [bot_responses]
                all_bubble = []
                for index, item in enumerate(list_pelanggan):
                    tiap_data = []
                    tiap_data.append("%s. Nama: %s" % (index+1, item['name']))
                    tiap_data.append("    Email: %s" %(item['email']))
                    tiap_data.append("    No Telepon: %s" % (item['phone']))
                    tiap_data.append("    KTP: %s" % (item['ktp']))
                    tiap_data.append("    Produk: %s\n" % (item['product_name']))
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
                message.append("Anda belum mengisi Pelanggan!")

            pesan = []
            message.append("Apa yang bisa Hedwig bantu?")
            pesan.append("- Ketik *tambah* untuk menambahkan Pelanggan")
            pesan.append("- Ketik *ubah* <spasi> *no_pelanggan* untuk mengubah Pelanggan")
            pesan.append("- Ketik *hapus* <spasi> *no_pelanggan* untuk menghapus Pelanggan")
            pesan.append("")
            pesan.append("Ketik *Pengaturan* untuk kembali ke halaman Pengaturan")
            pesan.append("Ketik *Beranda* untuk kembali ke halaman Beranda")
            message.append(("\n").join(pesan))
            
            save_redis.delete("%s::nama" %(phone_number), "")
            save_redis.delete("%s::email" %(phone_number), "")
            save_redis.delete("%s::telepon" %(phone_number), "")
            save_redis.delete("%s::ktp" %(phone_number), "")
            save_redis.delete("%s::pelanggan" %(phone_number), "")

        else:
            read = json.loads(save_redis.get("%s::menu" %(phone_number)))
            if 'tambah' in read['pelanggan']:
                message = tambah_pelanggan(incoming_msg, phone_number)
            elif 'ubah' in read['pelanggan']:
                message = ubah_pelanggan(incoming_msg, phone_number,id=None)
            
    return message

def fungsi_pelanggan(phone_number, incoming_msg):
    message = []
    
    # user diminta memasukkan email pelanggan
    # menyimpan data nama
    if save_redis.get("%s::pelanggan" %(phone_number)) == "nama":
        incoming_msg = incoming_msg.strip()
        save_redis.set("%s::pelanggan" %(phone_number), "email")
        save_redis.set("%s::nama" %(phone_number), incoming_msg)
        message.append("Kedua, masukkan Email Pelanggan terlebih dahulu" )
        
    # user diminta memasukkan no telepon
    # menyimpan data email
    elif save_redis.get("%s::pelanggan" %(phone_number)) == "email":
        incoming_msg = incoming_msg.strip()
        incoming_msg_regex = re.findall("^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$", incoming_msg)
        
        # format email benar
        if incoming_msg_regex != []:
            save_redis.set("%s::email" %(phone_number), incoming_msg_regex[0])
            save_redis.set("%s::pelanggan" %(phone_number), "telepon")
            message.append("Ketiga, masukkan Nomor Telepon Pelanggan")
            message.append("Contoh: 081339222111")
        
        # format email salah
        else:
            message.append("Email yang Anda masukkan tidak sesuai format email")
            message.append("Silakan masukkan kembali Email Anda")
            
    # user diminta memasukkan KTP pelanggan
    # menyimpan data telepon
    elif save_redis.get("%s::pelanggan" %(phone_number)) == "telepon":
        incoming_msg = incoming_msg.strip()
        incoming_msg_regex = re.findall("\+?([ -]?\d+)+|\(\d+\)([ -]\d+)", incoming_msg)
        
        if incoming_msg_regex != []:
            save_redis.set("%s::telepon" %(phone_number), incoming_msg)
            save_redis.set("%s::pelanggan" %(phone_number), "ktp")
            message.append("Keempat, masukkan No KTP pelanggan Anda")
        
        else:
            message.append("Nomor Telepon yang Anda masukkan tidak sesuai")
            message.append("Silakan masukkan kembali Nomor Telepon pelanggan Anda")
        
    # user diminta memasukkan no produk
    # menyimpan data ktp
    elif save_redis.get("%s::pelanggan" %(phone_number)) == "ktp":
        incoming_msg = incoming_msg.strip()
        
        respon_produk = requests.post(app.config['URL']+"/product/all",
                                    headers={"Authorization": "Bearer " + save_redis.get("%s::token"%(phone_number))}
                                    )
        respon_produk = respon_produk.json()
        list_produk = respon_produk['data']['records']
        
        if len(incoming_msg) == 16:
            save_redis.set("%s::ktp" %(phone_number), incoming_msg)
            save_redis.set("%s::pelanggan" %(phone_number), "no_produk")
            
            send_message = ['Berikut Daftar Produk Anda:']
            for index, produk in enumerate(list_produk):
                send_message.append("%s. %s" % (index+1, produk['name']))
            message.append(("\n").join(send_message))
            message.append("Terakhir, masukkan No Produk yang dihuni oleh Pelanggan Anda")
            
        else:
            message.append("No KTP yang Anda masukkan harus 16 digit")
            message.append("Silakan masukkan lagi No KTP pelanggan Anda lagi")
            
    # menyimpan no produk
    elif save_redis.get("%s::pelanggan" %(phone_number)) == "no_produk":
        incoming_msg = incoming_msg.strip()
        
        respon_produk = requests.post(app.config['URL']+"/product/all",
                                    headers={"Authorization": "Bearer " + save_redis.get("%s::token"%(phone_number))}
                                    )
        respon_produk = respon_produk.json()
        list_produk = respon_produk['data']['records']
        
        if int(incoming_msg) > len(list_produk):
            message.append("Nomor yang Anda masukkan tidak ada dalam daftar")
            message.append("Silakan masukkan lagi No Produk Anda")
        else:
            # ketika tambah pelanggan
            if "tambah" in save_redis.get("%s::menu" %(phone_number)):
                tambah = requests.post(app.config['URL']+"/customer",
                    headers={"Authorization": "Bearer "+ save_redis.get("%s::token" %(phone_number))},
                    json={
                        "name": save_redis.get("%s::nama" %(phone_number)),
                        "email": save_redis.get("%s::email" %(phone_number)),
                        "phone": save_redis.get("%s::telepon" %(phone_number)),
                        "ktp": save_redis.get("%s::ktp" %(phone_number)),
                        "product_id": list_produk[int(incoming_msg)-1]['id']
                    })
                
                if tambah.status_code == 200:
                    message.append("Pelanggan Anda berhasil ditambahkan!")
                else:
                    message.append("Pelanggan gagal ditambahkan!")
                    message.append(tambah.json()["message"]["body"])
            
            # ketika ubah pelanggan
            if "ubah" in save_redis.get("%s::menu" %(phone_number)):
                ubah = requests.put(app.config['URL']+"/customer/"+str(save_redis.get("%s::id_pelanggan" %(phone_number))),
                    headers={"Authorization": "Bearer "+ save_redis.get("%s::token" %(phone_number))},
                    json={
                        "name": save_redis.get("%s::nama" %(phone_number)),
                        "email": save_redis.get("%s::email" %(phone_number)),
                        "phone": save_redis.get("%s::telepon" %(phone_number)),
                        "ktp": save_redis.get("%s::ktp" %(phone_number)),
                        "product_id": list_produk[int(incoming_msg)-1]['id']
                    })
                
                if ubah.status_code == 200:
                    message.append("Pelanggan berhasil diubah")
                else:
                    message.append("Pelanggan gagal diubah")
                    message.append(ubah.json()["message"]["body"])

            pesan = []
            pesan.append("Ketik *Pelanggan* untuk kembali ke halaman Pelanggan")
            pesan.append("Ketik *Pengaturan* untuk kembali ke halaman Pengaturan")
            pesan.append("Ketik *Beranda* untuk kembali ke halaman Beranda")
            message.append(("\n").join(pesan)) 
                
            save_redis.set("%s::menu" %(phone_number), "pelanggan")
            save_redis.delete("%s::nama" %(phone_number), "")
            save_redis.delete("%s::email" %(phone_number), "")
            save_redis.delete("%s::telepon" %(phone_number), "")
            save_redis.delete("%s::ktp" %(phone_number), "")
            save_redis.delete("%s::pelanggan" %(phone_number), "")
                
    return message

# Menu tambah pelanggan
def tambah_pelanggan(incoming_msg,phone_number):
    message = []
    respon_produk = requests.post(app.config['URL']+"/product/all",
                                    headers={"Authorization": "Bearer " + save_redis.get("%s::token"%(phone_number))}
                                 )
    respon_produk = respon_produk.json()
    list_produk = respon_produk['data']['records']
    
    if len(list_produk) == 0:
        message.append("Anda belum mengisi Produk, silakan isi produk terlebih dahulu!")
        message.append("Ketik *Pengaturan* untuk ke menu Pengaturan")
    
    elif save_redis.get("%s::menu" %(phone_number)) == "pelanggan":
        message.append("Pertama, masukkan Nama Lengkap Pelanggan Anda")
        save_redis.set("%s::menu" %(phone_number), json.dumps({"pelanggan":"tambah"}))
        save_redis.set("%s::pelanggan"%(phone_number), "nama")

    else:
        message = fungsi_pelanggan(phone_number, incoming_msg)

    return message

# # Menu ubah produk
def ubah_pelanggan(incoming_msg, phone_number, id):
    message = []
    respon_produk = requests.post(app.config['URL']+"/product/all", headers={"Authorization": "Bearer "+ save_redis.get("%s::token" %(phone_number))})
    respon_produk = respon_produk.json()
    list_produk = respon_produk['data']['records']

    # user baru mengetikkan id
    if id != None:
        respon_pelanggan = requests.get(app.config['URL']+"/customer/"+ str(id), headers={"Authorization": "Bearer "+ save_redis.get("%s::token" %(phone_number))})
        save_redis.set("%s::id_pelanggan" %(phone_number),id)
        respon_pelanggan = respon_pelanggan.json()
        keterangan_produk = []
        keterangan_produk.append("Berikut inilah Pelanggan yang ingin Anda ubah:")
        keterangan_produk.append("%s. Nama: %s" % (1, respon_pelanggan['data']['name']))
        keterangan_produk.append("    Email: %s" % (respon_pelanggan['data']['email']))
        keterangan_produk.append("    No Telepon: %s" % (respon_pelanggan['data']['phone']))
        keterangan_produk.append("    KTP: %s" % (respon_pelanggan['data']['ktp']))
        keterangan_produk.append("    Produk: %s" % (respon_pelanggan['data']['product_name']))
        message.append(('\n').join(keterangan_produk))

        message.append("Pertama, masukkan Nama Lengkap Pelanggan Anda")
        save_redis.set("%s::pelanggan"%(phone_number), "nama")
        save_redis.set("%s::menu" %(phone_number), json.dumps({"pelanggan":"ubah"}))
    else:
        respon_pelanggan = requests.get(app.config['URL']+"/customer/"+ str(save_redis.get("%s::id_pelanggan" %(phone_number))), headers={"Authorization": "Bearer "+ save_redis.get("%s::token" %(phone_number))})
        message += fungsi_pelanggan(phone_number, incoming_msg)

    return message

# Menu hapus Pelanggan
def hapus_pelanggan(id, phone_number):
    message = []
    respon_pelanggan = requests.post(app.config['URL']+"/customer/all", headers={"Authorization": "Bearer "+ save_redis.get("%s::token" %(phone_number))})
    respon_pelanggan = respon_pelanggan.json()
    no_pelanggan = re.findall("hapus.+", id.lower())
    no_pelanggan = regex_num(no_pelanggan[0])
    if int(no_pelanggan) <= len(respon_pelanggan['data']['records']):
        id_pelanggan = respon_pelanggan['data']['records'][int(no_pelanggan)-1]['id']
        hapus = requests.delete(app.config['URL']+"/customer/" + str(id_pelanggan), headers={"Authorization": "Bearer "+ save_redis.get("%s::token" %(phone_number))})
        if hapus.status_code == 200:
            message.append("Pelanggan berhasil dihapus!")
        else:
            message.append("Pelanggan gagal dihapus! ")
    else:
        message.append("Nomor Pelanggan yang Anda masukkan salah")
        message.append("Silahkan ulangi kembali")

    pesan = []
    pesan.append("Ketik *Pelanggan* untuk kembali ke halaman Pelanggan")
    pesan.append("Ketik *Pengaturan* untuk kembali ke halaman Pengaturan")
    pesan.append("Ketik *Beranda* untuk kembali ke halaman Beranda")
    message.append(("\n").join(pesan))
    save_redis.set("%s::menu" %(phone_number), "pelanggan")

    return message

