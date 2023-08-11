from flask import Flask, request, jsonify 
import openai
import requests

app = Flask(__name__)

# Remplacez par votre page access token et verification token
PAGE_ACCESS_TOKEN = 'EAARgJ3oIAXgBO3ZB1E3WmzUGoA5cdJ8zujuk472ifu9ZBVWnzAiYo4t6qhRrDHTvl1OnqWpQ7bZBkoQGWr2rBGdN4CFYfZB359ceezSrwu9XWgViXEmf2H2kjnRHo0frMu2EZA8JaH4quZB6qI2qmFtz2fUsV9YpMVKbaFCStMTSoHyFxwW9fyAPX3tD6ZB'
VERIFY_TOKEN = 'Moramanga'

# Remplacez par votre API Key d'OpenAI
OPENAI_API_KEY = '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'

# Fonction pour obtenir une réponse de ChatGPT
def chat_with_gpt(prompt):
    openai.api_key = OPENAI_API_KEY
    response = openai.Completion.create(
        engine="text-davinci-002", # Vous pouvez essayer d'autres moteurs, comme "text-davinci-003" ou "text-gpt3.5-turbo"
        prompt=prompt,
        max_tokens=100,
        stop=['\n'] # Arrête la génération de texte à la première ligne
    )
    return response.choices[0].text.strip()

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

                    # Obtenir une réponse de ChatGPT
                    response_text = chat_with_gpt(message_text)

                    # Répondre au message avec la réponse de ChatGPT
                    send_message(sender_id, response_text)

        return "Message Received", 200

def send_message(recipient_id, message_text):
    # Fonction pour envoyer un message à l'utilisateur
    # Utilisez l'API Messenger de Facebook pour envoyer le message

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
