import requests
import re
import config
import json
from blueprints import app
from blueprints import save_redis
from datetime import datetime
from flask import Flask
from flask import request
from functions import regex
from functions import regex_num
from functions import formatrupiah
from functions import convertDate

# Menu awal riwayat tagihan
def riwayat_tagihan(incoming_msg, phone_number, bot_responses):
    semua = requests.post(app.config['URL']+"/billing/list", headers={"Authorization": "Bearer " + save_redis.get("%s::token" %(phone_number))})
    semua = semua.json()
    list_semua = semua['data']

    all_bubble = []
    message = []
    pesan = []
    
    if "riwayat" == save_redis.get("%s::menu" %(phone_number)):
        send_message = []
        send_message.append(bot_responses)
        send_message.append("")
        send_message.append('1. *semua* - untuk melihat semua riwayat tagihan')
        send_message.append('2. *unpaid* - untuk melihat riwayat tagihan yang belum terbayarkan')
        send_message.append('3. *paid* - untuk melihat riwayat tagihan yang sudah terbayarkan')
        send_message.append('4. *generate link* - untuk membuat link tagihan dari tagihan yang sudah pernah dibuat')
        message.append(("\n").join(send_message))
        save_redis.set("%s::menu" %(phone_number), json.dumps({"riwayat": "masuk"}))
        save_redis.delete("%s::submenu"%(phone_number), "")
        
    else:
        if len(list_semua) > 0:
            jumlah = 0
            index = 0
            status = ""
            send_message = ['Berikut ini adalah 10 Daftar Riwayat Tagihan terbaru Anda:\n']
            while jumlah < 10 and index < len(list_semua):
                if "1" == incoming_msg or "semua" == incoming_msg.lower():
                    jumlah += 1
                elif "2" == incoming_msg or "unpaid" == incoming_msg.lower():
                    status = "unpaid"
                    if list_semua[index]['billing_status'] == 1:
                        jumlah += 1
                    else:
                        index += 1
                        continue
                if "3" == incoming_msg or "paid" == incoming_msg.lower():
                    status = "paid"
                    if list_semua[index]['billing_status'] == 2 or list_semua[index]['billing_status'] == 3:
                        jumlah += 1
                    else:
                        index += 1
                        continue
                
                tiap_data = []
                tiap_data.append("%s. ID Tagihan: %s" %(index+1, list_semua[index]['billing_id']))
                tiap_data.append("    Produk: %s" %(list_semua[index]['product_name']))
                tiap_data.append("    Unit: %s" %(list_semua[index]['unit_name']))
                tiap_data.append("    Nama Pelanggan: %s" %(list_semua[index]['customer_name']))
                tiap_data.append("    Tagihan Sebelumnya: %s" %(formatrupiah(list_semua[index]['previous_balance'])))
                tiap_data.append("    Tagihan Saat Ini: %s" %(formatrupiah(list_semua[index]['current_balance'])))
                tiap_data.append("    Jumlah Tagihan: %s" %(formatrupiah(list_semua[index]['total'])))
                tiap_data.append("    Denda: %s" %(formatrupiah(list_semua[index]['charge'])))
                tiap_data.append("    Periode: %s" %(convertDate(list_semua[index]['billing_periode'])))
                tiap_data.append("    Mulai Tagihan: %s" %(convertDate(list_semua[index]['billing_start_date'])))
                tiap_data.append("    Jatuh Tempo: %s" %(convertDate(list_semua[index]['billing_end_date'])))
                if list_semua[index]['billing_status'] == 0:
                    status = "Unsent"
                elif list_semua[index]['billing_status'] == 1:
                    status = "Unpaid"
                elif list_semua[index]['billing_status'] == 2:
                    status = "Paid - Manually"
                elif list_semua[index]['billing_status'] == 3:
                    status = "Paid - AturTagihan"
                elif list_semua[index]['billing_status'] == 4:
                    status = "Settlement - AturTagihan"
                elif list_semua[index]['billing_status'] == 5:
                    status = "Expired"
                tiap_data.append("    Status: %s\n" % (status))
                tiap_data = ('\n').join(tiap_data)

                if len(send_message[0]) + len(tiap_data) >= 1600:
                    all_bubble.append(send_message)
                    send_message = ['']
                send_message.append(tiap_data)
                send_message = ('\n').join(send_message)
                send_message = [send_message]
                
                index += 1
            all_bubble.append(send_message)

            for bubble in all_bubble:
                message.append(bubble)
            send_message = []
            if jumlah == 0:
                message=['Tidak ada riwayat tagihan dengan status *%s*'%(status)]
            else:
                pesan_msg = []
                pesan_msg.append('Kalau mau lihat Riwayat Tagihan yang lebih detail, Anda bisa klik link di bawah ini:')
                pesan_msg.append("https://dashboard.aturtagihan.com/riwayat-tagihan")
                message.append(("\n").join(pesan_msg))
            
        else:
            send_message = ['Anda belum memiliki riwayat tagihan']
        save_redis.set("%s::menu" %(phone_number), "riwayat")
            
        message.append(("\n").join(send_message))
        
        pesan.append("Ketik *Riwayat Tagihan* untuk kembali ke halaman Riwayat Tagihan")
            
    pesan.append("Ketik *Pengaturan* untuk kembali ke halaman Pengaturan")
    pesan.append("Ketik *Beranda* untuk kembali ke halaman Beranda")
    message.append(("\n").join(pesan))

    return message

