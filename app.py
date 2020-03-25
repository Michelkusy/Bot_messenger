import os
import json
import predict_reply

import requests
from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET'])
def verify():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "Hello world", 200

# C'est ici que l'on gère les messages reçus
@app.route('/', methods=['POST'])
def webhook():
    try:
        data = request.get_json()
        if data["object"] == "page":
            for entry in data["entry"]:
                for messaging_event in entry["messaging"]:
                    # Si quelqu'un nous envoie un message: c'est ce qui nous intéresse ici
                    if messaging_event.get("message"):
                        # L'id facebook de notre interlocuteur
                        sender_id = messaging_event["sender"]["id"]
                        # L'id facebook de notre bot
                        recipient_id = messaging_event["recipient"]["id"]
                        try:
                            # Le message qu'on a reçu
                            message_text = messaging_event["message"]["text"]
                            # On fait réfléchir notre bot à une réponse...
                            reply = predict(message_text)
                            # ... et on l'envoie !
                            send_message(sender_id, reply)
                        except:
                            # Quand le bot ne comprends pas :(
                            send_message(sender_id, "Désolé j'ai bugué.")
        return "ok", 200
    except:
        pass

# La requête qui permet au bot de répondre un certain message
def send_message(recipient_id, message_text):
    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params = params, headers = headers, data = data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)

def log(message):
    print(message)

# Notre fonction qui permet à notre bot de répondre
def predict(incoming_msg):
    return predict_reply.classify(incoming_msg);

if __name__ == '__main__':
    app.run(debug = True)
