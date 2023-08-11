import openai

openai.api_key = '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'  # Remplacez par votre propre clé API OpenAI

def conversation_openai(prompt):
    response = openai.Completion.create(
        engine='davinci',
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

print("Bienvenue dans le chatbot ! Entrez 'exit' pour quitter.")

historique_conversation = ""

while True:
    saisie_utilisateur = input("Vous : ")
    if saisie_utilisateur.lower() == 'exit':
        break
    
    historique_conversation += f"Vous : {saisie_utilisateur}\n"
    
    reponse_bot = conversation_openai(historique_conversation)
    historique_conversation += f"Bot : {reponse_bot}\n"
    
    print(f"Bot : {reponse_bot}")
