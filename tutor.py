import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai.errors import APIError

SYSTEM_PROMPT = """
Você é um tutor de inglês amigável ajudando um estudante brasileiro.
Para cada mensagem em inglês:
1. Se houver erros, mostre a correção de forma gentil. Se estiver correto, elogie.
2. Responda em inglês e em português para reforçar a compreensão e faça UMA nova pergunta simples para continuar a conversa.
"""

def carregar_configuracao() -> genai.Client:
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Erro: GEMINI_API_KEY não encontrada no arquivo .env.")
        sys.exit(1)
    return genai.Client(api_key=api_key)

def processar_mensagem(client: genai.Client, entrada_usuario: str) -> str | None:
    prompt = f"{SYSTEM_PROMPT}\n\nMensagem do aluno: {entrada_usuario}"
    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt
        )
        return response.text
    except APIError as e:
        print(f"\n Erro na chamada da API: {e.message}\n")
        return None