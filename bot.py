from flask import Flask, request, jsonify

app = Flask(__name__)

# Remplacez par votre page access token et verification token
PAGE_ACCESS_TOKEN = 'EAARgJ3oIAXgBOwo8Pt4GpWIMr1xXyh3kUFkoZAynK5n16n9qhRsGZBBABY3I2oBoKqXIkArwJoFOAHqa6bfzAivIXlyliB6Rr87YwhZBQsqYtZCiDFS0g45mZCaNqhZAxEaBtBNQIxwLbiKUf24cmcLwPyuVznsql9SOwqRy60AAzywGaHkKDjZBWNc8bJQ'
VERIFY_TOKEN = 'Moramanga'

@app.route('/', methods=['GET'])
def verify_webhook():
    # Vérification du token lors de l'enregistrement de la webhook
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.verify_token") == VERIFY_TOKEN:
        return request.args.get("hub.challenge"), 200
    return "Invalid verification token", 403

@app.route('/', methods=['POST'])
def receive_message():
    data = request.get_json()

    # Vérification que l'événement provient de Facebook et contient des messages
    if data['object'] == 'page':
        for entry in data['entry']:
            for messaging_event in entry['messaging']:
                if messaging_event.get('message'):
                    sender_id = messaging_event['sender']['id']
                    message_text = messaging_event['message']['text']
                    
                    # Répondre au message
                    send_message(sender_id, "Bonjour Bruno !")

    return "Message Received", 200

def send_message(recipient_id, message_text):
    # Fonction pour envoyer un message à l'utilisateur
    # Utilisez l'API Messenger de Facebook pour envoyer le message
    
    # Importez les modules nécessaires pour utiliser l'API Messenger
    import requests

    # Endpoint de l'API Messenger de Facebook pour envoyer des messages
    endpoint = 'https://graph.facebook.com/v12.0/me/messages'
    
    # Paramètres du message
    params = {
        'access_token': PAGE_ACCESS_TOKEN
    }

    # Corps du message au format JSON
    data = {
        'recipient': {
            'id': recipient_id
        },
        'message': {
            'text': message_text
        }
    }

    # Envoi du message en utilisant une requête POST à l'API Messenger de Facebook
    response = requests.post(endpoint, params=params, json=data)
    if response.status_code == 200:
        print("Message envoyé avec succès")
    else:
        print("Échec de l'envoi du message")

if __name__ == "__main__":
    app.run(port=3000)
