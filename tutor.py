import logging
import time
from google import genai
from google.genai import types
from google.genai.errors import APIError
from config import TutorConfig

logger = logging.getLogger("tutor_ingles")


def configurar_logs(log_level: str = "INFO", log_file: str = "execucao.log") -> None:
    """Configura registros de execução em arquivo sem poluir o terminal do usuário."""
    if logger.handlers:
        return

    nivel = getattr(logging, log_level.upper(), logging.INFO)
    logger.setLevel(nivel)

    handler = logging.FileHandler(log_file, encoding="utf-8")
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def criar_cliente(config: TutorConfig) -> genai.Client:
    """Instancia o cliente do SDK Google GenAI usando a configuração carregada."""
    logger.info("Inicializando cliente GenAI (modelo=%s).", config.model)
    return genai.Client(api_key=config.api_key)


def preparar_config_geracao(config: TutorConfig) -> types.GenerateContentConfig:
    """Monta os parâmetros de geração do LLM a partir da configuração externa."""
    return types.GenerateContentConfig(
        system_instruction=config.system_prompt,
        temperature=config.temperature,
        max_output_tokens=config.max_output_tokens,
    )


def processar_mensagem(
    client: genai.Client, config: TutorConfig, entrada_usuario: str
) -> str | None:
    """Envia a mensagem ao modelo e trata falhas sem expor credenciais ou dados sensíveis."""
    entrada_limpa = entrada_usuario.strip()
    if not entrada_limpa:
        logger.warning("Solicitação ignorada: entrada vazia.")
        return None

    gen_config = preparar_config_geracao(config)
    inicio = time.perf_counter()

    logger.info(
        "Enviando solicitação ao LLM (modelo=%s, chars_entrada=%d, max_tokens=%d, temp=%.2f).",
        config.model,
        len(entrada_limpa),
        config.max_output_tokens,
        config.temperature,
    )

    try:
        response = client.models.generate_content(
            model=config.model,
            contents=entrada_limpa,
            config=gen_config,
        )
        duracao_ms = (time.perf_counter() - inicio) * 1000

        if not response or not getattr(response, "text", None) or not response.text.strip():
            logger.warning("Resposta vazia recebida do LLM (duracao_ms=%.1f).", duracao_ms)
            print("\n⚠️ O serviço respondeu, mas não retornou um conteúdo válido. Tente novamente.")
            return None

        resposta_texto = response.text.strip()
        logger.info(
            "Resposta processada com sucesso (duracao_ms=%.1f, chars_saida=%d).",
            duracao_ms,
            len(resposta_texto),
        )
        return resposta_texto

    except APIError as e:
        duracao_ms = (time.perf_counter() - inicio) * 1000
        codigo = getattr(e, "code", "desconhecido")
        mensagem_erro = str(e).lower()

        if (
            "api_key" in mensagem_erro
            or "invalid" in mensagem_erro
            or "unauthenticated" in mensagem_erro
            or codigo in (400, 401, 403)
        ):
            logger.error(
                "Falha de autenticação na API (codigo=%s, duracao_ms=%.1f).", codigo, duracao_ms
            )
            print("\n❌ [Erro de Autenticação] A chave de API fornecida foi recusada pelo servidor do Google.")
            print("Verifique se a sua GEMINI_API_KEY no arquivo .env está correta e ativa.\n")

        elif (
            "high demand" in mensagem_erro
            or "unavailable" in mensagem_erro
            or "quota" in mensagem_erro
            or codigo in (429, 503)
        ):
            logger.warning(
                "Serviço temporariamente indisponível ou limite atingido (codigo=%s, duracao_ms=%.1f).",
                codigo,
                duracao_ms,
            )
            print("\n⚠️ [Serviço Indisponível] O modelo do Gemini está enfrentando alta demanda ou limite de uso.")
            print("Por favor, aguarde alguns instantes e tente novamente.\n")

        else:
            logger.error("Erro na API do LLM (codigo=%s, duracao_ms=%.1f).", codigo, duracao_ms)
            print(f"\n❌ [Falha na API] Ocorreu um problema ao se comunicar com o serviço (código {codigo}).\n")

        return None

    except Exception as e:
        duracao_ms = (time.perf_counter() - inicio) * 1000
        logger.error(
            "Falha de comunicação ou timeout (tipo=%s, duracao_ms=%.1f).",
            type(e).__name__,
            duracao_ms,
        )
        print("\n❌ [Falha de Comunicação] Não foi possível conectar ao serviço de IA.")
        print("Verifique sua conexão com a internet e se há bloqueios de rede/firewall.\n")
        return None