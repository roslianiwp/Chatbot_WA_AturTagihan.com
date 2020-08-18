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

# Menu awal unit
def unit(incoming_msg, phone_number, bot_responses):
    respon_unit = requests.post(app.config['URL']+"/unit/all", headers={"Authorization": "Bearer "+ save_redis.get("%s::token" %(phone_number))})
    respon_unit = respon_unit.json()
    list_unit = respon_unit["data"]['records']
    message = []
    if "unit" in save_redis.get("%s::menu" %(phone_number)):
        # ketika user BELUM mengetikkan "tambah"/"ubah"/"hapus"
        if "tambah" in incoming_msg.lower():
            message = tambah_unit(incoming_msg, phone_number)
        elif "ubah" in incoming_msg.lower():
            no_unit = re.findall("ubah.+", incoming_msg.lower())
            no_unit = regex_num(no_unit[0])
            if int(no_unit) > len(list_unit):
                message.append("Nomor Produk yang Anda masukkan tidak tersedia!")
                message.append("")
                message.append("Silakan ketik *Unit* untuk kembali ke halaman sebelumnya")
            else:
                id_unit = respon_unit['data']['records'][int(no_unit)-1]['id']
                message = ubah_unit(incoming_msg, phone_number, id_unit)
        elif "hapus" in incoming_msg.lower():
            save_redis.set("%s::unit" %(phone_number), "hapus")
            message = hapus_unit(incoming_msg, phone_number)
            
        # ketika user SUDAH mengetikkan "tambah"/"ubah"/"hapus"
        elif save_redis.get("%s::menu" %(phone_number)) == "unit":
            if respon_unit["data"]["count"] != 0:
                message_bubble = [bot_responses]
                all_bubble = []
                for index, item in enumerate(list_unit):
                    tiap_data = []
                    tiap_data.append("%s. Nama: %s" %(index+1, item['name'].capitalize()))
                    tiap_data.append("    Produk: %s" %( item['product_name'].capitalize()))
                    tiap_data.append("    Jenis Unit: %s" %( item['unit_type_name'].capitalize()))
                    tiap_data.append("    Nama Pelanggan: %s" %( item['customer_name'].capitalize()))
                    tiap_data.append("    Periode Penyewaan: %s" %( item['mapping_period_name'].capitalize()))
                    tiap_data.append("    Ukuran Unit: %s m2" %( item['size']))
                    tiap_data.append("    Alamat Unit: %s" %( item['address'].capitalize()))
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
                message.append("Anda belum mengisi unit!")

            pesan = []
            pesan.append("Apa yang bisa Hedwig bantu?")
            pesan.append("- Ketik *tambah* untuk menambahkan unit")
            pesan.append("- Ketik *ubah* <spasi> *no_unit* untuk mengubah unit")
            pesan.append("- Ketik *hapus* <spasi> *no_unit* untuk menghapus unit")
            pesan.append("")
            pesan.append("Ketik *Pengaturan* untuk kembali ke halaman Pengaturan")
            pesan.append("Ketik *Beranda* untuk kembali ke halaman Beranda")
            message.append(("\n").join(pesan))

        else:
            read = json.loads(save_redis.get("%s::menu" %(phone_number)))
            if 'tambah' in read['unit']:
                message = tambah_unit(incoming_msg, phone_number)
            elif 'ubah' in read['unit']:
                message = ubah_unit(incoming_msg, phone_number, id=None)
            
    return message

def fungsi_unit(incoming_msg, phone_number):
    message = []
    
    # user diminta memasukkan ukuran unit
    # menyimpan data nama unit
    if save_redis.get("%s::unit" %(phone_number)) == 'nama_unit':
        incoming_msg = incoming_msg.strip()
        save_redis.set("%s::unit"%(phone_number), "ukuran_unit")
        save_redis.set("%s::nama_unit"%(phone_number), incoming_msg)
        message.append("Sekarang, masukkan ukuran unit Anda")
        message.append("Ukurannya dalam m2 yaa")
  
    # user diminta memasukkan no produk
    # menyimpan data ukuran unit
    elif save_redis.get("%s::unit" %(phone_number)) == 'ukuran_unit':
        incoming_msg = incoming_msg.strip()
        
        # data produk
        respon_produk = requests.post(app.config['URL']+"/product/all", headers={"Authorization": "Bearer "+ save_redis.get("%s::token" %(phone_number))})
        respon_produk = respon_produk.json()
        list_produk = respon_produk['data']['records']
        
        # ketika produk masih kosong
        if len(list_produk) < 1:
            message.append("Anda belum mengisi produk, yuk isi produk terlebih dahulu")
            
            pesan = []
            pesan.append("Ketik *Unit* untuk kembali ke halaman Unit")
            pesan.append("Ketik *Pengaturan* untuk kembali ke halaman Pengaturan")
            pesan.append("Ketik *Beranda* untuk kembali ke halaman Beranda")
            message.append(("\n").join(pesan))
            
            save_redis.set("%s::menu"%(phone_number), "unit")
            save_redis.delete("%s::unit"%(phone_number), "")
            save_redis.delete("%s::nama_unit"%(phone_number), "")
            save_redis.delete("%s::jumlah_unit"%(phone_number), "")
            
        # ketika produk ada
        else:
            send_message = []
            for index, produk in enumerate(list_produk):
                send_message.append("%s. %s" % (index+1, produk['name']))
            message.append(("\n").join(send_message))
            
            message.append("Selanjutnya, pilih No Produk yang ingin Anda tambahkan")
            
            save_redis.set("%s::unit"%(phone_number), "no_produk")
            save_redis.set("%s::ukuran_unit"%(phone_number), incoming_msg)
    
    # user diminta memasukkan alamat
    # menyimpan data nomor produk
    elif save_redis.get("%s::unit" %(phone_number)) == 'no_produk':
        incoming_msg = incoming_msg.strip()
        
        # data produk
        respon_produk = requests.post(app.config['URL']+"/product/all", headers={"Authorization": "Bearer "+ save_redis.get("%s::token" %(phone_number))})
        respon_produk = respon_produk.json()
        list_produk = respon_produk['data']['records']
        
        if int(incoming_msg) > len(list_produk):
            message.append("Nomor yang Anda masukkan tidak ada dalam daftar!")
            message.append("Yuk pilih lagi No Produk Anda")
        else:
            save_redis.set("%s::unit"%(phone_number), "alamat")
            save_redis.set("%s::no_produk"%(phone_number), incoming_msg)
            message.append("Lalu, masukkan Alamat Unit Anda")
            
    # user diminta memasukkan nomor jenis unit
    # menyimpan data alamat
    elif save_redis.get("%s::unit" %(phone_number)) == 'alamat':
        incoming_msg = incoming_msg.strip()
    
        # data jenis unit
        respon_jenis_unit = requests.post(app.config['URL']+"/unit_type/all", headers={"Authorization": "Bearer "+ save_redis.get("%s::token" %(phone_number))})
        respon_jenis_unit = respon_jenis_unit.json()
        list_jenis_unit = respon_jenis_unit['data']['records']
        
        # data produk
        respon_produk = requests.post(app.config['URL']+"/product/all", headers={"Authorization": "Bearer "+ save_redis.get("%s::token" %(phone_number))})
        respon_produk = respon_produk.json()
        list_produk = respon_produk['data']['records']
        
        if len(list_jenis_unit) < 1:
            message.append("Anda belum mengisi jenis unit, silakan isi jenis unit terlebih dahulu")
            
            pesan = []
            pesan.append("Ketik *Unit* untuk kembali ke halaman Unit")
            pesan.append("Ketik *Pengaturan* untuk kembali ke halaman Pengaturan")
            pesan.append("Ketik *Beranda* untuk kembali ke halaman Beranda")
            message.append(("\n").join(pesan))
            
            save_redis.set("%s::menu"%(phone_number), "unit")
            save_redis.delete("%s::unit"%(phone_number), "")
            save_redis.delete("%s::jumlah_unit"%(phone_number), "")
            save_redis.delete("%s::nama_unit"%(phone_number), "")
            save_redis.delete("%s::ukuran_unit"%(phone_number), "")
            save_redis.delete("%s::no_produk"%(phone_number), "")
        else:
            send_message = []
            jml_jenis_unit = 0
            for index, jenis_unit in enumerate(list_jenis_unit):
                if list_produk[int(save_redis.get("%s::no_produk"%(phone_number)))-1]["id"] == int(jenis_unit["product_id"]):
                    send_message.append("%s. %s" % (index+1, jenis_unit['name']))
                    jml_jenis_unit += 1
            
            if jml_jenis_unit != 0:
                message.append(("\n").join(send_message))
                
                message.append("Baik, sekarang masukkan No Jenis Unit yang ingin Anda tambahkan")
                
                save_redis.set("%s::unit"%(phone_number), "no_jenis_unit")
                save_redis.set("%s::alamat"%(phone_number), incoming_msg)
            else:
                send_msg = []
                send_msg.append("Belum ada Jenis Unit untuk Produk: %s"%(list_produk[int(save_redis.get("%s::no_produk"%(phone_number))) - 1]['name']))
                send_msg.append("")
                send_msg.append("Masukkan Jenis Unit terlebih dahulu!")
                message.append(("\n").join(send_msg))
                pesan = []
                pesan.append("")
                pesan.append("Ketik *Unit* untuk kembali ke halaman Unit")
                pesan.append("Ketik *Pengaturan* untuk kembali ke halaman Pengaturan")
                pesan.append("Ketik *Beranda* untuk kembali ke halaman Beranda")
                save_redis.set("%s::menu" %(phone_number), "unit")
                save_redis.delete("%s::unit"%(phone_number), "")
                save_redis.delete("%s::jumlah_unit"%(phone_number), "")
                save_redis.delete("%s::nama_unit"%(phone_number), "")
                save_redis.delete("%s::ukuran_unit"%(phone_number), "")
                save_redis.delete("%s::no_produk"%(phone_number), "")
    
    # user diminta memasukkan pelanggan
    # menyimpan data nomor jenis unit
    elif save_redis.get("%s::unit" %(phone_number)) == 'no_jenis_unit':
        incoming_msg = incoming_msg.strip()
        
        # data jenis unit
        respon_jenis_unit = requests.post(app.config['URL']+"/unit_type/all", headers={"Authorization": "Bearer "+ save_redis.get("%s::token" %(phone_number))})
        respon_jenis_unit = respon_jenis_unit.json()
        list_jenis_unit = respon_jenis_unit['data']['records']
        
        # pelanggan
        respon_pelanggan = requests.post(app.config['URL']+"/customer/all", headers={"Authorization": "Bearer "+ save_redis.get("%s::token" %(phone_number))})
        respon_pelanggan = respon_pelanggan.json()
        list_pelanggan = respon_pelanggan['data']['records']
        
        # data produk
        respon_produk = requests.post(app.config['URL']+"/product/all", headers={"Authorization": "Bearer "+ save_redis.get("%s::token" %(phone_number))})
        respon_produk = respon_produk.json()
        list_produk = respon_produk['data']['records']
        
        if int(incoming_msg) > len(list_jenis_unit):
            message.append("Nomor yang Anda masukkan tidak ada dalam daftar")
            message.append("Silakan masukkan lagi No Jenis Unit Anda")
        else:
            # ketika pelanggan masih kosong
            if len(list_pelanggan) < 1:
                message.append("Anda belum mengisi pelanggan, yuk isi data pelanggan dahulu di halaman Pelanggan")
                
                pesan = []
                pesan.append("Ketik *Unit* untuk kembali ke halaman Unit")
                pesan.append("Ketik *Pengaturan* untuk kembali ke halaman Pengaturan")
                pesan.append("Ketik *Beranda* untuk kembali ke halaman Beranda")
                message.append(("\n").join(pesan))
                
                save_redis.set("%s::menu"%(phone_number), "unit")
                save_redis.delete("%s::unit"%(phone_number), "")
                save_redis.delete("%s::nama_unit"%(phone_number), "")
                save_redis.delete("%s::jumlah_unit"%(phone_number), "")
                save_redis.delete("%s::ukuran_unit"%(phone_number), "")
                save_redis.delete("%s::no_produk"%(phone_number), "")
                
            # pelanggan sudah ada
            else:
                send_message = []
                jml_pelanggan = 0
                for index, pelanggan in enumerate(list_pelanggan):
                    if list_produk[int(save_redis.get("%s::no_produk"%(phone_number)))-1]["id"] == pelanggan["product_id"]:
                        send_message.append("%s. %s" % (index+1, pelanggan['name']))
                        jml_pelanggan += 1
                
                if jml_pelanggan != 0:
                    message.append(("\n").join(send_message))
                    
                    message.append("Pelanggan mana yang ingin Anda tambahkan? Tulis nomornya ya!")
                    
                    save_redis.set("%s::unit"%(phone_number), "no_pelanggan")
                    save_redis.set("%s::no_jenis_unit"%(phone_number), list_jenis_unit[int(incoming_msg)-1]["id"])
                    save_redis.set("%s::no_produk"%(phone_number), list_produk[int(save_redis.get("%s::no_produk"%(phone_number)))-1]["id"])
                else:
                    send_msg = []
                    send_msg.append("Belum ada Pelanggan untuk Produk: %s"%(list_produk[int(save_redis.get("%s::no_produk"%(phone_number))) - 1]['name']))
                    send_msg.append("Masukkan Pelanggan terlebih dahulu!")
                    message.append(("\n").join(send_msg))
                    pesan = []
                    pesan.append("Ketik *Unit* untuk kembali ke halaman Unit")
                    pesan.append("Ketik *Pengaturan* untuk kembali ke halaman Pengaturan")
                    pesan.append("Ketik *Beranda* untuk kembali ke halaman Beranda")
                    save_redis.set("%s::menu" %(phone_number), "unit")
                    save_redis.delete("%s::unit"%(phone_number), "")
                    save_redis.delete("%s::nama_unit"%(phone_number), "")
                    save_redis.delete("%s::jumlah_unit"%(phone_number), "")
                    save_redis.delete("%s::ukuran_unit"%(phone_number), "")
                    save_redis.delete("%s::no_produk"%(phone_number), "")
                    
    # menyimpan data nomor pelanggan
    elif save_redis.get("%s::unit" %(phone_number)) == 'no_pelanggan':
        incoming_msg = incoming_msg.strip()
        
        # pelanggan
        respon_pelanggan = requests.post(app.config['URL']+"/customer/all", headers={"Authorization": "Bearer "+ save_redis.get("%s::token" %(phone_number))})
        respon_pelanggan = respon_pelanggan.json()
        list_pelanggan = respon_pelanggan['data']['records']
        
        if int(incoming_msg) > len(list_pelanggan):
            message.append("Nomor yang Anda masukkan tidak ada dalam daftar")
            message.append("Silakan masukkan lagi No Pelanggan Anda")
        else:
            mapping_period = 117
            if "aturtagihan" in app.config['URL']:
                mapping_period = 1
            if "tambah" in save_redis.get("%s::menu" %(phone_number)):
                for i in range(int(save_redis.get("%s::jumlah_unit"%(phone_number)))):
                    if int(save_redis.get("%s::jumlah_unit"%(phone_number))) == 1:
                        nama_unit = save_redis.get("%s::nama_unit"%(phone_number))
                    else:
                        nama_unit = save_redis.get("%s::nama_unit"%(phone_number)) + "-" + str(i+1)
                    print("no produk: ", int(save_redis.get("%s::no_produk"%(phone_number))))
                    tambah = requests.post(app.config['URL']+"/unit", 
                        headers={"Authorization": "Bearer "+ save_redis.get("%s::token" %(phone_number))},
                        json={
                            "name": nama_unit,
                            "product_id":int(save_redis.get("%s::no_produk"%(phone_number))),
                            "unit_type_id": int(save_redis.get("%s::no_jenis_unit"%(phone_number))),
                            "mapping_period_id":mapping_period,
                            "customer_id": int(list_pelanggan[int(incoming_msg) - 1]['id']),
                            "size": int(save_redis.get("%s::ukuran_unit" %(phone_number))),
                            "address": save_redis.get("%s::alamat"%(phone_number))
                        })
                    if tambah.status_code == 200:
                        message.append("Unit berhasil ditambahkan!")
                    else:
                        message.append("Unit gagal ditambahkan!")
                        message.append(tambah.json()["message"]["body"])
            elif "ubah" in save_redis.get("%s::menu" %(phone_number)):
                ubah = requests.put(app.config['URL']+"/unit/"+str(save_redis.get("%s::id_unit" %(phone_number))), 
                    headers={"Authorization": "Bearer "+ save_redis.get("%s::token" %(phone_number))},
                    json={
                        "name": save_redis.get("%s::nama_unit"%(phone_number)),
                        "product_id":int(save_redis.get("%s::no_produk"%(phone_number))),
                        "unit_type_id": int(save_redis.get("%s::no_jenis_unit"%(phone_number))),
                        "mapping_period_id":mapping_period,
                        "customer_id": int(list_pelanggan[int(incoming_msg) - 1]['id']),
                        "size": int(save_redis.get("%s::ukuran_unit" %(phone_number))),
                        "address": save_redis.get("%s::alamat"%(phone_number))
                    })
                if ubah.status_code == 200:
                    message.append("Unit berhasil diubah")
                else:
                    message.append("Unit gagal diubah")
                    message.append(ubah.json()["message"]["body"])
            pesan = []
            pesan.append("Ketik *Unit* untuk kembali ke halaman Unit")
            pesan.append("Ketik *Pengaturan* untuk kembali ke halaman Pengaturan")
            pesan.append("Ketik *Beranda* untuk kembali ke halaman Beranda")
            message.append(("\n").join(pesan)) 
                
            save_redis.set("%s::menu" %(phone_number), "unit")
            save_redis.delete("%s::jumlah_unit" %(phone_number), "")
            save_redis.delete("%s::nama_unit" %(phone_number), "")
            save_redis.delete("%s::ukuran_unit" %(phone_number), "")
            save_redis.delete("%s::no_produk" %(phone_number), "")
            save_redis.delete("%s::alamat" %(phone_number), "")
            save_redis.delete("%s::no_jenis_unit" %(phone_number), "")
            save_redis.delete("%s::no_pelanggan" %(phone_number), "")
    
    return message
 
def tambah_unit(incoming_msg, phone_number):
    message = []
    
    # user diminta memasukkan jumlah unit
    if save_redis.get("%s::menu" %(phone_number)) == 'unit':
        message.append("Ikuti langkah-langkah yang Hedwig kasih tahu ya!")
        message.append("Pertama, masukkan jumlah unit yang ingin ditambahkan")
        save_redis.set("%s::menu"%(phone_number), json.dumps({"unit":"tambah"}))
        save_redis.set("%s::unit"%(phone_number), "jumlah_unit")
  
    # user diminta memasukkan nama unit
    # menyimpan data jumlah unit
    elif save_redis.get("%s::unit" %(phone_number)) == 'jumlah_unit':
        incoming_msg = incoming_msg.strip()
        message.append("Lalu, masukkan nama unit Anda")
        save_redis.set("%s::jumlah_unit"%(phone_number), incoming_msg)
        save_redis.set("%s::unit"%(phone_number), "nama_unit")
  
    # pindah ke fungsi unit
    else:
        message = fungsi_unit(incoming_msg, phone_number)
  
    return message

def ubah_unit(incoming_msg, phone_number, id):
    message = []
    
    if id != None:
        respon_unit = requests.get(app.config['URL']+"/unit/"+ str(id), headers={"Authorization": "Bearer "+ save_redis.get("%s::token" %(phone_number))})
        save_redis.set("%s::id_unit" %(phone_number),id)
        respon_unit = respon_unit.json()
        item = respon_unit['data']
        isi_unit = []
        isi_unit.append("Berikut inilah Unit yang ingin Anda ubah:")
        isi_unit.append("%s. Nama: %s" %(1, item['name'].capitalize()))
        isi_unit.append("    Produk: %s" %( item['product_name'].capitalize()))
        isi_unit.append("    Jenis Unit: %s" %( item['unit_type_name'].capitalize()))
        isi_unit.append("    Nama Pelanggan: %s" %( item['customer_name'].capitalize()))
        isi_unit.append("    Periode Penyewaan: %s" %( item['mapping_period_name'].capitalize()))
        isi_unit.append("    Ukuran Unit: %s m2" %( item['size']))
        isi_unit.append("    Alamat Unit: %s" %( item['address'].capitalize()))

        kirim_msg = ("\n").join(isi_unit)
        message.append(kirim_msg)
    
        message.append("Silakan masukkan nama unit Anda")
        save_redis.set("%s::unit"%(phone_number), "nama_unit")
        save_redis.set("%s::menu" %(phone_number), json.dumps({"unit":"ubah"}))
  
    # pindah ke fungsi unit
    else:
        message += fungsi_unit(incoming_msg, phone_number)
  
    return message

def hapus_unit(id, phone_number):
    message = []
    respon_unit = requests.post(app.config['URL']+"/unit/all", headers={"Authorization": "Bearer "+ save_redis.get("%s::token" %(phone_number))})
    respon_unit = respon_unit.json()
    no_unit = re.findall("hapus.+", id.lower())
    no_unit = regex_num(no_unit[0])
    if int(no_unit) <= len(respon_unit['data']['records']):
        id_unit = respon_unit['data']['records'][int(no_unit)-1]['id']
        hapus = requests.delete(app.config['URL']+"/unit/" + str(id_unit), 
            headers={"Authorization": "Bearer "+ save_redis.get("%s::token" %(phone_number))})
        if hapus.status_code == 200:
            message.append("Unit berhasil dihapus!")
        else: 
            message.append("Unit gagal dihapus! ")
    else:
        message.append("Nomor Unit yang Anda masukkan salah")
        message.append("Silakan ulangi kembali")

    pesan = []
    pesan.append("Ketik *Unit* untuk kembali ke halaman Unit")
    pesan.append("Ketik *Pengaturan* untuk kembali ke halaman Pengaturan")
    pesan.append("Ketik *Beranda* untuk kembali ke halaman Beranda")
    message.append(('\n').join(pesan))
    save_redis.delete("%s::unit" %(phone_number), "")
    save_redis.set("%s::menu"%(phone_number), "unit")
    return message