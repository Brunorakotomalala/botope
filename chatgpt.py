import openai
openai.api_key = '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'  # Remplace 'ta_clé_api_openai' par ta propre clé API OpenAI
def envoyer_requete_chatgpt(message):
    response = openai.Completion.create(
        engine='davinci-codex',  # Tu peux utiliser d'autres moteurs si tu le souhaites
        prompt=message,
        max_tokens=100,
        temperature=0.7,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    return response.choices[0].text.strip()

while True:
    user_input = input("Tape ta question ici : ")
    if user_input.lower() == 'exit':
        break
    response = envoyer_requete_chatgpt(user_input)
    print(response)
