import sys
from config import ConfiguracaoError, carregar_configuracao
from tutor import configurar_logs, criar_cliente, logger, processar_mensagem


def main():
    """Gerencia a captura de dados e exibição do fluxo no terminal."""
    try:
        config = carregar_configuracao()
    except ConfiguracaoError as erro:
        print(f"\n❌ [Erro de Configuração] {erro}\n")
        sys.exit(1)

    configurar_logs(log_level=config.log_level, log_file=config.log_file)
    logger.info("Sessão do English Tutor iniciada.")

    client = criar_cliente(config)

    print("🇬🇧 English Tutor Assistant - Nível Avançado")
    print(f"Modelo ativo: {config.model} | Max tokens: {config.max_output_tokens} | Temp: {config.temperature}")
    print("Escreva suas mensagens em inglês! Digite 'sair' para encerrar.\n")
    print("-" * 50)

    while True:
        try:
            entrada = input("Você (em inglês): ")
        except (KeyboardInterrupt, EOFError):
            logger.info("Sessão encerrada pelo usuário via interrupção.")
            print("\n\nGoodbye! 👋")
            break

        entrada_limpa = entrada.strip()
        if not entrada_limpa:
            print("⚠️ Entrada vazia! Por favor, digite uma frase em inglês ou 'sair' para encerrar.\n")
            continue

        if entrada_limpa.lower() in ["sair", "exit", "quit"]:
            logger.info("Sessão encerrada normalmente pelo usuário.")
            print("Goodbye! 👋")
            break

        resposta = processar_mensagem(client, config, entrada_limpa)
        if resposta:
            print(f"\n🤖 Tutor:\n{resposta}\n")
            print("-" * 50)


if __name__ == "__main__":
    main()