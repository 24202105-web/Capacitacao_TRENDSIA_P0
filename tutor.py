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
    """Carrega as variáveis de ambiente e valida a chave de API."""
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")

    # Tratamento: Credencial ausente
    if not api_key or api_key.strip() == "":
        print("\n [Erro de Configuração] Credencial ausente!")
        print("A variável GEMINI_API_KEY não foi encontrada no arquivo .env.")
        print("Crie o arquivo .env baseado no .env.example e adicione sua chave.\n")
        sys.exit(1)

    # Tratamento: Credencial visivelmente inválida/placeholder
    if api_key.strip() in ["sua_chave_aqui", "SUA_CHAVE_AQUI"]:
        print("\n❌ [Erro de Autenticação] Credencial inválida!")
        print("A chave informada no arquivo .env ainda é um placeholder padrão.")
        print("Substitua 'sua_chave_aqui' por uma chave válida obtida no Google AI Studio.\n")
        sys.exit(1)

    return genai.Client(api_key=api_key)

def processar_mensagem(client: genai.Client, entrada_usuario: str) -> str | None:
    """Envia a mensagem ao modelo e trata cenários de falha de comunicação, credencial inválida e timeout."""
    prompt = f"{SYSTEM_PROMPT}\n\nMensagem do aluno: {entrada_usuario}"

    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt
        )

        # Tratamento: Resposta vazia ou em formato inesperado
        if not response or not hasattr(response, 'text') or not response.text:
            print("\n O serviço respondeu, mas não retornou um conteúdo válido. Tente novamente.")
            return None

        return response.text.strip()

    except APIError as e:
        mensagem_erro = str(e).lower()

        # Tratamento: Credencial inválida retornada pelo servidor (ex: 400/403/UNAUTHENTICATED)
        if "api_key" in mensagem_erro or "invalid" in mensagem_erro or "unauthenticated" in mensagem_erro or "400" in mensagem_erro:
            print("\n❌ [Erro de Autenticação] A chave de API fornecida foi recusada pelo servidor do Google.")
            print("Verifique se a sua GEMINI_API_KEY no arquivo .env está correta e ativa.\n")

        # Tratamento: Indisponibilidade ou alta demanda (503/RESOURCE_EXHAUSTED)
        elif "high demand" in mensagem_erro or "unavailable" in mensagem_erro or "503" in mensagem_erro or "quota" in mensagem_erro:
            print("\n⚠️ [Serviço Indisponível] O modelo do Gemini está enfrentando alta demanda no momento.")
            print("Por favor, aguarde alguns instantes e tente novamente.\n")

        # Tratamento: Erro genérico da API sem expor stacktrace técnico extenso
        else:
            print(f"\n❌ [Falha na API] Ocorreu um problema ao se comunicar com o serviço: {e.message}\n")

        return None

    except Exception as e:
        # Tratamento: Timeout ou falhas gerais de conexão
        print(f"\n❌ [Falha de Comunicação] Não foi possível conectar ao serviço de IA.")
        print("Verifique sua conexão com a internet e se há bloqueios de rede/firewall.\n")
        return None