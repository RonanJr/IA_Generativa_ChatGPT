import pandas as pd
import requests
import json
import openai

api_url = 'https://sdw-2023-prd.up.railway.app'
openai_api_key = 'SUA CHAVE'

openai.api_key = openai_api_key


##------------PEGA OS USUARIOS DO CSV
#df = pd.read_csv('../UsersID.txt')
#users_id = df['UsersID'].tolist()
users_id = [1,2,3029]

##------------MANDA A REQUISIÇÂO PARA A API E RETORNA OS DADOS JSON
def get_users(id):
    response = requests.get(f'{api_url}/users/{id}')
    return response.json() if response.status_code == 200 else None

users = [user for id in users_id if (user := get_users(id)) is not None]
##print(json.dumps(users, indent=2))

##------------ABRE O CHAT_GPT
def generate_ai_news(user):
    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messagens=[
            {"role": "system", "content": "Você é um especialista em Vendas Online"},
            {"role": "user", "content": f"Crie uma mensagem para {user['name']} sobre vendas online (maximo de 100 caracteres)"},
        ]
    )
    return completion.choices[0].message.content.strip('\"')

for user in users:
    news = generate_ai_news(user)


def update_user(user):
    response = requests.put(f"{api_url}/users/{id}", json=user)
    return True if response.status_code == 200 else False

for user in users:
    success = update_user(user)
    
print(news)
