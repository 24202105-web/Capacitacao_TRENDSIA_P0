import os
from dataclasses import dataclass
from dotenv import load_dotenv

PROMPT_PADRAO = (
    "Você é um tutor de inglês amigável ajudando um estudante brasileiro.\n"
    "Para cada mensagem em inglês:\n"
    "1. Se houver erros, mostre a correção de forma gentil. Se estiver correto, elogie.\n"
    "2. Responda em inglês e em português para reforçar a compreensão e faça UMA nova pergunta simples para continuar a conversa."
)

PLACEHOLDERS_INVALIDOS = {"sua_chave_aqui", "SUA_CHAVE_AQUI", "COLE_SUA_CHAVE_AQUI"}


class ConfiguracaoError(Exception):
    """Erro levantado quando variáveis obrigatórias ou parâmetros estão ausentes/inválidos."""


@dataclass(frozen=True)
class TutorConfig:
    api_key: str
    model: str = "gemini-3.5-flash-lite"
    temperature: float = 0.7
    max_output_tokens: int = 500
    system_prompt: str = PROMPT_PADRAO
    log_level: str = "INFO"
    log_file: str = "execucao.log"


def carregar_configuracao(carregar_dotenv: bool = True) -> TutorConfig:
    """Carrega e valida as configurações a partir de variáveis de ambiente."""
    if carregar_dotenv:
        load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        raise ConfiguracaoError(
            "A variável GEMINI_API_KEY não foi encontrada no arquivo .env. "
            "Crie o arquivo .env baseado no .env.example e adicione sua chave."
        )

    if api_key in PLACEHOLDERS_INVALIDOS:
        raise ConfiguracaoError(
            "A chave informada no arquivo .env ainda é um placeholder padrão. "
            "Substitua 'sua_chave_aqui' por uma chave válida obtida no Google AI Studio."
        )

    model = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite").strip()
    if not model:
        raise ConfiguracaoError("A variável GEMINI_MODEL não pode estar vazia.")

    try:
        temperature = float(os.getenv("GEMINI_TEMPERATURE", "0.7"))
    except ValueError as exc:
        raise ConfiguracaoError("GEMINI_TEMPERATURE deve ser um número decimal (ex: 0.7).") from exc

    if not 0.0 <= temperature <= 2.0:
        raise ConfiguracaoError("GEMINI_TEMPERATURE deve estar entre 0.0 e 2.0.")

    try:
        max_output_tokens = int(os.getenv("GEMINI_MAX_OUTPUT_TOKENS", "500"))
    except ValueError as exc:
        raise ConfiguracaoError("GEMINI_MAX_OUTPUT_TOKENS deve ser um número inteiro.") from exc

    if max_output_tokens <= 0:
        raise ConfiguracaoError("GEMINI_MAX_OUTPUT_TOKENS deve ser maior que zero.")

    system_prompt = os.getenv("TUTOR_SYSTEM_PROMPT", PROMPT_PADRAO).strip() or PROMPT_PADRAO
    log_level = os.getenv("LOG_LEVEL", "INFO").strip().upper()
    log_file = os.getenv("LOG_FILE", "execucao.log").strip() or "execucao.log"

    return TutorConfig(
        api_key=api_key,
        model=model,
        temperature=temperature,
        max_output_tokens=max_output_tokens,
        system_prompt=system_prompt,
        log_level=log_level,
        log_file=log_file,
    )