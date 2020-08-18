import requests
import re
import json
import config
from blueprints import app
from blueprints import save_redis
from flask import Flask
from flask import request
from functions import regex
from functions import regex_num
from functions import formatrupiah

# Menu awal Formula
def formula(incoming_msg, phone_number, bot_responses):
    respon_formula = requests.post(app.config['URL']+"/formula/all",
                                   headers={"Authorization": "Bearer " + save_redis.get("%s::token"%(phone_number))}
                                   )
    respon_formula = respon_formula.json()
    list_formula = respon_formula["data"]['records']
    message = []
    if "formula" in save_redis.get("%s::menu"%(phone_number)):
        # ketika user BELUM mengetikkan "tambah"/"ubah"/"hapus"
        if "tambah" in incoming_msg.lower():
            message = tambah_formula(incoming_msg, phone_number)
        elif "ubah" in incoming_msg.lower():
            no_formula = re.findall("\d+", incoming_msg)
            no_formula = int(no_formula[0])
            # ketika nomor yang dimasukkan user ADA dalam list
            if no_formula <= len(list_formula):
                id_jenis_formula = list_formula[no_formula-1]['id']
                message = ubah_formula(incoming_msg, phone_number, id_jenis_formula)
                
            # ketika nomor yang dimasukkan TIDAK ADA
            else:
                message.append("Nomor yang Anda masukkan tidak ada dalam daftar")
                message.append("Silakan masukkan lagi")

        elif "hapus" in incoming_msg.lower():
            no_formula = re.findall("\d+", incoming_msg)
            no_formula = int(no_formula[0])
            # ketika nomor yang dimasukkan user ADA dalam list
            if no_formula <= len(list_formula):
                id_jenis_produk = list_formula[no_formula]['id']
                message = hapus_formula(id_jenis_produk, phone_number)
            # ketika nomor yang dimasukkan TIDAK ADA
            else:
                message.append("Nomor yang Anda masukkan tidak ada dalam daftar")
                message.append("Silakan masukkan lagi")

        # ketika user SUDAH mengetikkan "tambah"/"ubah"/"hapus"
        elif save_redis.get("%s::menu"%(phone_number)) == "formula":
            if respon_formula["data"]["count"] != 0:
                all_bubble = []
                message_bubble = [bot_responses]
                for index, formula in enumerate(list_formula):
                    tiap_data = []
                    tiap_data.append("%s. Produk: %s" %(index+1, formula['product_name']))
                    tiap_data.append("    Jenis Unit: %s" %(formula['unit_type_name']))
                    tiap_data.append("    Jenis Tagihan: %s" %(formula['billing_type_name']))
                    tiap_data.append("    Kategori Tagihan: %s" %(formula['billing_category']))
                    tiap_data.append("    Jenis Perhitungan: %s" %                                     (formula['charge_type']))
                    tiap_data.append("    Formula: %s" %(formula['formulation']))
                    tiap_data.append("    Harga Dasar: %s" %(formatrupiah(formula['base_price'])))
                    tiap_data.append("")
                    tiap_data = '\n'.join(tiap_data)
                    if len(message_bubble[0]) + len(tiap_data) >= 1600:
                        all_bubble.append(message_bubble)
                        message_bubble = ['']
                    message_bubble.append(tiap_data)
                    message_bubble = '\n'.join(message_bubble)
                    message_bubble = [message_bubble]
                all_bubble.append(message_bubble)
                
                for bubble in all_bubble:
                    message.append(bubble)
                    
            else:
                message.append("Anda belum mengisi Formula!")

            bubble = ["Apa yang bisa Hedwig bantu?"]
            bubble.append("Ketik *tambah* untuk menambahkan Formula")
            bubble.append("Ketik *ubah* <spasi> *no_formula* untuk mengubah Formula")
            bubble.append("Ketik *hapus* <spasi> *no_formula* untuk menghapus Formula")
            message.append(("\n").join(bubble))
            bubble = ["Ketik *pengaturan* untuk kembali ke menu Pengaturan"]
            bubble.append("Ketik *beranda* untuk kembali ke menu Beranda")
            message.append(("\n").join(bubble))
        else:
            if 'tambah' in json.loads(save_redis.get("%s::menu"%(phone_number)))['formula']:
                message = tambah_formula(incoming_msg, phone_number)
            elif 'ubah' in json.loads(save_redis.get("%s::menu"%(phone_number)))['formula']:
                message = ubah_formula(incoming_msg, phone_number)
    
    return message


def fungsi_formula(phone_number, incoming_msg):
    # data produk
    respon_produk = requests.post(app.config['URL']+"/product/all",
                                  headers={"Authorization": "Bearer " + save_redis.get("%s::token"%(phone_number))}
                                )
    respon_produk = respon_produk.json()
    list_produk = respon_produk['data']['records']

    # data jenis unit
    respon_jenis_unit = requests.post(app.config['URL']+"/unit_type/all",
                                      headers={"Authorization": "Bearer " + save_redis.get("%s::token"%(phone_number))}
                                    )
    respon_jenis_unit = respon_jenis_unit.json()
    list_jenis_unit = respon_jenis_unit['data']['records']

    # data jenis tagihan
    respon_jenis_tagihan = requests.post(app.config['URL']+"/billing_type/all",
                                         headers={"Authorization": "Bearer " + save_redis.get("%s::token"%(phone_number))}
                                        )
    respon_jenis_tagihan = respon_jenis_tagihan.json()
    list_jenis_tagihan = respon_jenis_tagihan['data']['records']

    # data harga
    respon_harga = requests.post(app.config['URL']+"/price/all",
                                    headers={"Authorization": "Bearer " + save_redis.get("%s::token"%(phone_number))}
                                )
    respon_harga = respon_harga.json()
    list_harga = respon_harga['data']['records']

    if "ubah" in incoming_msg:
        incoming_msg = incoming_msg.split()
        incoming_msg = incoming_msg[1]

    all_bubble = []
    message = []
    # Produk TERSIMPAN, memasukkan Jenis Unit
    if save_redis.get("%s::no_produk"%(phone_number)) is None:
        # menyimpan input produk ke session
        produk = incoming_msg.strip()
        save_redis.set("%s::no_produk"%(phone_number), int(produk))

        # menampilkan data yang sudah dimasukkan
        send_message = ["Data yang sudah dimasukkan:"]
        send_message.append("Produk: %s" %(list_produk[int(produk) - 1]['name']))
        save_redis.set("%s::message"%(phone_number), ("\n").join(send_message))
        all_bubble.append("\n".join(send_message))

        # mengambil data jenis unit berdasarkan produk yang dipilih
        send_message = ["Silakan pilih nomor Jenis Unit Anda:"]
        jml_jenis_unit = 0
        for index, jenis_unit in enumerate(list_jenis_unit):
            tiap_data = []
            if list_produk[int(produk) - 1]['id'] == jenis_unit['product_id']:
                tiap_data.append("%s. %s" % (index+1, jenis_unit['name']))
                jml_jenis_unit += 1
            else:
                continue
            tiap_data = '\n'.join(tiap_data)

            if len(send_message[0]) + len(tiap_data) >= 1600:
                all_bubble.append(send_message)
                send_message = ['']
            send_message.append(tiap_data)
            send_message = "\n".join(send_message)
            send_message = [send_message]
        all_bubble.append(send_message)
        if jml_jenis_unit != 0:
            for bubble in all_bubble:
                message.append(bubble)
        else:
            send_message = ["Belum ada Jenis Unit untuk Produk: %s" %(list_produk[int(produk) - 1]['name'])]
            send_message.append("Masukkan Jenis Unit terlebih dahulu")
            message.append(("\n").join(send_message))
            
            send_message = ["Ketik *Pengaturan* untuk ke menu Pengaturan"]
            send_message.append("Ketik *Beranda* untuk ke menu Beranda")
            message.append(("\n").join(send_message))
            
            save_redis.delete("%s::menu"%(phone_number), "")
            save_redis.delete("%s::no_produk"%(phone_number), "")

    #  Jenis Unit TERSIMPAN, memasukkan Jenis Tagihan
    elif save_redis.get("%s::no_jenis_unit"%(phone_number)) is None:
        # menyimpan input jenis unit ke session
        input_jenis_unit = incoming_msg.strip()
        save_redis.set("%s::no_jenis_unit"%(phone_number), list_jenis_unit[int(input_jenis_unit) - 1]['id'])
        send_message = []
        # menampilkan data yang sudah dimasukkan
        send_message.append(save_redis.get("%s::message"%(phone_number)))
        send_message.append("Jenis Unit: %s" %(list_jenis_unit[int(input_jenis_unit) - 1]['name']))
        save_redis.set("%s::message"%(phone_number), ("\n").join(send_message))
        all_bubble.append('\n'.join(send_message))

        # mengambil data jenis tagihan berdasarkan produk yang diinput
        send_message = ["Silakan pilih nomor Jenis Tagihan Anda:"]
        jml_jenis_tagihan = 0
        for index, jenis_tagihan in enumerate(list_jenis_tagihan):
            tiap_data = []
            if list_produk[int(save_redis.get("%s::no_produk"%(phone_number))) - 1]["id"] == jenis_tagihan['product_id']:
                tiap_data.append("%s. %s" % (index+1, jenis_tagihan['name']))
                jml_jenis_tagihan += 1
            else:
                continue
            tiap_data = '\n'.join(tiap_data)

            if len(send_message[0]) + len(tiap_data) >= 1600:
                all_bubble.append(send_message)
                send_message = ['']
            send_message.append(tiap_data)
            send_message = '\n'.join(send_message)
            send_message = [send_message]
        all_bubble.append(send_message)
        if jml_jenis_tagihan != 0:
            for bubble in all_bubble:
                message.append(bubble)
                
        else:
            send_message = ["Belum ada Jenis Tagihan untuk Produk: %s" %(list_produk[int(save_redis.get("%s::no_produk"%(phone_number))) - 1]['name'])]
            send_message.append("Masukkan Jenis Tagihan terlebih dahulu")
            message.append(("\n").join(send_message))
            
            send_message = ["Ketik *Pengaturan* untuk ke menu Pengaturan"]
            send_message.append("Ketik *Beranda* untuk ke menu Beranda")
            message.append(("\n").join(send_message))
            
            save_redis.delete("%s::menu"%(phone_number), "")
            save_redis.delete("%s::no_produk"%(phone_number), "")
            save_redis.delete("%s::no_jenis_unit"%(phone_number), "")

    # Jenis Tagihan TERSIMPAN, memasukkan Jenis Perhitungan
    elif save_redis.get("%s::no_jenis_tagihan"%(phone_number)) is None:
        # menyimpan input jenis tagihan ke session
        input_jenis_tagihan = incoming_msg.strip()
        save_redis.set("%s::no_jenis_tagihan"%(phone_number), list_jenis_tagihan[int(input_jenis_tagihan) - 1]['id'])

        # menampilkan data yang sudah dimasukkan
        send_message = []
        send_message.append(save_redis.get("%s::message"%(phone_number)))
        send_message.append("Jenis Tagihan: %s" % (list_jenis_tagihan[int(input_jenis_tagihan) - 1]['name']))
        save_redis.set("%s::message"%(phone_number), ("\n").join(send_message))
        all_bubble.append('\n'.join(send_message))

        # mengambil jenis perhitungan
        send_message = ["Silakan pilih Jenis Perhitungan yang Anda inginkan:"]
        send_message.append("1. Formula")
        send_message.append("2. Range")
        all_bubble.append('\n'.join(send_message))
        # kirim tiap bubble chat
        for bubble in all_bubble:
            message.append(bubble)

    # Jenis Perhitungan TERSIMPAN, memasukkan Kategori Tagihan
    elif save_redis.get("%s::jenis_perhitungan"%(phone_number)) is None:
        # menyimpan input jenis perhitungan ke session
        input_jenis_perhitungan = incoming_msg.strip()
        pilihan = ''
        if int(input_jenis_perhitungan) == 1:
            pilihan = 'formula'
            save_redis.set("%s::jenis_perhitungan"%(phone_number), pilihan)
        elif int(input_jenis_perhitungan) == 2:
            pilihan = 'range'
            save_redis.set("%s::jenis_perhitungan"%(phone_number), pilihan)

        # menampilkan data yang sudah dimasukkan
        send_message = []
        send_message.append(save_redis.get("%s::message"%(phone_number)))
        send_message.append("Jenis Perhitungan: %s" % (pilihan))
        save_redis.set("%s::message"%(phone_number), ("\n").join(send_message))
        all_bubble.append('\n'.join(send_message))

        # mengambil kategori tagihan
        send_message = ["Silakan pilih Kategori Tagihan yang Anda inginkan:"]
        send_message.append("1. IPL")
        send_message.append("2. Listrik")
        send_message.append("3. Air")
        all_bubble.append('\n'.join(send_message))
        # kirim tiap bubble chat
        for bubble in all_bubble:
            message.append(bubble)

    # Kategori Tagihan TERSIMPAN, memasukkan Harga
    elif save_redis.get("%s::kategori_tagihan"%(phone_number)) is None:
        # menyimpan input kategori tagihan ke session
        input_kategori_tagihan = incoming_msg.strip()
        pilihan = ''
        if int(input_kategori_tagihan) == 1:
            pilihan = 'IPL'
            save_redis.set("%s::kategori_tagihan"%(phone_number), pilihan.lower())
        elif int(input_kategori_tagihan) == 2:
            pilihan = 'listrik'
            save_redis.set("%s::kategori_tagihan"%(phone_number), pilihan)
        elif int(input_kategori_tagihan) == 3:
            pilihan = 'air'
            save_redis.set("%s::kategori_tagihan"%(phone_number), pilihan)

        # menampilkan data yang sudah dimasukkan
        send_message = []
        send_message.append(save_redis.get("%s::message"%(phone_number)))
        send_message.append("Kategori tagihan: %s"%(pilihan))
        save_redis.set("%s::message"%(phone_number), ("\n").join(send_message))
        all_bubble.append('\n'.join(send_message))

        # jika user memilih 'FORMULA' untuk JENIS PERHITUNGAN
        if save_redis.get("%s::jenis_perhitungan"%(phone_number)) == 'formula':
            # mengambil data harga
            send_message = ['Silakan pilih nomor pada Daftar Harga Anda:']
            jml_jenis_harga = 0

            for index, jenis_harga in enumerate(list_harga):
                tiap_data = []
                if int(save_redis.get("%s::no_jenis_unit"%(phone_number))) == int(jenis_harga['unit_type_id']) and save_redis.get("%s::kategori_tagihan"%(phone_number)).lower() == jenis_harga['billing_category'].lower():
                    tiap_data.append("%s. %s" %(index+1, formatrupiah(jenis_harga['base_price'])))
                    jml_jenis_harga += 1
                else:
                    continue
                tiap_data = '\n'.join(tiap_data)

                if len(send_message[0]) + len(tiap_data) >= 1600:
                    all_bubble.append(send_message)
                    send_message = ['']
                send_message.append(tiap_data)
                send_message = '\n'.join(send_message)
                send_message = [send_message]
            all_bubble.append(send_message)
            if jml_jenis_harga != 0:
                for bubble in all_bubble:
                    message.append(bubble)
            else:
                send_message = ['Belum ada Harga yang tersedia']
                send_message.append("Masukkan Harga terlebih dahulu")
                message.append(("\n").join(send_message))
                
                send_message = ["Ketik *Pengaturan* untuk ke menu Pengaturan"]
                send_message.append("Ketik *Beranda* untuk ke menu Beranda")
                message.append(("\n").join(send_message))
                
                save_redis.delete("%s::menu"%(phone_number), "")
                save_redis.delete("%s::kategori_tagihan"%(phone_number), "")
                save_redis.delete("%s::jenis_perhitungan"%(phone_number), "")
                save_redis.delete("%s::no_jenis_tagihan"%(phone_number), "")
                save_redis.delete("%s::no_jenis_unit"%(phone_number), "")
                save_redis.delete("%s::no_produk"%(phone_number), "")
                
        # jika user memilih RANGE untuk JENIS PERHITUNGAN
        elif save_redis.get("%s::jenis_perhitungan"%(phone_number)) == 'range':
            message = ['Masukkan range harga:']

    # Harga TERSIMPAN, memasukkan Formula
    elif save_redis.get("%s::no_harga"%(phone_number)) is None:
        # menyimpan input harga
        input_nomor_harga = incoming_msg.strip()
        save_redis.set("%s::no_harga"%(phone_number), list_harga[int(input_nomor_harga)-1]['id'])

        # menampilkan data yang sudah dimasukkan
        send_message = []
        send_message.append(save_redis.get("%s::message"%(phone_number)))
        send_message.append("Harga: %s" %(formatrupiah(list_harga[int(input_nomor_harga)-1]['base_price'])))
        save_redis.set("%s::message"%(phone_number), ("\n").join(send_message))
        all_bubble.append('\n'.join(send_message))

        # contoh pengisian formula
        send_message = ['Silakan masukkan formula seperti contoh ini:']
        send_message.append("*price.base_price * unit.size*")
        all_bubble.append('\n'.join(send_message))
        for bubble in all_bubble:
            message.append(bubble)

    # Nembak endpoint untuk pilihan Jenis Perhitungan Formula
    else:
        input_formula = incoming_msg.strip()

        if json.loads(save_redis.get("%s::menu"%(phone_number)))['formula'] == 'tambah':
            tambah = requests.post(app.config['URL']+"/formula",
                                   headers={
                                       "Authorization": "Bearer " + save_redis.get("%s::token"%(phone_number))},
                                   json={
                                        "product_id": int(list_produk[int(save_redis.get("%s::no_produk"%(phone_number))) - 1]['id']),
                                        "unit_type_id": int(save_redis.get("%s::no_jenis_unit"%(phone_number))),
                                        "billing_type_id": int(save_redis.get("%s::no_jenis_tagihan"%(phone_number))),
                                        "charge_type": save_redis.get("%s::jenis_perhitungan"%(phone_number)),
                                        "billing_category":save_redis.get("%s::kategori_tagihan"%(phone_number)),
                                        "price_id": int(save_redis.get("%s::no_harga"%(phone_number))),
                                        "formulation": input_formula,
                                    })
            if tambah.status_code == 200:
                message = ["Formula berhasil ditambahkan"]
            else:
                message = ["Formula gagal ditambahkan"]
                message.append(tambah.json()["message"]["body"])
                message = [("\n").join(message)]

        elif json.loads(save_redis.get("%s::menu"%(phone_number)))['formula'] == 'ubah':
            ubah = requests.put(app.config['URL']+"/formula/" + str(save_redis.get("%s::id_formula"%(phone_number))),
                                 headers={
                                     "Authorization": "Bearer " + save_redis.get("%s::token"%(phone_number))},
                                 json={
                                        "product_id": int(list_produk[int(save_redis.get("%s::no_produk"%(phone_number))) - 1]['id']),
                                        "unit_type_id": int(save_redis.get("%s::no_jenis_unit"%(phone_number))),
                                        "billing_type_id": int(save_redis.get("%s::no_jenis_tagihan"%(phone_number))),
                                        "charge_type": save_redis.get("%s::jenis_perhitungan"%(phone_number)),
                                        "billing_category":save_redis.get("%s::kategori_tagihan"%(phone_number)),
                                        "price_id": int(save_redis.get("%s::no_harga"%(phone_number))),
                                        "formulation": input_formula,
                                    })
            if ubah.status_code == 200:
                message = ["Formula berhasil diubah"]
            else:
                message = ["Formula gagal diubah"]
                message.append(ubah.json()["message"]["body"])
                message = [("\n").join(message)]
                
        send_message = ["Ketik *Formula* untuk ke menu Formula"]
        send_message.append("Ketik *Pengaturan* untuk kembali ke menu Pengaturan")
        send_message.append("Ketik *Beranda* untuk kembali ke menu Beranda")
        message.append(("\n").join(send_message))
        
        save_redis.set("%s::menu"%(phone_number), "formula")
        
        save_redis.delete("%s::no_produk"%(phone_number), "")
        save_redis.delete("%s::no_jenis_unit"%(phone_number), "")
        save_redis.delete("%s::no_jenis_tagihan"%(phone_number), "")
        save_redis.delete("%s::jenis_perhitungan"%(phone_number), "")
        save_redis.delete("%s::kategori_tagihan"%(phone_number), "")
        save_redis.delete("%s::no_harga"%(phone_number), "")

    return message

# Menu tambah Formula
def tambah_formula(incoming_msg, phone_number):
    message = []

    # data produk
    respon_produk = requests.post(app.config['URL']+"/product/all", headers={"Authorization": "Bearer " + save_redis.get("%s::token"%(phone_number))})
    respon_produk = respon_produk.json()
    list_produk = respon_produk['data']['records']

    # ketika user baru mengetik tambah
    if save_redis.get("%s::menu"%(phone_number)) == "formula":
        if respon_produk["data"]["count"] != 0:
            message_bubble = ["Berikut ini adalah Daftar Produk milik Anda: "]
            all_bubble = []
            for index, produk in enumerate(list_produk):
                tiap_data = []
                tiap_data.append("%s. Produk: %s" % (index+1, produk['name']))
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
            
            message.append("Silakan masukkan nomor Produk:")
            save_redis.set("%s::menu"%(phone_number), json.dumps({"formula": "tambah"}))
        else:
            message.append("Anda belum mengisi Produk, silahkan isi produk terlebih dahulu!")

    # ketika user sudah memasukkan data
    else:
        message = fungsi_formula(phone_number, incoming_msg)

    return message

# Menu ubah Formula
def ubah_formula(incoming_msg, phone_number, id_formula=None):
    all_bubble = []
    message = []

    # data produk
    respon_produk = requests.post(app.config['URL']+"/product/all",
                                  headers={"Authorization": "Bearer " + save_redis.get("%s::token"%(phone_number))}
                                )
    respon_produk = respon_produk.json()
    list_produk = respon_produk['data']['records']
    # data formula yang dipilih
    if id_formula is None:
        respon_formula = requests.get(app.config['URL']+"/formula/" + str(save_redis.get("%s::id_formula"%(phone_number))),
                                      headers={"Authorization": "Bearer " + save_redis.get("%s::token"%(phone_number))}
                                    )
    else:
        respon_formula = requests.get(app.config['URL']+"/formula/" + str(id_formula),
                                      headers={"Authorization": "Bearer " + save_redis.get("%s::token"%(phone_number))}
                                    )
    respon_formula = respon_formula.json()

    send_message = ["Berikut ini Formula yang ingin Anda ubah:"]
    send_message.append("Produk: %s" % (respon_formula['data']["product_name"]))
    send_message.append("Jenis Unit: %s" %(respon_formula['data']['unit_type_name']))
    send_message.append("Jenis Tagihan: %s" %(respon_formula['data']['billing_type_name']))
    send_message.append("Jenis Perhitungan: %s" %(respon_formula['data']['charge_type']))
    send_message.append("Kategori Tagihan: %s" %(respon_formula['data']['billing_category']))
    send_message.append("Harga: %s" % (formatrupiah(respon_formula['data']['base_price'])))
    send_message.append("Formula: %s" % (respon_formula['data']['formulation']))
    all_bubble.append('\n'.join(send_message))

    if id_formula is not None:
        save_redis.set("%s::id_formula"%(phone_number), id_formula)
        if respon_produk["data"]["count"] != 0:
            send_message = ["Silahkan pilih nomor Produk Anda: "]
            for index, produk in enumerate(list_produk):
                tiap_data = []
                tiap_data.append("%s. %s" % (index+1, produk['name']))
                tiap_data = '\n'.join(tiap_data)

                if len(send_message[0]) + len(tiap_data) >= 1600:
                    all_bubble.append(send_message)
                    send_message = ['']
                send_message.append(tiap_data)
                send_message = '\n'.join(send_message)
                send_message = [send_message]
            all_bubble.append(("\n").join(send_message))
            
            for bubble in all_bubble:
                message.append(bubble)
            
            save_redis.set("%s::menu"%(phone_number), json.dumps({"formula": "ubah"}))
        else:
            message.append("Anda belum mengisi Produk, silakan isi produk terlebih dahulu!")

    else:
        for bubble in all_bubble:
            message.append(bubble)
            
        message += fungsi_formula(phone_number, incoming_msg)
        
    return message

# Menu hapus Formula
def hapus_formula(id_formula, phone_number):
    hapus = requests.delete(app.config['URL']+"/formula/" + str(id_formula),
                            headers={"Authorization": "Bearer " + save_redis.get("%s::token"%(phone_number))}
                            )
    if hapus.status_code == 200:
        message = ["Formula berhasil dihapus!"]
    else:
        message = ["Formula gagal dihapus!"]

    message.append("")
    message.append("Ketik *Formula* untuk kembali ke halaman Formula")
    message.append("Ketik *Pengaturan* untuk kembali ke halaman Pengaturan")
    message.append("Ketik *Beranda* untuk kembali ke halaman Beranda")

    return [("\n").join(message)]
