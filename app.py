import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai.errors import APIError

# Carrega as variáveis do arquivo .env
load_dotenv()

# Verifica se a chave foi configurada
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("❌ Erro: A variável GEMINI_API_KEY não foi encontrada no arquivo .env.")
    sys.exit(1)

# Inicializa o cliente oficial da API do Gemini
client = genai.Client(api_key=api_key)

# Instrução de sistema para o papel de tutor
SYSTEM_INSTRUCTION = """
Você é um tutor de inglês amigável e paciente ajudando um estudante brasileiro.
Para cada mensagem que o usuário enviar em inglês:
1. Se houver erros gramaticais ou de vocabulário, mostre a correção de forma gentil. Se estiver correto, elogie rapidamente.
2. Responda em inglês de forma natural e faça UMA nova pergunta simples para dar continuidade à conversa.
Mantenha suas respostas curtas e diretas.
"""

def main():
    print("🇬🇧 English Tutor Assistant - Nível Básico (Gemini AI)")
    print("Escreva suas mensagens em inglês! Digite 'sair' para encerrar.\n")
    print("-" * 50)

    # Inicializa a sessão de chat com as instruções do sistema e o modelo recomendado
    chat = client.chats.create(
        model="gemini-3.8-flash",
        config={"system_instruction": SYSTEM_INSTRUCTION}
    )

    while True:
        # 1. Recebe a entrada textual do usuário pelo terminal
        entrada = input("Você (em inglês): ")
        
        if entrada.lower().strip() in ['sair', 'exit', 'quit']:
            print("Goodbye! See you next time! 👋")
            break

        if not entrada.strip():
            continue

        try:
            # 2. Envia a mensagem no chat (solicitação derivada com histórico e system instruction)
            response = chat.send_message(entrada)
            
            # 3. Apresenta a resposta ao usuário
            print(f"\n🤖 Tutor:\n{response.text}\n")
            print("-" * 50)
            
        except APIError as e:
            print(f"\n❌ Erro na chamada da API: {e.message}\n")

if __name__ == "__main__":
    main()