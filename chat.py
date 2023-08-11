import openai

openai.api_key = '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'  # Remplacez par votre propre clé API OpenAI

def conversation_openai(prompt):
    response = openai.Completion.create(
        engine='davinci',
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

print("Bienvenue dans le chatbot ! Tapez 'exit' pour quitter.")

conversation_history = ""

while True:
    user_input = input("Vous: ")
    if user_input.lower() == 'exit':
        break
    
    conversation_history += f"Vous: {user_input}\n"
    
    bot_response = conversation_openai(conversation_history)
    conversation_history += f"Bot: {bot_response}\n"
    
    print(f"Bot: {bot_response}")
