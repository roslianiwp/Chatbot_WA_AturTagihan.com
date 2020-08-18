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
from functions import formatrupiah

# Menu awal harga
def harga(incoming_msg, phone_number, bot_responses):
    respon_harga = requests.post(app.config['URL']+"/price/all",
                                 headers={"Authorization": "Bearer " + save_redis.get("%s::token"%(phone_number))}
                                 )
    respon_harga = respon_harga.json()
    list_harga = respon_harga["data"]['records']
    message = []

    if "harga" in save_redis.get("%s::menu"%(phone_number)):
        # ketika user BELUM mengetikkan "tambah"/"ubah"/"hapus"
        if "tambah" in incoming_msg.lower():
            message = tambah_harga(incoming_msg, phone_number)
        elif "ubah" in incoming_msg.lower():
            no_harga = re.findall("\d+", incoming_msg)
            no_harga = int(no_harga[0])
            # ketika nomor yang dimasukkan user ADA dalam daftar
            if no_harga <= len(list_harga):
                id_harga = list_harga[no_harga-1]['id']
                message = ubah_harga(incoming_msg, phone_number, id_harga)
            # nomor yang dimasukkan TIDAK ADA
            else:
                message.append("Nomor yang Anda masukkan tidak ada dalam daftar")
                message.append("Silakan masukkan lagi")

        elif "hapus" in incoming_msg.lower():
            no_harga = re.findall("\d+", incoming_msg)
            no_harga = int(no_harga[0])
            # ketika nomor yang dimasukkan user ADA dalam daftar
            if no_harga <= len(list_harga):
                id_harga = list_harga[no_harga-1]['id']
                message = hapus_harga(id_harga, phone_number)
            # nomor yang dimasukkan TIDAK ADA
            else:
                message.append("Nomor yang Anda masukkan tidak ada dalam daftar")
                message.append("Silakan masukkan lagi")

        # ketika user SUDAH mengetikkan "tambah"/"ubah"/"hapus"
        elif save_redis.get("%s::menu"%(phone_number)) == "harga":
            if respon_harga["data"]["count"] != 0:
                message_bubble = [bot_responses]
                all_bubble = []
                for index, harga in enumerate(list_harga):
                    tiap_data = []
                    tiap_data.append("%s. Produk: %s" %(index+1, harga['product_name']))
                    tiap_data.append("    Jenis Unit: %s" %(harga['unit_type_name']))
                    tiap_data.append("    Kategori Tagihan: %s" %(harga['billing_category']))
                    tiap_data.append("    Harga: %s" % (formatrupiah(harga['base_price'])))
                    tiap_data.append("")
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
                message.append("Anda belum mengisi Harga. Isi dulu yuk!")

            # INI NANTI FUNCTION SENDIRI YA!
            bubble = ["Apa yang ingin Anda lakukan?"]
            bubble.append("- Ketik *tambah* untuk menambahkan harga")
            bubble.append("- Ketik *ubah* <spasi> *no_harga* untuk mengubah harga")
            bubble.append("- Ketik *hapus* <spasi> *no_harga* untuk menghapus harga")
            message.append(("\n").join(bubble))
            
            bubble = ["Ketik *Pengaturan* untuk kembali ke menu Pengaturan"]
            bubble.append("Ketik *Beranda* untuk kembali ke menu Beranda")
            message.append(("\n").join(bubble))
            
            save_redis.delete("%s::no_produk"%(phone_number))
            save_redis.delete("%s::no_jenis_unit"%(phone_number))
            save_redis.delete("%s::kategori_tagihan"%(phone_number))
            save_redis.delete("%s::message"%(phone_number))
        else:
            if 'tambah' in json.loads(save_redis.get("%s::menu"%(phone_number)))['harga']:
                message = tambah_harga(incoming_msg, phone_number)
            elif 'ubah' in json.loads(save_redis.get("%s::menu"%(phone_number)))['harga']:
                message = ubah_harga(incoming_msg, phone_number)
    
    return message


def fungsi_harga(phone_number, incoming_msg):
    # data produk
    respon_produk = requests.post(app.config['URL']+"/product/all",
                                  headers={"Authorization": "Bearer " + save_redis.get("%s::token"%(phone_number))})
    respon_produk = respon_produk.json()
    list_produk = respon_produk['data']['records']

    # data jenis unit
    respon_jenis_unit = requests.post(app.config['URL']+"/unit_type/all",
                                      headers={"Authorization": "Bearer " + save_redis.get("%s::token"%(phone_number))})
    respon_jenis_unit = respon_jenis_unit.json()
    list_jenis_unit = respon_jenis_unit['data']['records']

    if "ubah" in incoming_msg:
        incoming_msg = incoming_msg.split()
        incoming_msg = incoming_msg[1]

    # ketika user memasukkan nomor produk
    if save_redis.get("%s::no_produk"%(phone_number)) is None:
        input_produk = incoming_msg.strip()
        message = []

        # menyimpan input produk ke session
        save_redis.set("%s::no_produk"%(phone_number), list_produk[int(input_produk)-1]['id'])

        # menampilkan data yang sudah dimasukkan
        send_message = ["Data yang sudah dimasukkan:"]
        nama_produk = list_produk[int(input_produk)-1]['name']
        send_message.append("Nama Produk: %s" %(nama_produk))
        save_redis.set("%s::message"%(phone_number), "Nama Produk: %s" %(nama_produk))
        message.append("\n".join(send_message))

        # mengambil data jenis unit berdasarkan produk yang dimasukkan
        send_message = ["Sekarang, silakan pilih nomor Jenis Unit Anda:"]
        for index, jenis_unit in enumerate(list_jenis_unit):
            if list_produk[int(input_produk)-1]['id'] == jenis_unit['product_id']:
                send_message.append("%s. %s" % (index+1, jenis_unit['name']))

        if len(send_message) > 1:
            message.append("\n".join(send_message))
        else:
            send_message = ["Belum ada Jenis Unit untuk Produk: %s" %(list_produk[int(input_produk)-1]['name'])]
            send_message.append("Masukkan Jenis Unit terlebih dahulu di Menu Jenis Unit")
            message.append(("\n").join(send_message))
            
            send_message = ["Ketik *Pengaturan* untuk ke menu Pengaturan"]
            send_message.append("Ketik *Beranda* untuk ke menu Beranda")
            message.append(("\n").join(send_message))

    # ketika user memasukkan nomor jenis unit
    elif save_redis.get("%s::no_jenis_unit"%(phone_number)) is None:
        input_jenis_unit = incoming_msg.strip()
        message = []

        # menyimpan input jenis unit ke session
        save_redis.set("%s::no_jenis_unit"%(phone_number), list_jenis_unit[int(input_jenis_unit)-1]['id'])

        # menampilkan data yang sudah dimasukkan
        send_message = ["Data yang sudah dimasukkan:"]
        send_message.append(save_redis.get("%s::message"%(phone_number)))
        send_message.append("Nama Jenis Unit: %s" %(list_jenis_unit[int(input_jenis_unit)-1]['name']))
        message.append("\n".join(send_message))
        save_redis.set("%s::message"%(phone_number), "\n".join(send_message))

        # menampilkan pilihan kategori tagihan
        send_message = ["Lalu, pilih Kategori Tagihan yang Anda inginkan:"]
        send_message.append("1. IPL")
        send_message.append("2. Listrik")
        send_message.append("3. Air")
        message.append("\n".join(send_message))

    # user memasukkan kategori tagihan
    elif save_redis.get("%s::kategori_tagihan"%(phone_number)) is None:
        message = []
        # menyimpan input kategori tagihan ke session
        input_kategori_tagihan = incoming_msg.strip()
        pilihan = ''
        if int(input_kategori_tagihan) == 1:
            pilihan = 'IPL'
            save_redis.set("%s::kategori_tagihan"%(phone_number), pilihan)
        elif int(input_kategori_tagihan) == 2:
            pilihan = 'Listrik'
            save_redis.set("%s::kategori_tagihan"%(phone_number), pilihan)
        elif int(input_kategori_tagihan) == 3:
            pilihan = 'Air'
            save_redis.set("%s::kategori_tagihan"%(phone_number), pilihan)

        # menampilkan data yang sudah dimasukkan
        send_message = []
        send_message.append(save_redis.get("%s::message"%(phone_number)))
        send_message.append("Kategori Tagihan: %s" % (pilihan))
        save_redis.set("%s::message"%(phone_number), "\n".join(send_message))
        message.append("\n".join(send_message))

        # meminta user memasukkan harga
        message.append("Selanjutnya, masukkan harga yang Anda inginkan")

    # user memasukkan harga
    else:
        input_harga = incoming_msg.strip()
        
        # cek apakah tambah
        if json.loads(save_redis.get("%s::menu"%(phone_number)))['harga'] == 'tambah':
            tambah = requests.post(app.config['URL']+"/price",
                                    headers={
                                       "Authorization": "Bearer " + save_redis.get("%s::token"%(phone_number))
                                    },
                                    json={
                                        "unit_type_id": int(save_redis.get("%s::no_jenis_unit"%(phone_number))),
                                        "billing_category": save_redis.get("%s::kategori_tagihan"%(phone_number)).lower(),
                                        "base_price": int(input_harga),
                                    })
            if tambah.status_code == 200:
                message = ["Harga berhasil ditambahkan!"]
            else:
                tambah = tambah.json()
                message = ["Harga gagal ditambahkan!"]
                message.append(tambah["message"]["body"])
            save_redis.set("%s::menu"%(phone_number), "harga")

        elif json.loads(save_redis.get("%s::menu"%(phone_number)))['harga'] == 'ubah':
            ubah = requests.put(app.config['URL']+"/price/" + str(save_redis.get("%s::id_harga"%(phone_number))),
                                headers={
                                    "Authorization": "Bearer " + save_redis.get("%s::token"%(phone_number))
                                },
                                json={
                                    "unit_type_id": int(save_redis.get("%s::no_jenis_unit"%(phone_number))),
                                    "billing_category": save_redis.get("%s::kategori_tagihan"%(phone_number)).lower(),
                                    "base_price": int(input_harga),
                                })
            if ubah.status_code == 200:
                message = ['Harga berhasil diubah']
            else:
                message = ['Harga gagal diubah']
                message.append(ubah.json()["message"]["body"])
            save_redis.set("%s::menu"%(phone_number), "harga")

        send_message = ["Ketik *Harga* untuk ke menu Harga"]
        send_message.append("Ketik *Pengaturan* untuk ke menu Pengaturan")
        send_message.append("Ketik *Beranda* untuk ke menu Beranda")
        message.append(("\n").join(send_message))
        
        save_redis.delete("%s::no_produk"%(phone_number))
        save_redis.delete("%s::no_jenis_unit"%(phone_number))
        save_redis.delete("%s::kategori_tagihan"%(phone_number))
        save_redis.delete("%s::message"%(phone_number))

    return message

def tambah_harga(incoming_msg, phone_number):
    message = []

    # data produk
    respon_produk = requests.post(app.config['URL']+"/product/all", headers={"Authorization": "Bearer " + save_redis.get("%s::token"%(phone_number))})
    respon_produk = respon_produk.json()
    list_produk = respon_produk['data']['records']

    if save_redis.get("%s::menu"%(phone_number)) == "harga":
        if respon_produk['data']['count'] != 0:
            message_bubble = ["Berikut ini adalah Daftar Produk milik Anda: "]
            all_bubble = []
            for index, produk in enumerate(list_produk):
                tiap_data = []
                tiap_data.append("%s. Produk: %s" % (index+1, produk['name']))
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
                
            message.append("Silakan masukkan nomor Produk yang Anda inginkan:")
            save_redis.set("%s::menu"%(phone_number), json.dumps({'harga': 'tambah'}))
        else:
            message.append("Anda belum mengisi Produk, silakan isi produk terlebih dahulu!")

    else:
        message = fungsi_harga(phone_number, incoming_msg)

    return message

def ubah_harga(incoming_msg, phone_number, id_harga=None):
    respon_produk = requests.post(app.config['URL']+"/product/all",
                                  headers={"Authorization": "Bearer " + save_redis.get("%s::token"%(phone_number))})
    respon_produk = respon_produk.json()
    list_produk = respon_produk['data']['records']
    message = []

    # user baru mengetikkan 'ubah <nomor>'
    if id_harga is not None:
        respon_harga = requests.get(app.config['URL']+"/price/" + str(id_harga),
                                    headers={"Authorization": "Bearer " + save_redis.get("%s::token"%(phone_number))})
        respon_harga = respon_harga.json()
        save_redis.set("%s::id_harga"%(phone_number), id_harga)
        send_message = ['Berikut ini Harga yang ingin Anda ubah:']
        send_message.append('Nama Produk: %s' %(respon_harga['data']['product_name']))
        send_message.append('Nama Jenis Unit: %s' %(respon_harga['data']['unit_type_name']))
        send_message.append('Kategori Tagihan: %s' %(respon_harga['data']['billing_category']))
        send_message.append('Harga: %s' % (formatrupiah(respon_harga['data']['base_price'])))
        send_message = "\n".join(send_message)
        message.append(send_message)
        send_message = ['Berikut Daftar Produk Anda:']
        for index, produk in enumerate(list_produk):
            send_message.append("%s. %s" % (index+1, produk['name']))
        send_message = "\n".join(send_message)
        message.append(send_message)
        message.append("Silakan pilih nomor Produk Anda")
        save_redis.set("%s::menu"%(phone_number), json.dumps({"harga": "ubah"}))
        
    else:
        respon_harga = requests.get(app.config['URL']+"/price/" + str(save_redis.get("%s::id_harga"%(phone_number))),
                                    headers={"Authorization": "Bearer " + save_redis.get("%s::token"%(phone_number))})
        respon_harga = respon_harga.json()

        if save_redis.get("%s::kategori_tagihan"%(phone_number)) is None or save_redis.get("%s::no_jenis_unit"%(phone_number)) is None or save_redis.get("%s::no_produk"%(phone_number)):
            send_message = ['Berikut ini Harga yang ingin Anda ubah:']
            send_message.append('Nama Produk: %s' %(respon_harga['data']['product_name']))
            send_message.append('Nama Jenis Unit: %s' %(respon_harga['data']['unit_type_name']))
            send_message.append('Kategori Tagihan: %s' %(respon_harga['data']['billing_category']))
            send_message.append('Harga: %s' %(formatrupiah(respon_harga['data']['base_price'])))
            send_message = "\n".join(send_message)
            message.append(send_message)
        
        message += fungsi_harga(phone_number, incoming_msg)

    return message

def hapus_harga(id_harga, phone_number):
    hapus = requests.delete(app.config['URL']+"/price/" + str(id_harga),
                            headers={"Authorization": "Bearer " + save_redis.get("%s::token"%(phone_number))})
    if hapus.status_code == 200:
        message = ['Harga berhasil dihapus']
    else:
        message = ['Harga gagal dihapus']
        message.append(hapus.json()["message"]["body"])

    send_message = ["Ketik *Harga* untuk ke menu Harga"]
    send_message.append("Ketik *Pengaturan* untuk ke menu Pengaturan")
    send_message.append("Ketik *Beranda* untuk ke menu Beranda")
    message.append(("\n").join(send_message))
    return message
