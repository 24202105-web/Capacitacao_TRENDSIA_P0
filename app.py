import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai.errors import APIError

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("Erro: GEMINI_API_KEY não encontrada no .env")
    sys.exit(1)

client = genai.Client(api_key=api_key)

SYSTEM_PROMPT = """
Você é um tutor de inglês amigável ajudando um estudante brasileiro.
Para cada mensagem em inglês:
1. Se houver erros, mostre a correção de forma gentil. Se estiver correto, elogie.
2. Responda em inglês e em portugês para forçar a compreenção e faça UMA nova pergunta simples para continuar a conversa.
"""

def main():
    print("🇬🇧 English Tutor Assistant - Nível Básico (Gemini AI)")
    print("Escreva suas mensagens em inglês! Digite 'sair' para encerrar.\n")
    print("-" * 50)

    while True:
        entrada = input("Você (em inglês): ")
        
        if entrada.lower().strip() in ['sair', 'exit', 'quit']:
            print("Goodbye! 👋")
            break

        if not entrada.strip():
            continue

        prompt_derivado = f"{SYSTEM_PROMPT}\n\nMensagem do aluno: {entrada}"

        try:
            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=prompt_derivado
            )
            print(f"\n🤖 Tutor:\n{response.text}\n")
            print("-" * 50)
            
        except APIError as e:
            print(f"\n❌ Erro na chamada da API: {e.message}\n")

if __name__ == "__main__":
    main()