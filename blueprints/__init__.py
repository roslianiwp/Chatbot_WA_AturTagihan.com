import requests
import os
import config
from flask import Flask
from flask import request
import redis
from pprint import pprint

app = Flask(__name__)

app.secret_key = "Alterra2020"
# "A0Zr98j/3yXR~ XHH!jmN]LWX/,?RT"

redis_config = {
    "host": "127.0.0.1",
    "port": 6379,
    "db": 0,
    "charset": "utf-8",
    "decode_responses":True
}
save_redis = redis.Redis(**redis_config)

my_flask = os.environ.get("FLASK_ENV", "Production")
if my_flask == "Production":
    app.config.from_object(config.ProductionHedwig)
elif my_flask == "Development":
    app.config.from_object(config.DevelopmentHedwig)

from functions import bot_reply
from blueprints.NLP.bot import chat
from blueprints.formula import formula
from blueprints.harga import harga
from blueprints.jenis_tagihan import jenis_tagihan
from blueprints.jenis_unit import jenis_unit
from blueprints.login import login
from blueprints.pelanggan import pelanggan
from blueprints.produk import produk
from blueprints.register import register
from blueprints.aktivasi_rekening import aktivasi_rekening
from blueprints.unit import unit
from blueprints.tagihan import tagihan
from blueprints.link_tagihan import link_tagihan
from blueprints.riwayat_tagihan import riwayat_tagihan

@app.route("/")
def hello():
    return "Hello, Hedwig Chatbot AturTagihan Here!"

@app.route("/webhooks/inbound-message", methods=["POST"])
def inbound_message():
    incoming_response = request.get_json()
    incoming_msg = incoming_response["message"]["content"]["text"]
    remote_number = incoming_response["from"]["number"]
    pprint(incoming_response)
    bot_responses = chat(incoming_msg)
    message = []
    
    # Jika user BELUM login atau register
    if save_redis.get("%s::token"%(remote_number)) is None:
        if "aturtagihan" == bot_responses[0]:
            message.append(bot_responses[1])
            message.append("1. Masuk")
            message.append("2. Daftar")
            message = [("\n").join(message)]
            
            send_message = ["Apakah Anda sudah memiliki akun? Silakan pilih menu yang sesuai ya!"]
            send_message.append("")
            send_message.append("(contoh: *1* atau *masuk*)")
            message.append(("\n").join(send_message))
            save_redis.delete("%s::menu"%(remote_number), "")
            
        # jika user SUDAH masuk menu LOGIN atau REGISTER
        elif save_redis.get("%s::menu"%(remote_number)) is not None:
            if "login" in save_redis.get("%s::menu"%(remote_number)):
                message = login(incoming_msg, remote_number, bot_responses[1])
            elif "daftar" in save_redis.get("%s::menu"%(remote_number)):
                message = register(incoming_msg, remote_number, bot_responses[1])
            
        # jika user BELUM masuk menu LOGIN atau REGISTER
        elif "masuk" == bot_responses[0] or "1" in incoming_msg:
            save_redis.set("%s::menu"%(remote_number), "login")
            message = login(incoming_msg, remote_number, bot_responses[1])
        elif "daftar" == bot_responses[0] or "2" in incoming_msg:
            save_redis.set("%s::menu"%(remote_number), "daftar")
            message = register(incoming_msg, remote_number, bot_responses[1])
        
        # jika user mengetik hal lain tapi belum login atau register
        else:
            message.append("Hedwig belum kenal sama Anda karena Anda belum masuk!")
            message.append("Silakan ketik *masuk* untuk masuk")
            message.append("Silakan ketik *daftar* untuk mendaftarkan akun")
            message = [("\n").join(message)]
            
    # Jika user SUDAH login atau register
    elif save_redis.get("%s::token"%(remote_number)) is not None:
        if "beranda" == bot_responses[0]:
            message.append("Halo %s! Hedwig siap membantumu.." %(save_redis.get("%s::name"%(remote_number))))
            message.append(bot_responses[1])
            message.append("")
            message.append("Apa yang bisa Hedwig bantu?")
            message.append("1. *buat tagihan* - membuat tagihan")
            message.append("2. *riwayat tagihan* - melihat riwayat tagihan dan membuat ulang link tagihan")
            message.append("3. *pengaturan* - untuk masuk ke menu produk, jenis tagihan, jenis unit, harga, formula, pelanggan, unit, dan aktivasi rekening")
            message = [("\n").join(message)]
            
            send_message = ["Silakan pilih menu yang Anda inginkan ya"]
            send_message.append("")
            send_message.append("(contoh: *1* atau *buat tagihan*)")
            message.append(("\n").join(send_message))
            
            save_redis.delete("%s::menu"%(remote_number),"")
            save_redis.set("%s::submenu"%(remote_number),"beranda")
            
        elif "pengaturan" == bot_responses[0] or ("3" == incoming_msg and save_redis.get("%s::submenu"%(remote_number)) == "beranda"):
            bot_responses = chat("pengaturan")
            message.append(bot_responses[1])
            send_message = ["Di halaman ini, Anda bisa menambah, mengubah, atau menghapus data properti Anda"]
            message.append(("\n").join(send_message))
            message.append("Apa yang bisa Hedwig bantu?")
            
            send_message = ["1. *Produk*"]
            send_message.append("2. *Jenis unit*")
            send_message.append("3. *Jenis tagihan*")
            send_message.append("4. *Harga*")
            send_message.append("5. *Formula*")
            send_message.append("6. *Pelanggan*")
            send_message.append("7. *Unit*")
            send_message.append("8. *Aktivasi rekening* (daftar ke pembayaran digital)")
            message.append(("\n").join(send_message))
            
            send_message = ["Silakan pilih menu yang Anda inginkan ya"]
            send_message.append("")
            send_message.append("(contoh: *1* atau *produk*)")
            message.append(("\n").join(send_message))
            
            save_redis.set("%s::submenu"%(remote_number), "pengaturan")
            save_redis.delete(f"{remote_number}::menu", "")
            
        elif save_redis.get("%s::menu"%(remote_number)) is not None:
            if "jenis_tagihan" in save_redis.get("%s::menu"%(remote_number)):
                message = jenis_tagihan(incoming_msg, remote_number, bot_responses[1])
            elif "tagihan" in save_redis.get("%s::menu"%(remote_number)):
                message = tagihan(incoming_msg, remote_number, bot_responses[1])
            elif "riwayat" in save_redis.get("%s::menu"%(remote_number)):
                if "4" in incoming_msg or "link" == bot_responses[0]:
                    bot_responses = chat("link")
                    save_redis.set(f"{remote_number}::menu", "link")
                    message = link_tagihan(incoming_msg, remote_number, bot_responses[1])
                else:
                    message = riwayat_tagihan(incoming_msg, remote_number, bot_responses[1])
            elif "produk" in save_redis.get("%s::menu"%(remote_number)):
                message = produk(incoming_msg, remote_number, bot_responses[1])
            elif "jenis_unit" in save_redis.get("%s::menu"%(remote_number)):
                message = jenis_unit(incoming_msg, remote_number, bot_responses[1])
            elif "harga" in save_redis.get("%s::menu"%(remote_number)):
                message = harga(incoming_msg, remote_number, bot_responses[1])
            elif "formula" in save_redis.get("%s::menu"%(remote_number)):
                message = formula(incoming_msg, remote_number, bot_responses[1])
            elif "pelanggan" in save_redis.get("%s::menu"%(remote_number)):
                message = pelanggan(incoming_msg, remote_number, bot_responses[1])
            elif "unit" in save_redis.get("%s::menu"%(remote_number)):
                message = unit(incoming_msg, remote_number, bot_responses[1])
            elif "aktivasi_rekening" in save_redis.get("%s::menu"%(remote_number)):
                message = aktivasi_rekening(incoming_msg, remote_number, bot_responses[1])
            elif "link" in save_redis.get("%s::menu"%(remote_number)):
                message = link_tagihan(incoming_msg, remote_number, bot_responses[1])
            
        elif save_redis.get("%s::menu"%(remote_number)) is None and save_redis.get("%s::submenu"%(remote_number)) is not None:
            if save_redis.get("%s::submenu"%(remote_number)) == "beranda":
                if "buat tagihan" == bot_responses[0] or "1" in incoming_msg:
                    bot_responses = chat("buat tagihan")
                    save_redis.set("%s::menu"%(remote_number), "tagihan")
                    message = tagihan(incoming_msg, remote_number, bot_responses[1])
                elif "riwayat tagihan" == bot_responses[0] or "2" in incoming_msg:
                    bot_responses = chat("riwayat tagihan")
                    save_redis.set("%s::menu"%(remote_number), "riwayat")
                    message = riwayat_tagihan(incoming_msg, remote_number, bot_responses[1])
            
            elif save_redis.get("%s::submenu"%(remote_number)) == "pengaturan":
                if "produk" == bot_responses[0] or "1" in incoming_msg:
                    bot_responses = chat("produk")
                    save_redis.set("%s::menu"%(remote_number), "produk")
                    save_redis.delete("%s::submenu"%(remote_number), "")
                    message = produk(incoming_msg, remote_number, bot_responses[1])
                elif "jenis unit" == bot_responses[0] or "2" in incoming_msg:
                    bot_responses = chat("jenis unit")
                    save_redis.set("%s::menu"%(remote_number), "jenis_unit")
                    save_redis.delete("%s::submenu"%(remote_number), "")
                    message = jenis_unit(incoming_msg, remote_number, bot_responses[1])
                elif "jenis tagihan" == bot_responses[0] or "3" in incoming_msg:
                    bot_responses = chat("jenis tagihan")
                    save_redis.set("%s::menu"%(remote_number), "jenis_tagihan")
                    save_redis.delete("%s::submenu"%(remote_number), "")
                    message = jenis_tagihan(incoming_msg, remote_number, bot_responses[1])
                elif "harga" == bot_responses[0] or "4" in incoming_msg:
                    bot_responses = chat("harga")
                    save_redis.set("%s::menu"%(remote_number), "harga")
                    save_redis.delete("%s::submenu"%(remote_number), "")
                    message = harga(incoming_msg, remote_number, bot_responses[1])
                elif "formula" == bot_responses[0] or "5" in incoming_msg:
                    bot_responses = chat("formula")
                    save_redis.set("%s::menu"%(remote_number), "formula")
                    save_redis.delete("%s::submenu"%(remote_number), "")
                    message = formula(incoming_msg, remote_number, bot_responses[1])
                elif "pelanggan" == bot_responses[0] or "6" in incoming_msg:
                    bot_responses = chat("pelanggan")
                    save_redis.set("%s::menu"%(remote_number), "pelanggan")
                    save_redis.delete("%s::submenu"%(remote_number), "")
                    message = pelanggan(incoming_msg, remote_number, bot_responses[1])
                elif "unit" == bot_responses[0] or "7" in incoming_msg:
                    bot_responses = chat("unit")
                    save_redis.set("%s::menu"%(remote_number), "unit")
                    save_redis.delete("%s::submenu"%(remote_number), "")
                    message = unit(incoming_msg, remote_number, bot_responses[1])
                elif "aktivasi rekening" == bot_responses[0] or "8" in incoming_msg:
                    bot_responses = chat("aktivasi rekening")
                    save_redis.set("%s::menu"%(remote_number), "aktivasi_rekening")
                    save_redis.delete("%s::submenu"%(remote_number), "")
                    message = aktivasi_rekening(incoming_msg, remote_number, bot_responses[1])
        else:
            message.append("Anda sudah masuk kok")
            message.append("Anda bisa ketik *Beranda* untuk langsung ke menu Beranda")
            message = [("\n").join(message)]
    
    for i in range(len(message)):
        if type(message[i]) is list:
            bot_reply(("\n").join(message[i]), remote_number)
        else:
            bot_reply(message[i], remote_number)
            
    token = save_redis.get("%s::token"%(remote_number))
    if token is not None:
        save_redis.set("%s::token"%(remote_number), token, ex=3600*24)
    return "200"

@app.route("/webhooks/message-status", methods=["POST"])
def message_status():
    data = request.get_json()
    pprint(data)
    return "200"