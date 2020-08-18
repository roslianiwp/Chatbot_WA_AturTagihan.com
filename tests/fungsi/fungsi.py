def send_message(phone_number, incoming_msg):
    return {
            "from": { "type": "whatsapp", "number": "14157386170" },
            "to": { "type": "whatsapp", "number": phone_number },
            "message": {
                "content": {
                    "type": "text",
                    "text": incoming_msg
                }
            }
        }