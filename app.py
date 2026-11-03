import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai.errors import APIError

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("Erro: A variável da GEMINI não foi encontrada no arquivo .env.")
    sys.exit(1)

client = genai.Client(api_key=api_key)

SYSTEM_PROMPT = """
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

    while True:
        # 1. Recebe a entrada textual do usuário pelo terminal
        entrada = input("Você (em inglês): ")
        
        if entrada.lower().strip() in ['sair', 'exit', 'quit']:
            print("Goodbye! See you next time! 👋")
            break

        if not entrada.strip():
            continue

        # 2. Solicitação derivada da entrada enviada ao LLM
        prompt_derivado = f"{SYSTEM_PROMPT}\n\nMensagem do aluno: {entrada}"

        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt_derivado
            )
            # 3. Apresenta a resposta ao usuário
            print(f"\n🤖 Tutor:\n{response.text}\n")
            print("-" * 50)
            
        except APIError as e:
            print(f"\n❌ Erro na chamada da API: {e.message}\n")

if __name__ == "__main__":
    main()